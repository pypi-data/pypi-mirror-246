import unittest
import random
import sys
import os
import pandas as pd

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import Training_Mgmt.Exercise.Exercise as E
import Training_Mgmt.Exercise.Record as R
import Training_Mgmt.Person.Person as P

class TestExercise(unittest.TestCase):

    def setUp(self):
        self.exercise1 = E.Exercise('medium', ['leg'])
        self.exercise2 = E.Exercise('easy', ['chest'])
        self.exercise3 = E.Exercise('hard', ['bicep','back'])
        self.exercise4 = E.Exercise('easy', ['tricep'])
    
    def test_set_intensity(self):
        self.exercise1.intensity_level = 'easy'
        self.assertEqual(self.exercise1.intensity_level, 'easy')

    def test_set_bodypart(self):
        self.exercise1.body_part = ['chest']
        self.assertEqual(self.exercise1.body_part, ['chest'])

    def test_cardio_suggestion(self):
        random.seed(1)
        self.assertEqual(self.exercise1.cardio_suggestion(), ('Rowing Machine', 40))
        self.assertEqual(self.exercise2.cardio_suggestion(), ('Indoor Cycling', 30))
        self.assertEqual(self.exercise3.cardio_suggestion(), ('Elliptical Trainer', 60))
        random.seed(2)
        self.assertEqual(self.exercise4.cardio_suggestion(), ('Running', 30))

    def test_strength_suggestion(self):
        random.seed(1)
        self.assertEqual(self.exercise1.strength_suggestion(), {'LEG PRESS [4*12]': 'https://www.youtube.com/watch?v=IZxyjW7MPJQ&pp=ygUJbGVnIHByZXNz',
                         'CALF RAISES [4*12]': 'https://www.youtube.com/watch?v=d2GgSoHvIXo&pp=ygULY2FsZiByYWlzZXM%3D',
                         'LEG CURL [4*12]': 'https://www.youtube.com/watch?v=ELOCsoDSmrg&pp=ygUIbGVnIGN1cmw%3D',
                         'LEG EXTENSION [4*12]': 'https://www.youtube.com/watch?v=ljO4jkwv8wQ&pp=ygUNbGVnIGV4dGVuc2lvbg%3D%3D',
                         'LEG PRESS [4*12]': 'https://www.youtube.com/watch?v=IZxyjW7MPJQ&pp=ygUJbGVnIHByZXNz',
                         'LUNGES [4*10]': 'https://www.youtube.com/shorts/yXVHr7wrleQ',
                         'SQUATS [5*6]': 'https://www.youtube.com/shorts/AIZ8q1qruKw'})
        random.seed(1)
        self.assertEqual(self.exercise2.strength_suggestion(), {'INCLINE BENCH PRESS [5*5]': 'https://www.youtube.com/watch?v=SrqOu55lrYU&pp=ygUTaW5jbGluZSBiZW5jaCBwcmVzcw%3D%3D',
                                                                'DIP PUSH UP [4*12]': 'https://www.youtube.com/watch?v=ybjGSN9IwaA&pp=ygULZGlwIHB1c2ggdXA%3D',
                                                                'BENCH PRESS [5*5]': 'https://www.youtube.com/watch?v=4Y2ZdHCOXok&pp=ygULYmVuY2ggcHJlc3M%3D',
                                                                'DUMBELL FLAT BENCH PRESS [4*10]': 'https://www.youtube.com/watch?v=QsYre__-aro&pp=ygUYZHVtYmVsbCBmbGF0IGJlbmNoIHByZXNz',
                                                                'PEC DECK FLYS [5*12]': 'https://www.youtube.com/shorts/g3T7LsEeDWQ'})
        random.seed(1)
        self.assertEqual(self.exercise3.strength_suggestion(), {'PREACHER CURL [4*15]': 'https://www.youtube.com/watch?v=fIWP-FRFNU0',
                                                                'HAMMER CURL [4*15]': 'https://www.youtube.com/watch?v=zC3nLlEvin4',
                                                                'CABLE CURL [4*15]': 'https://www.youtube.com/watch?v=NFzTWp2qpiE&pp=ygUKY2FibGUgY3VybA%3D%3D',
                                                                'BICEP CURL [4*15]': 'https://www.youtube.com/watch?v=ykJmrZ5v0Oo',
                                                                'BACK EXTENSION [4*10]': 'https://www.youtube.com/watch?v=ph3pddpKzzw&pp=ygUOYmFjayBleHRlbnNpb24%3D',
                                                                'SINGLE-ARM DUMBBELL ROW [4*10]': 'https://www.youtube.com/watch?v=roCP6wCXPqo&pp=ygUXc2luZ2xlLWFybSBkdW1iYmVsbCByb3c%3D',
                                                                'DEADLIFT [5*8]': 'https://www.youtube.com/watch?v=XxWcirHIwVo&pp=ygUIZGVhZGxpZnQ%3D'})
        random.seed(2)
        self.assertEqual(self.exercise4.strength_suggestion(), {'TRICEPS PUSHDOWN [4*15]': 'https://www.youtube.com/watch?v=2-LAMcpzODU',
                                                                'OVERHEAD TRICEPS EXTENSION [4*15]': 'https://www.youtube.com/watch?v=-Vyt2QdsR7E&pp=ygUab3ZlcmhlYWQgdHJpY2VwcyBleHRlbnNpb24%3D',
                                                                'TRICEPS OVERHEAD PRESS WITH DUMBBELL [4*15]': 'https://www.youtube.com/watch?v=-Vyt2QdsR7E&pp=ygUkdHJpY2VwcyBvdmVyaGVhZCBwcmVzcyB3aXRoIGR1bWJiZWxs',
                                                                'SKULL CRUSHERS [4*15]': 'https://www.youtube.com/watch?v=d_KZxkY_0cM&pp=ygUOc2t1bGwgY3J1c2hlcnM%3D',
                                                                'TRICEPS ROPE PUSHDOWN [4*15]': 'https://www.youtube.com/watch?v=kiuVA0gs3EI&pp=ygUVdHJpY2VwcyByb3BlIHB1c2hkb3du'})
        
    def test_hybrid_suggestion(self):
        random.seed(2)
        self.assertEqual(self.exercise1.hybrid_suggestion(), [{'SQUATS [5*6]': 'https://www.youtube.com/shorts/AIZ8q1qruKw',
                                                              'LUNGES [4*10]': 'https://www.youtube.com/shorts/yXVHr7wrleQ',
                                                              'WALL SIT [4*12]': 'https://www.youtube.com/watch?v=y-wV4Venusw',
                                                              'LEG PRESS [4*12]': 'https://www.youtube.com/watch?v=IZxyjW7MPJQ&pp=ygUJbGVnIHByZXNz'},
                                                              {'Rowing Machine': 30}])
        random.seed(5)
        self.assertEqual(self.exercise2.hybrid_suggestion(), [{'DIP PUSH UP [4*12]': 'https://www.youtube.com/watch?v=ybjGSN9IwaA&pp=ygULZGlwIHB1c2ggdXA%3D',
                                                               'DUMBELL FLAT BENCH PRESS [4*10]': 'https://www.youtube.com/watch?v=QsYre__-aro&pp=ygUYZHVtYmVsbCBmbGF0IGJlbmNoIHByZXNz',
                                                               'PEC DECK FLYS [5*12]': 'https://www.youtube.com/shorts/g3T7LsEeDWQ'},
                                                               {'Running': 15}])
        random.seed(8)
        self.assertEqual(self.exercise3.hybrid_suggestion(), [{'CONCENTRATION CURL [4*15]': 'https://www.youtube.com/watch?v=0AUGkch3tzc',
                                                               'REVERSE CURL [4*15]': 'https://www.youtube.com/watch?v=nRgxYX2Ve9w&pp=ygUMcmV2ZXJzZSBjdXJs',
                                                               'INCLINE DUMBBELL CURL [4*15]': 'https://www.youtube.com/watch?v=soxrZlIl35U',
                                                               'BENT-OVER ROW [4*10]': 'https://www.youtube.com/watch?v=FWJR5Ve8bnQ&pp=ygUNYmVudC1vdmVyIHJvdw%3D%3D',
                                                               'LAT PULLDOWN [4*12]': 'https://www.youtube.com/watch?v=SALxEARiMkw&pp=ygUMbGF0IHB1bGxkb3du'},
                                                               {'Running': 40}])
        random.seed(6)
        self.assertEqual(self.exercise4.hybrid_suggestion(), [{'REVERSE GRIP PUSHDOWN [4*15]': 'https://www.youtube.com/watch?v=o2HRy4ay4rE&pp=ygUVcmV2ZXJzZSBncmlwIHB1c2hkb3du',
                                                               'OVERHEAD TRICEPS EXTENSION [4*15]': 'https://www.youtube.com/watch?v=-Vyt2QdsR7E&pp=ygUab3ZlcmhlYWQgdHJpY2VwcyBleHRlbnNpb24%3D',
                                                               'TRICEPS ROPE PUSHDOWN [4*15]': 'https://www.youtube.com/watch?v=kiuVA0gs3EI&pp=ygUVdHJpY2VwcyByb3BlIHB1c2hkb3du'},
                                                               {'Elliptical Trainer': 15}])
        
    def test_strength_choices_helper(self):
        random.seed(9)
        self.assertEqual(self.exercise1.strength_choices_helper(5), {'SUMO SQUATS [5*6]': 'https://www.youtube.com/watch?v=9ZuXKqRbT9k',
                                                                     'CALF RAISES [4*12]': 'https://www.youtube.com/watch?v=d2GgSoHvIXo&pp=ygULY2FsZiByYWlzZXM%3D',
                                                                     'LEG CURL [4*12]': 'https://www.youtube.com/watch?v=ELOCsoDSmrg&pp=ygUIbGVnIGN1cmw%3D',
                                                                     'LUNGES [4*10]': 'https://www.youtube.com/shorts/yXVHr7wrleQ',
                                                                     'STEP-UPS [4*12]': 'https://www.youtube.com/watch?v=WCFCdxzFBa4&pp=ygUIc3RlcC11cHM%3D'})
        random.seed(1)
        self.assertEqual(self.exercise2.strength_choices_helper(2), {'INCLINE BENCH PRESS [5*5]': 'https://www.youtube.com/watch?v=SrqOu55lrYU&pp=ygUTaW5jbGluZSBiZW5jaCBwcmVzcw%3D%3D',
                                                                     'DIP PUSH UP [4*12]': 'https://www.youtube.com/watch?v=ybjGSN9IwaA&pp=ygULZGlwIHB1c2ggdXA%3D'})
        random.seed(5)
        self.assertEqual(self.exercise3.strength_choices_helper(4), {'ALTERNATE DUMBBELL CURL [4*15]': 'https://www.youtube.com/watch?v=sAq_ocpRh_I',
                                                                     'CABLE CURL [4*15]': 'https://www.youtube.com/watch?v=NFzTWp2qpiE&pp=ygUKY2FibGUgY3VybA%3D%3D',
                                                                     'SEATED CABLE ROW [4*10]': 'https://www.youtube.com/watch?v=GZbfZ033f74&pp=ygUQc2VhdGVkIGNhYmxlIHJvdw%3D%3D',
                                                                     'SINGLE-ARM DUMBBELL ROW [4*10]': 'https://www.youtube.com/watch?v=roCP6wCXPqo&pp=ygUXc2luZ2xlLWFybSBkdW1iYmVsbCByb3c%3D'})
        random.seed(6)
        self.assertEqual(self.exercise4.strength_choices_helper(1), {'REVERSE GRIP PUSHDOWN [4*15]': 'https://www.youtube.com/watch?v=o2HRy4ay4rE&pp=ygUVcmV2ZXJzZSBncmlwIHB1c2hkb3du'})

    def tearDown(self) -> None:
        return super().tearDown()

