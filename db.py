import sqlite3


class Database:
    def __init__(self) -> None:
        self.db = sqlite3.connect("database.db")
        self.cursor = self.db.cursor()

    def __del__(self) -> None:
        self.cursor.close()
        self.db.close()

    def setup(self) -> None:
        self.cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS server (
                id INTEGER PRIMARY KEY,
                welcome_channel_id INTEGER
            )
            """
        )
        self.db.commit()

    def get_welcome_channel_id(self, guild_id: int) -> int | None:
        self.cursor.execute(
            f"""
            SELECT welcome_channel_id
            FROM server
            WHERE id = {guild_id}
            """
        )
        value = self.cursor.fetchone()
        return value[0] if value is not None else None

    def set_welcome_channel_id(self, guild_id: int, welcome_channel_id: int | None) -> None:
        self.cursor.execute(
            f"""
            INSERT INTO server (id, welcome_channel_id)
            VALUES ({guild_id}, {welcome_channel_id or "NULL"})
            ON CONFLICT(id) DO UPDATE SET welcome_channel_id = {welcome_channel_id}
            """
        )
        self.db.commit()


db = Database()