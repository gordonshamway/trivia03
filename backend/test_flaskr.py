import os
import unittest
import json
from flask_sqlalchemy import SQLAlchemy

from flaskr import create_app
from models import setup_db, Question, Category


class TriviaTestCase(unittest.TestCase):
    """This class represents the trivia test case"""

    def setUp(self):
        """Define test variables and initialize app."""
        self.app = create_app()
        self.client = self.app.test_client
        self.database_name = "trivia"
        self.username = os.environ.get('TEST_USERNAME')
        self.password = os.environ.get('TEST_PASSWORD')
        self.server = os.environ.get('TEST_SERVER')
        self.port = os.environ.get('TEST_PORT')
        self.database_path = "postgres://{}:{}@{}:{}/{}".format(self.username, self.password, self.server, self.port, self.database_name)
        setup_db(self.app, self.database_path)

        # binds the app to the current context
        with self.app.app_context():
            self.db = SQLAlchemy()
            self.db.init_app(self.app)
            # create all tables
            self.db.create_all()
    
    def tearDown(self):
        """Executed after reach test"""
        pass

    """
    TODO
    Write at least one test for each test for successful operation and for expected errors.
    """
    def test_get_categories_success(self):
        golden_categories = [{'id': 1, 'type': 'Science'}, {'id': 2, 'type': 'Art'}, {'id': 3, 'type': 'Geography'}, {'id': 4, 'type': 'History'}, {'id': 5, 'type': 'Entertainment'}, {'id': 6, 'type': 'Sports'}]
        
        res = self.client().get('/categories')
        res_payload = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(res_payload['success'], True)
        self.assertEqual(res_payload['categories'], golden_categories)

    def test_post_categories_failure(self):
        res = self.client().post('/categories')
        self.assertEqual(res.status_code, 405)
    
    def test_get_questions_success(self):
        res = self.client().get('/questions')
        res_payload = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(res_payload['success'], True)
        self.assertEqual(res_payload['total_questions'], 18)

    def test_post_questions_failure(self):
        res = self.client().post('/questions')
        self.assertEqual(res.status_code, 422)
    
    def test_get_question_delete_success(self):
        res = self.client().delete('/questions/2')
        res_payload = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(res_payload['success'], True)
        self.assertEqual(res_payload['message'], 'Successfully deleted')
    
    def test_get_question_delete_failure(self):
        res = self.client().delete('/questions/2000')
        res_payload = json.loads(res.data)
        self.assertEqual(res.status_code, 422)
        self.assertEqual(res_payload['success'], False)
        self.assertEqual(res_payload['message'], 'Unprocessable')
    
    def test_post_new_questions_success(self):
        headers = {'Content-type': 'application/json'}
        test_data = {'question': 'How much is the fish?', 'answer': '12,50€', 'category': 3, 'difficulty': 2}
        res = self.client().post('/questions', json=test_data, headers=headers)
        res_payload = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(res_payload['success'], True)
        self.assertEqual(res_payload['message'], 'Question successfully inserted')

    def test_post_new_questions_failure(self):
        test_data = {'question': 'How much is the fish?', 'answer': '12,50€', 'category': 3, 'difficulteee': 2}
        headers = {'Content-type': 'application/json'}
        res = self.client().post('/questions', json=test_data, headers=headers)
        res_payload = json.loads(res.data)
        self.assertEqual(res.status_code, 422)
        self.assertEqual(res_payload['success'], False)
        self.assertEqual(res_payload['message'], 'Unprocessable')

    def test_post_question_search_success(self):
        res = self.client().post('/questions/search?title=how')
        res_payload = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(res_payload['success'], True)
        self.assertGreaterEqual(len(res_payload['questions']), 1)

    def test_post_question_search_failure(self):
        res = self.client().post('/questions/search?titlleee=how')
        res_payload = json.loads(res.data)
        self.assertEqual(res.status_code, 422)
        self.assertEqual(res_payload['success'], False)
        self.assertEqual(res_payload['message'], 'Unprocessable')

    def test_get_all_questions_per_category_success(self):
        res = self.client().get('/categories/1')
        res_payload = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(res_payload['success'], True)
        self.assertGreater(len(res_payload['questions']),1)

    def test_get_all_questions_per_category_failure(self):
        res = self.client().get('/categories/666')
        res_payload = json.loads(res.data)
        self.assertEqual(res.status_code, 422)
        self.assertEqual(res_payload['success'], False)

    def test_post_play_success(self):
        prev_question = {'previous_question': [1,2,3,4]}
        headers = {'Content-type': 'application/json'}
        res = self.client().post('/categories/1/play', json=prev_question, headers=headers)
        res_payload = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(res_payload['success'], True)
        self.assertGreater(len(res_payload['list_of_questions_to_play']),1)

    def test_post_play_failure(self):
        prev_question = {'previous_questionzzzz': [1,2,3,4]}
        headers = {'Content-type': 'application/json'}
        res = self.client().post('/categories/1/play', json=prev_question, headers=headers)
        res_payload = json.loads(res.data)
        self.assertEqual(res.status_code, 422)
        self.assertEqual(res_payload['success'], False)
        self.assertEqual(res_payload['message'], 'Unprocessable')

# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()