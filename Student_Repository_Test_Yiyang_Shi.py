"""Author:Yiyang Shi
   Program content:HW09: Creating a data repository of courses, students, and instructors
   Creating a data repository of courses, students, and instructors
"""
import unittest
from Student_Repository_Yiyang_Shi import Repository


class RepositoryTest(unittest.TestCase):
    """test the Repository"""
    def test_Repository(self):
        """test the Repository"""
        t = Repository()
        self.assertIsNone(t.student())
        self.assertIsNone(t.instructor())


if __name__ == '__main__':
    unittest.main(exit=False, verbosity=2)