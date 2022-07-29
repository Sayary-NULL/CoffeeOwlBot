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

    def get_trigger_form_text(self, message: str = None):
        con, cur = self.get_open_cursor()
        if message is not None:
            cur.execute(f"""select text_response from "trigger" where text_request == ?""", (message, ))
        else:
            cur.execute(f"""select trigger_id, text_request, text_response from "trigger" """)
        return cur.fetchall()

    def set_trigger(self, text_request: str, text_response: str):
        con, cur = self.get_open_cursor()
        cur.execute("""insert into "trigger" (text_request, text_response) values (?, ?)""",
                    (text_request, text_response))
        con.commit()

    def del_trigger(self, id_trigger):
        con, cur = self.get_open_cursor()
        cur.execute("""delete from "trigger" where trigger_id = ?""", (id_trigger, ))
        con.commit()
