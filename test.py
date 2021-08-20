import unittest
from bd import DB


class TestConnectBD(unittest.TestCase):
    def test_status_connect_db(self):
        db = DB()
        self.assertIsNone(db.error)


if __name__ == '__main__':
    unittest.main()
