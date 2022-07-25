import sqlite3 as sl


class DB:
    def __init__(self, file_name):
        self.str_connect = f'file:{file_name}'

        if not self.test_connect():
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
