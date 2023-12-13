import unittest
import sys
import os
import pandas as pd

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import Training_Mgmt.Exercise.Record as R
import Training_Mgmt.Person.Person as P

class TestRecord(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.record = R.Record(P.Person("Gevin", "2000-01-01", 174, 66, "Male", "Bulking", "Very active"))

    def test_add(self):
        self.record.add([{'date': "2023-12-01", 'exercise_name': 'leg', 'exercise_set': 5, 'exercise_rep': 10}])
        self.record.add([{'date': "2023-12-02", 'exercise_name': 'chest', 'exercise_set': 3, 'exercise_rep': 12}])
        self.record.add([{'date': "2023-12-03", 'exercise_name': 'bicep', 'exercise_set': 6, 'exercise_rep': 8}])
        self.record.add([{'date': "2023-12-04", 'exercise_name': 'shoulder', 'exercise_set': 2, 'exercise_rep': 20}])
        df = pd.read_csv("Gevin_exercise.csv")
        date = df.at[0,'date']
        exercise_name = df.at[0, 'exercise_name']
        exercise_set = df.at[0,'exercise_set']
        exercise_rep = df.at[0,'exercise_rep']
        self.assertEqual(date, "2023-12-01")
        self.assertEqual(exercise_name, 'leg')
        self.assertEqual(exercise_set, 5)
        self.assertEqual(exercise_rep, 10)

    def test_remove_by_index(self):
        self.record.remove_by_index(1)
        df = pd.read_csv("Gevin_exercise.csv")
        date = df.at[1,'date']
        exercise_name = df.at[1, 'exercise_name']
        exercise_set = df.at[1,'exercise_set']
        exercise_rep = df.at[1,'exercise_rep']
        self.assertEqual(date, "2023-12-03")
        self.assertEqual(exercise_name, 'bicep')
        self.assertEqual(exercise_set, 6)
        self.assertEqual(exercise_rep, 8)
        self.assertEqual(self.record.remove_by_index(100), None)

    def test_modify(self):
        self.record.modify(2, {"exercise_name": 'back', "exercise_set": 100, "exercise_rep": 200})
        df = pd.read_csv("Gevin_exercise.csv")
        date = df.at[2,'date']
        exercise_name = df.at[2, 'exercise_name']
        exercise_set = df.at[2,'exercise_set']
        exercise_rep = df.at[2,'exercise_rep']
        self.assertEqual(date, "2023-12-04")
        self.assertEqual(exercise_name, 'back')
        self.assertEqual(exercise_set, 100)
        self.assertEqual(exercise_rep, 200)
        self.assertEqual(self.record.modify(100,{"exercise_name": 'back', "exercise_set": 100, "exercise_rep": 200}), None)

    @classmethod
    def tearDownClass(cls):
        return 