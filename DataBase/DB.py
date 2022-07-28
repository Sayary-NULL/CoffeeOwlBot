import sqlite3 as sl
from loguru import logger


class DB:
    def __init__(self, file_name):
        self.str_connect = f'file:{file_name}'

        if not self.test_connect():
            logger.error(f'К бд нет доступа: {self.str_connect}')
            raise NameError("к бд нет доступа")

    def test_connect(self) -> bool:
        try:
            sl.connect(self.str_connect, uri=True)
            return True
        except sl.OperationalError:
            return False

    def get_open_cursor(self):
        con = sl.connect(self.str_connect, uri=True)
        return con, con.cursor()

    def get_channel_status(self, channel_id: int):
        con, cur = self.get_open_cursor()
        cur.execute("""select * from channel where channel_id = ?""", (channel_id, ))
        return cur.fetchone()

    def set_channel_status(self, channel_id: int,
                           is_base: bool = False,
                           is_command: bool = False,
                           is_admin: bool = False,
                           is_test: bool = False):
        con, cur = self.get_open_cursor()
        cur.execute("""insert into channel values (?,?,?,?,?)""", (channel_id, is_admin, is_base, is_test, is_command))
        con.commit()

    def update_channel_status(self, channel_id: int,
                              is_base: bool = False,
                              is_command: bool = False,
                              is_admin: bool = False,
                              is_test: bool = False):
        con, cur = self.get_open_cursor()
        cur.execute("""update channel set is_admin = ?, is_base = ?, is_test = ?, is_command = ? where channel_id = ?""",
                    (is_admin, is_base, is_test, is_command, channel_id))
        con.commit()