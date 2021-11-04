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
        self.database_path = "postgres://student:student@{}/{}".format('localhost:5432', self.database_name)
        setup_db(self.app, self.database_path)

        self.val_question = {'question':'Which is the most popular sport?','answer':'Soccer','category':'6','diffuculty':1}
        self.bad_question = {'question':'Which is the most popular sport?','answer':'Soccer','category':"Sports",'diffuculty':"low"}

        # binds the app to the current context
        with self.app.app_context():
            self.db = SQLAlchemy()
            self.db.init_app(self.app)
            # create all tables
            self.db.create_all()
    
    def tearDown(self):
        """Executed after reach test"""
        pass
    
    def test_get_categories(self):
        res = self.client().get("/categories")
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertTrue(bool(data['categories']))
        self.assertIn('Sports',data['categories'].values())

    def test_get_questions_by_page(self):
        res = self.client().get("/questions?page=1")
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertGreater(data['total_questions'],0)
        self.assertIn(data['current_category'],data['categories'].values())

    def test_add_question(self):
        res = self.client().post("/questions", json=self.val_question)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)

    def test_404_get_questions_by_page(self):
        res = self.client().get("/questions?page=100")
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data["message"], "resource not found")

    def test_404_get_questions_by_category(self):
        res = self.client().get("/categories/100/questions")
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data["message"], "resource not found")

    def test_422_add_question_unprocessable(self):
        res = self.client().post("/questions", headers={'Content-Type':'application/json'}, data=json.dumps(self.bad_question))
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 422)
        self.assertEqual(data["message"], "unprocessable")

    def test_500_add_question_error(self):
        res = self.client().post("/questions", data=json.dumps({}))
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 500)
        self.assertEqual(data["message"], "internal error, unable to fulfil request")

    
# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()