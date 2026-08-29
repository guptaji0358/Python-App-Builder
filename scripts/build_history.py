import sqlite3
import datetime

from .user_data import DbPath

DB_FILE = DbPath("builds.db")


class BuildHistory:
    """A small SQLite log of every successful build, stored at
    user-data/db/builds.db. EnsureUserDataDirs() must have created
    user-data/db/ before this is constructed."""

    def __init__(self):
        self.Connection = sqlite3.connect(DB_FILE)
        self.Connection.execute("""
            CREATE TABLE IF NOT EXISTS builds (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                app_name TEXT,
                source_script TEXT,
                output_path TEXT,
                build_type TEXT,
                console_mode TEXT,
                size_mb REAL,
                created_at TEXT
            )
        """)
        self.Connection.commit()

    def Record(self,AppName,SourceScript,OutputPath,BuildType,ConsoleMode,SizeMB):
        self.Connection.execute(
            """INSERT INTO builds
                (app_name,source_script,output_path,build_type,console_mode,size_mb,created_at)
                VALUES (?,?,?,?,?,?,?)""",
            (
                AppName,
                SourceScript,
                OutputPath,
                BuildType,
                ConsoleMode,
                SizeMB,
                datetime.datetime.now().isoformat(timespec="seconds"),
            ),
        )
        self.Connection.commit()

    def Recent(self,Limit=20):
        Cursor = self.Connection.execute(
            """SELECT app_name,output_path,size_mb,created_at
                FROM builds ORDER BY id DESC LIMIT ?""",
            (Limit,),
        )
        return Cursor.fetchall()
