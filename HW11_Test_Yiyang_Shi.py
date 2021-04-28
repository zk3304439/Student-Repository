"""Author:Yiyang Shi
   Program content:HW11: database
   database solution in sql
"""
import unittest
from HW11_Yiyang_Shi import Repository


class RepositoryTest(unittest.TestCase):
    """test the Repository"""
    def test_Repository(self):
        """test the Repository"""
        t = Repository()
        self.assertIsNone(t.student())
        self.assertIsNone(t.instructor())
        self.assertIsNone(t.student_grades_table_db("810_startup.db"))


if __name__ == '__main__':
    unittest.main(exit=False, verbosity=2)