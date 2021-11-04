import os
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import random

from models import setup_db, db, Question, Category

QUESTIONS_PER_PAGE = 10

def paginate_questions(request, selection):
    page = request.args.get("page", 1, type=int)
    start = (page - 1) * QUESTIONS_PER_PAGE
    end = start + QUESTIONS_PER_PAGE

    questions = [question.format() for question in selection]
    current_questions = questions[start:end]

    return current_questions

def create_app(test_config=None):
  # create and configure the app
  app = Flask(__name__)
  setup_db(app)
  CORS(app)

  # CORS Headers
  @app.after_request
  def after_request(response):
      response.headers.add(
          "Access-Control-Allow-Headers", "Content-Type,Authorization,true"
      )
      response.headers.add(
          "Access-Control-Allow-Methods", "GET,POST,DELETE,OPTIONS"
      )
      return response

  @app.route('/categories', methods=['GET'])
  def get_categories():
    categories = Category.query.order_by(Category.id).all()
    data = {}
    for category in categories:
      data[category.id] = category.type

    return jsonify(
      {
        'categories':data
      }
    )

  @app.route('/questions', methods=['GET'])
  def get_questions_by_page():
    questions = Question.query.order_by(Question.id).all()
    categories = Category.query.order_by(Category.id).all()

    current_questions = paginate_questions(request, questions)

    if len(current_questions) == 0:
      abort(404)

    data = {}
    for category in categories:
      data[category.id] = category.type

    current_category = data[current_questions[0]['category']]

    return jsonify(
      {
        'questions':current_questions,
        'total_questions':len(questions),
        'categories':data,
        'current_category':current_category
      }
    )

  @app.route('/categories/<int:id>/questions', methods=['GET'])
  def get_questions_by_category(id):
    questions = db.session.query(Question, Category)\
      .join(Category, Category.id==id)\
      .filter(Question.category == id).all()

    if len(questions) == 0:
      abort(404)

    formatted_questions = [q.format() for q, _ in questions]
    current_category = questions[0][1].format()

    return jsonify(
      {
        'questions':formatted_questions,
        'total_questions':len(questions),
        'current_category':current_category['type']
      }
    )
  
  @app.route('/questions', methods=['POST'])
  def add_question():
    body = request.get_json()
    question = body.get("question")
    answer = body.get("answer")
    difficulty = body.get("difficulty")
    category = body.get("category")

    try:
      new_question = Question(question,answer,category,difficulty)
      new_question.insert()
      return jsonify({'success':True})

    except:
      abort(422)

  @app.route('/questions/<int:id>', methods=['DELETE'])
  def delete_question(id):
    question = Question.query.get(id)

    if question !=None:
      question.delete()
      return jsonify({'success':True, 'id':question.id})

    else:
      abort(404)

  @app.route('/questions/search', methods=['POST'])
  def get_questions_by_term():
    body = request.get_json()
    term = '%'+body.get("searchTerm")+'%'

    questions = db.session.query(Question, Category)\
      .join(Category, Category.id==Question.category)\
      .filter(Question.question.ilike(term)).all()

    if len(questions) == 0:
      abort(404)

    formatted_questions = [q.format() for q, _ in questions]
    current_category = questions[0][1].format()

    return jsonify(
      {
        'questions':formatted_questions,
        'total_questions':len(questions),
        'current_category':current_category['type']
      }
    )

  @app.route('/quizzes', methods=['POST'])
  def play_quiz():
    body = request.get_json()
    previous_questions = body.get("previous_questions")
    category_id = body.get("quiz_category")['id']

    if category_id == 0:
      questions_query = Question.query.all()
    else:
      questions_query = Question.query.filter_by(category=category_id).all()

    questions = [q.format() for q in questions_query]
    question = questions[0]

    while len(questions) > 0:
      random.shuffle(questions)
      q = questions.pop()
      if q['id'] not in previous_questions:
        question = q
        break

    return jsonify(
      {
        'question':question
      })

  @app.errorhandler(404)
  def not_found(error):
      return (
        jsonify({"success": False, "error": 404, "message": "resource not found"}),
        404
      )

  @app.errorhandler(422)
  def unprocessable(error):
      return (
          jsonify({"success": False, "error": 422, "message": "unprocessable"}),
          422
      )

  @app.errorhandler(400)
  def bad_request(error):
      return (
        jsonify({"success": False, "error": 400, "message": "bad request"}), 
        400
      )

  @app.errorhandler(500)
  def bad_request(error):
      return (
        jsonify({"success": False, "error": 500, "message": "internal error, unable to fulfil request"}), 
        500
      )
  
  return app

    