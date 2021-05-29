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
        self.database_name = "trivia_test"
        self.database_path = "postgres://postgres:postgres@{}/{}".format(
            'localhost:5433', self.database_name)
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
    Write at least one test for each test for successful operation and for expected errors.
    """

    def test_get_categories(self):
        """" gets categories using /categories endpoint"""
        res = self.client().get('/categories')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(len(data['categories']))

    def test_get_questions_no_page(self):
        """" gets questions using /questions endpoint without a page argument"""
        res = self.client().get('/questions')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['total_questions'])
        self.assertTrue(len(data['list_of_questions']))
        self.assertTrue(len(data['categories']))

    def test_get_questions_valid_page(self):
        """" gets questions using /questions endpoint without a page argument"""
        res = self.client().get('/questions?page=2')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['total_questions'])
        self.assertTrue(len(data['list_of_questions']))
        self.assertTrue(len(data['categories']))

    def test_get_questions404(self):
        """requests a page beyond the range of pages"""
        res = self.client().get('/questions?page=10000')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'Not Found')

    def test_create_question(self):
        """Apply MCDC on the data required to create a question"""

        # 1) request creation with valid data
        new_question = {'question': "new question",
                        'answer': 'answer', 'difficulty': 1, 'category': 1}
        res = self.client().post('/questions', json=new_question)
        data = json.loads(res.data)
        # get the last inserted question
        inserted_question = Question.query.order_by(
            self.db.desc(Question.id)).first()
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(data['question_created'], inserted_question.id)
        self.assertTrue(data['total_questions'])
        self.assertTrue(len(data['questions']))

        # 2) request creation with no question provided
        new_question = {'answer': 'answer', 'difficulty': 1, 'category': 1}
        res = self.client().post('/questions', json=new_question)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 422)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'Unprocessable')

        # 3) request creation with no answer provided
        new_question = {'question': 'new question',
                        'difficulty': 1, 'category': 1}
        res = self.client().post('/questions', json=new_question)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 422)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'Unprocessable')

        # 4) request creation with no difficulty provided
        new_question = {'answer': 'answer',
                        'question': 'new question', 'category': 1}
        res = self.client().post('/questions', json=new_question)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 422)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'Unprocessable')

        # 5) request creation with no category provided
        new_question = {'answer': 'answer',
                        'difficulty': 1, 'question': 'new question'}
        res = self.client().post('/questions', json=new_question)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 422)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'Unprocessable')
        pass

    def test_delete_question(self):
        """request a valid question deletion"""
        question = Question.query.order_by(self.db.desc(Question.id)).first()
        self.assertNotEqual(question, None)
        question_id = question.id
        res = self.client().delete('/questions/'+str(question_id))
        data = json.loads(res.data)
        question = Question.query.get(question_id)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(data['question_deleted'], question_id)
        self.assertTrue(len(data['questions']))
        self.assertTrue(data['total_questions'])
        self.assertEqual(question, None)

    def test_delete_question404(self):
        """request a delete with unknown id"""
        res = self.client().delete('/questions/12233')
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'Not found.')

    def test_search_question_with_results(self):
        """searches questions with existing results"""
        res = self.client().post('/questions', json={'search': 'the'})
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['total_questions'])
        self.assertTrue(len(data['questions']))

    def test_search_question_with_noresults(self):
        """searches questions with no results"""
        res = self.client().post(
            '/questions', json={'search': 'dsfldjsfkrwekrljfdsfjk'})
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(data['total_questions'], 0)
        self.assertEqual(len(data['questions']), 0)


# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()
