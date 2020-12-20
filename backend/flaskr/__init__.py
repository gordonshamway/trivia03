import os
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import random

from models import setup_db, Question, Category

QUESTIONS_PER_PAGE = 10

def create_app(test_config=None):
  """Initializes the app, db and CORS
  """
  # create and configure the app
  app = Flask(__name__)
  setup_db(app)
  cors = CORS(app, resources={r"/*": {"origins": "*"}})

  @app.after_request
  def after_request(response):
    response.headers.add('Access-Control-Allow-Headers', 'Content-Type, Authorization, true')
    response.headers.add('Access-Control-Allow-Methods', 'GET,PATCH,POST,DELETE,OPTIONS')
    return response


  def paginate_questions(req, list_of_questions):
    """Paginate the requests of questions
    ARGS:
      req - request with page parameter (int)
      list_of_questions - list 
    RETURNS:
      a list of questions in the specific range
    """
    page = req.args.get('page', 1, type=int)
    start= (page - 1) * QUESTIONS_PER_PAGE
    end = start + QUESTIONS_PER_PAGE
    return list_of_questions[start:end]

  @app.route('/categories', methods=['GET'])
  def get_categories():
    """Endpoint to receive all categories (GET)
    ARGS:
      NONE
    RETURNS:
      Success - JSON with payload
      Error - JSON with error_message (404)
    """
    try:
      categories = Category.query.order_by(Category.id).all()
      some_list = []
      for c in categories:
        some_list.append(c.format())
      return jsonify({
        "success": True,
        "categories": some_list
        })
    except:
      pass
      abort(404)

  @app.route('/questions', methods=['GET'])
  def get_questions():
    """Endpoint to receive all questions (GET)
    ARGS:
      NONE
    RETURNS:
      Success - JSON with payload
      Error - JSON with error_message (404)
    """
    try:
      questions = Question.query.order_by(Question.id).all()
      current_questions = paginate_questions(request, questions)
      return jsonify({
        'success': True,
        'questions': [c.format() for c in current_questions],
        'total_questions': len(questions)
      })
    except:
      abort(404)

  @app.route('/questions/<int:question_id>', methods=['DELETE'])
  def delete_question(question_id):
    """Endpoint to delete a specific question (DELETE)
    ARGS:
      question_id - int
    RETURNS:
      Success - JSON with success message
      Error - JSON with error_message (422)
    """
    try:
      this_question = Question.query.filter_by(id=question_id).one_or_none()
      Question.delete(this_question)
      return jsonify ({
        'success': True,
        'message': 'Successfully deleted'
      })
    except:
      abort(422)

  @app.route('/questions', methods=['POST'])
  def create_question():
    """Endpoint to create a new question (POST)
    ARGS:
      JSON with payload
    RETURNS:
      Success - JSON with success message
      Error - JSON with error_message (422)
    """
    body = request.get_json()
    try:
      question = body.get('question', None)
      answer = body.get('answer', None)
      category = body.get('category', None)
      difficulty = body.get('difficulty', None)
      if None in [question, answer, category, difficulty]:
        raise
      this_question = Question(question=question, answer=answer, category=category, difficulty=difficulty)
      this_question.insert()

      return jsonify({
        'success': True,
        'message': 'Question successfully inserted'
      })
    except:
      print('in abort mode')
      abort(422)

  @app.route('/questions/search', methods=['POST'])
  def search_questions():
    """Endpoint to search for questions by question content (POST)
    ARGS:
      URL ARG title - string
    RETURNS:
      Success - JSON with list of found questions
      Error - JSON with error_message (422)
    """
    try:
      if not request.args['title']:
        raise
      search_term = request.args.get('title', None)
      q_string = f'%{search_term}%'
      found_questions = Question.query.filter(Question.question.ilike(q_string)).all()
      return jsonify({
        'success': True,
        'questions': [f.format() for f in found_questions]
      })
    except:
      abort(422)

  @app.route('/categories/<int:category_id>', methods=['GET'])
  def get_all_questions_per_category(category_id):
    """Endpoint to receive all questions by a category_id (GET)
    ARGS:
      category_id - int
    RETURNS:
      Success - JSON with list of questions in that given category
      Error - JSON with error_message (422)
    """
    try:
      all_questions_for_category = Question.query.order_by(Question.id).filter(Question.category == category_id).all()
      if not all_questions_for_category:
        abort(404)
      else:
        return jsonify({
          'success': True,
          'questions': [c.format() for c in all_questions_for_category]
        })
    except:
      abort(422)

  @app.route('/categories/<int:category_id>/play', methods=['POST'])
  def play_game(category_id):
    """Endpoint to receive questions for a category_id without blacklist (POST)
    ARGS:
      category_id - int
      JSON (previous_question) - list of backlist questions which we don´t wanted to return
    RETURNS:
      Success - JSON with list of questions
      Error - JSON with error_message (422)
    """
    try:
      body = request.get_json()
      previous_questions = body.get('previous_question', None)
      list_of_not_asked_questions = Question.query.filter(Question.category == category_id, ~Question.id.in_(previous_questions))
      return jsonify({
        'success': True,
        'list_of_questions_to_play': [i.format() for i in list_of_not_asked_questions]
      })
    except:
      abort(422)

  @app.errorhandler(400)
  def unprocessable(error):
    return jsonify({
      "success": False,
      "error": 400,
      "message": "Bad request"
    }),400

  @app.errorhandler(404)
  def not_found(error):
    return jsonify({
      "success": False,
      "error": 404,
      "message": "Resource not found"
    }),404

  @app.errorhandler(404)
  def not_found(error):
    return jsonify({
      "success": False,
      "error": 405,
      "message": "Method not allowed"
    }),405

  @app.errorhandler(422)
  def unprocessable(error):
    return jsonify({
      "success": False,
      "error": 422,
      "message": "Unprocessable"
    }),422

  @app.errorhandler(500)
  def unprocessable(error):
    return jsonify({
      "success": False,
      "error": 500,
      "message": "Server error"
    }),500
  return app