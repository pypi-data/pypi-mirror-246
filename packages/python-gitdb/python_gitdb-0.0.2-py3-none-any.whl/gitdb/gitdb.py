import logging
from typing import Optional, Any

from pygit2 import (
    init_repository,
    Repository,
    IndexEntry,
    GIT_FILEMODE_BLOB,
    Signature
)

from gitdb.serializers import BaseSerializer, JsonSerializer


# prepare logger
log = logging.getLogger(__name__)


class GitDb:
    """
    main class to interact with the git repository as database
    """
    def __init__(
        self,
        repo_path: str,
        serializer: BaseSerializer = JsonSerializer
    ):
        log.debug("initializing git database at '%s'", repo_path)
        self._repo: Repository = init_repository(
            path=repo_path,
            bare=True
        )
        self._serializer = serializer()

    @property
    def repo(self) -> Repository:
        """
        get repository

        :return: repository
        :rtype: Repository
        """
        return self._repo

    @property
    def serializer(self) -> BaseSerializer:
        """
        get serializer

        :return: serializer
        :rtype: BaseSerializer
        """
        return self._serializer

    def set(
        self, k: str,
        data: bytes,
        auto_commit: bool = True
    ):
        """
        Set a value by its key to the git repository database.
        If auto_commit is True, the value will directly be committed.

        :param k: key
        :type k: str
        :param data: data
        :type data: bytes
        :param auto_commit: if True, data will be committed, defaults to True
        :type auto_commit: bool, optional
        """
        log.debug(
            "storing for key '%s': %s", k, data
        )

        # serialize the data
        s = self.serializer.serialize(obj=data)

        log.debug("serialized data: %s", s)

        # store given data as blob and obtain object ID
        oid = self.repo.create_blob(s)

        # create index entry for object ID and add it
        index_entry = IndexEntry(
            path=k,
            object_id=oid,
            mode=GIT_FILEMODE_BLOB
        )
        self.repo.index.add(index_entry)

        if auto_commit is True:
            # automatically commit the data to git
            self.commit()

    def get(
        self,
        k: str
    ) -> Any:
        """
        Get value from git repository database by given key.

        :param k: key
        :type k: str
        :return: value from database
        :rtype: Any
        """
        # get last commit from repository
        last_commit = self.repo[self.repo.head.target]

        data = last_commit.tree[k].data

        log.debug("obtained data for key '%s': %s", k, data)

        # get object data from tree and deserialize it
        obj = self.serializer.deserialize(data)
        log.debug("deserialized data: %s", obj)

        return obj

    def delete(
        self,
        k: str,
        auto_commit: bool = True
    ) -> None:
        """
        Delete data by its key from git repository database

        :param k: key
        :type k: str
        :param auto_commit: if True, data is committed,
                            defaults to True
        :type auto_commit: bool, optional
        """
        self.repo.index.remove(k)

        if auto_commit is True:
            # automatically commit the data to git
            self.commit()

    def commit(
        self,
        message: str = "auto-commit",
        signature: Optional[Signature] = None
    ):
        """
        commit data in git repository

        :param message: message used for commit, defaults to "auto-commit"
        :type message: str, optional
        :param signature: signature used for commit; if not provided the
                          default signature is used, defaults to None
        :type signature: Optional[Signature], optional
        """
        # use given signature or if not provided the default
        signature = signature or self.repo.default_signature

        # resolve the reference
        tree = self.repo.index.write_tree()
        self.repo.index.add_all

        parent, ref = self.repo.resolve_refish(
            refish=self.repo.head.name
        )

        self.repo.create_commit(
            ref.name,
            signature,
            signature,
            message,
            tree,
            [parent.oid]
        )

        # write blob to disk
        self.repo.index.write()

        log.debug(
            "writing commit '%s' by %s to disk", message, signature
        )
