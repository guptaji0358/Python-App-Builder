import sqlite3

from .user_data import DbPath


class IndexDatabase:
    """A tiny name->path cache backed by its own SQLite file. Lets the file
    search index be available instantly on startup (loaded from the last
    scan) while FileIndexerThread/IconIndexerThread refresh it in the
    background, instead of every launch waiting on a fresh full-disk scan."""

    def __init__(self,FileName):
        self.Connection = sqlite3.connect(DbPath(FileName))
        self.Connection.execute("""
            CREATE TABLE IF NOT EXISTS files (
                name TEXT PRIMARY KEY,
                path TEXT NOT NULL
            )
        """)
        self.Connection.commit()

    def Load(self):
        Cursor = self.Connection.execute("SELECT name,path FROM files")
        return dict(Cursor.fetchall())

    def Save(self,Index):
        self.Connection.execute("DELETE FROM files")
        self.Connection.executemany(
            "INSERT INTO files (name,path) VALUES (?,?)",
            list(Index.items()),
        )
        self.Connection.commit()


class PyFileIndexDatabase(IndexDatabase):
    """user-data/db/py_index.db - cached .py file search index."""
    def __init__(self):
        super().__init__("py_index.db")


class IconFileIndexDatabase(IndexDatabase):
    """user-data/db/icon_index.db - cached .ico file search index."""
    def __init__(self):
        super().__init__("icon_index.db")
