import sqlite3
from loguru import logger

from tesseract.file import File, Chunk


class DBManager:
    def __init__(self, db_path: str):
        self.db_path = db_path
        logger.info(f"DBManager initialized with database path: {db_path}")

    def __enter__(self):
        self.db = sqlite3.connect(self.db_path, check_same_thread=False)
        self.cursor = self.db.cursor()
        self.init_db()
        logger.info("Database connection established")
        return self

    def __exit__(self, *_):
        self.db.close()
        logger.info("Database connection closed")

    def init_db(self):
        try:
            self.cursor.execute("""
                CREATE TABLE IF NOT EXISTS files (
                    file_path TEXT PRIMARY KEY,
                    hash TEXT NOT NULL
                )
            """)
            self.cursor.execute("""
                CREATE TABLE IF NOT EXISTS chunks (
                    file_path TEXT NOT NULL,
                    order_num INTEGER NOT NULL,
                    chunk_hash TEXT NOT NULL,
                    PRIMARY KEY (file_path, order_num),
                    FOREIGN KEY (file_path) REFERENCES files (file_path)
                )
            """)
            self.db.commit()
            logger.info("Initialized database tables")
        except sqlite3.Error as e:
            logger.error(f"Error initializing database tables: {e}")
            raise

    def create_file(self, file: File):
        try:
            self.cursor.execute(
                "INSERT INTO files (file_path, hash) VALUES (?, ?)",
                (file.file_path, file.hash)
            )
            self.db.commit()
            logger.info(f"File created in database: {file.file_path}")
        except sqlite3.Error as e:
            logger.error(f"Error creating file in database: {e}")
            raise

    def create_chunk(self, chunk: Chunk):
        try:
            self.cursor.execute(
                "INSERT INTO chunks (file_path, order_num, chunk_hash) VALUES (?, ?, ?)",
                (chunk.file_path, chunk.order, chunk.hash)
            )
            self.db.commit()
            logger.info(f"Chunk created in database: {chunk.file_path} {chunk.order}")
        except sqlite3.Error as e:
            logger.error(f"Error creating chunk in database: {e}")
            raise

    def update_file(self, file: File):
        try:
            self.cursor.execute(
                "UPDATE files SET hash=? WHERE file_path=?",
                (file.hash, file.file_path)
            )
            self.db.commit()
            logger.info(f"File updated in database: {file.file_path}")
        except sqlite3.Error as e:
            logger.error(f"Error updating file in database: {e}")
            raise

    def update_chunk(self, chunk: Chunk):
        try:
            self.cursor.execute(
                "UPDATE chunks SET chunk_hash=? WHERE file_path=? AND order_num=?",
                (chunk.hash, chunk.file_path, chunk.order)
            )
            self.db.commit()
            logger.info(f"Chunk updated in database: {chunk.file_path} {chunk.order}")
        except sqlite3.Error as e:
            logger.error(f"Error updating chunk in database: {e}")
            raise

    def delete_file(self, file_path: str):
        try:
            self.cursor.execute("DELETE FROM files WHERE file_path=?", (file_path, ))
            self.db.commit()
            logger.info(f"File deleted from database: {file_path}")
        except sqlite3.Error as e:
            logger.error(f"Error deleting file from database: {e}")
            raise

    def delete_chunk(self, file_path: str, order: int):
        try:
            self.cursor.execute(
                "DELETE FROM chunks WHERE file_path=? AND order_num=?",
                (file_path, order)
            )
            self.db.commit()
            logger.info(f"Chunk deleted from database: {file_path} {order}")
        except sqlite3.Error as e:
            logger.error(f"Error deleting chunk from database: {e}")
            raise

    def get_chunks(self, file_path: str):
        try:
            self.cursor.execute(
                "SELECT file_path, order_num, chunk_hash FROM chunks WHERE file_path=?",
                (file_path, )
            )
            chunks = [
                Chunk(file_path=row[0], order=row[1], hash=row[2])
                for row in self.cursor.fetchall()
            ]
            logger.info(f"Fetched chunks for file path: {file_path}")
            return chunks
        except sqlite3.Error as e:
            logger.error(f"Database error while fetching chunks: {e}")
            raise

    def get_files(self):
        try:
            self.cursor.execute("SELECT file_path, hash FROM files")
            files = [
                File(file_path=row[0], hash=row[1])
                for row in self.cursor.fetchall()
            ]
            logger.info("Fetched files")
            return files
        except sqlite3.Error as e:
            logger.error(f"Database error while fetching files: {e}")
            raise

    def get_file_by_path(self, file_path: str):
        try:
            self.cursor.execute(
                "SELECT file_path, hash FROM files WHERE file_path=?",
                (file_path, )
            )
            row = self.cursor.fetchone()
            if row is None:
                return None
            file = File(file_path=row[0], hash=row[1])
            logger.info(f"Fetched file by path: {file_path}")
            return file
        except sqlite3.Error as e:
            logger.error(f"Database error while fetching file by path: {e}")
            raise
