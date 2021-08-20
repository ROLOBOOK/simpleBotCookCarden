import pymysql
import traceback

from config import HOST, USER, PASSWORD, DATEBASE


class DB:
    def __init__(self):
        """Подключаемся к базе, создаем курсов"""
        self.error = None
        try:
            self.db = pymysql.connect(host=HOST,
                                           user=USER,
                                           password=PASSWORD,
                                           database=DATEBASE
                                           )
            self.cursor = self.db.cursor()
        except (pymysql.err.OperationalError, pymysql.err.ProgrammingError, RuntimeError):
            self.error = traceback.format_exc()


    @property
    def close(self):
        self.db.close()

    def make_request(self, request):
        """Делаем запрос к базе"""
        try:
            if not self.error:
                self.cursor.execute(request)
                return self.cursor.fetchall()
            return None
        except :
            self.error = traceback.format_exc()
            return None


if __name__ == '__main__':
    db = DB()
    print(db.error)
    res = db.make_request('SELECT * FROM cookforcardendb.countforone;')
    print(res)
