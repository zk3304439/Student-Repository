"""Author:Yiyang Shi
   Program content:HW10: Continue to add new features to the student data repository
   Continue to add new features to the student data repository
"""
import unittest
from HW10_Yiyang_Shi import Repository


class RepositoryTest(unittest.TestCase):
    """test the Repository"""
    def test_Repository(self):
        """test the Repository"""
        t = Repository()
        self.assertIsNone(t.student())
        self.assertIsNone(t.instructor())


if __name__ == '__main__':
    unittest.main(exit=False, verbosity=2)