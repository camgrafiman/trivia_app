import os
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import random

from models import setup_db, Question, Category
from helpers import paginate, hasNextPage

QUESTIONS_PER_PAGE = 10


def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__)
    setup_db(app)

    '''
  @DONETODO: Set up CORS. Allow '*' for origins. Delete the sample route after completing the TODOs
  '''
    CORS(app, resources={r"/*": {"origins": "*"}})

    '''
  @DONETODO: Use the after_request decorator to set Access-Control-Allow
  '''
    # CORS Headers:
    @app.after_request
    def after_request(response):
        # response.headers.add('Access-Control-Allow-Origin', '*')
        response.headers.add('Access-Control-Allow-Headers',
                             'Content-Type, Authorization, true')
        response.headers.add('Access-Control-Allow-Methods',
                             'GET, PATCH, POST, DELETE, OPTIONS')
        response.headers.add('Access-Control-Allow-Credentials', 'true')
        return response

    ''' 
Index route
@DOCUMENTED!
    '''
    # Added the / index endpoint for the api:
    @app.route("/")
    def index():
        questions = Question.query.all()
        categories = Category.query.all()

        return jsonify({
            'questions': request.url_root + 'questions',
            'categories': request.url_root + 'categories',
            'total_questions': len(questions),
            'total_categories': len(categories)
        })

    '''
  @DONETODO:
  Create an endpoint to handle GET requests
  for all available categories.
  @DOCUMENTED!
  '''
    @app.route("/categories", methods=['GET'])
    def categories():

        try:
            categories = Category.query.all()

            return jsonify({
                'categories': [c.format() for c in categories],
                'success': True
            })
        except:
            abort(404)

    '''
  @DONETODO:
  Create an endpoint to handle GET requests for questions,
  including pagination (every 10 questions).
  This endpoint should return a list of questions,
  number of total questions, current category, categories.

  TEST: At this point, when you start the application
  you should see questions and categories generated,
  ten questions per page and pagination at the bottom of the screen for three pages.
  Clicking on the page numbers should update the questions.
  @DOCUMENTED!
  '''
    @app.route("/questions", methods=['GET'])
    def questions():
        all_questions = Question.query.order_by(Question.id).all()
        current_questions = paginate(
            request, all_questions, QUESTIONS_PER_PAGE)

        categories = Category.query.order_by(Category.id).all()

        restant_pages = len(all_questions) % QUESTIONS_PER_PAGE

        if len(current_questions) == 0:
            abort(404)

        return jsonify({
            'success': True,
            'list_of_questions': current_questions,
            'total_questions': len(all_questions),
            'categories': [category.format() for category in categories],
            'items_per_page': QUESTIONS_PER_PAGE,
            'next_page': hasNextPage(len(current_questions), request, restant_pages)
        })

    '''
  @DONETODO:
  Create an endpoint to DELETE question using a question ID.

  TEST: When you click the trash icon next to a question, the question will be removed.
  This removal will persist in the database and when you refresh the page.
  @DOCUMENTED!
  '''
    @app.route("/questions/<int:id>", methods=['DELETE'])
    def delete_question(id):
        question = Question.query.get(id)
        if question is None:
            abort(404)

        question.delete()
        new_list_questions = Question.query.order_by(Question.id).all()
        # print(new_list_questions)

        return jsonify({
            'success': True,
            'question_deleted': id,
            'questions': [question.format() for question in new_list_questions]
        })

    '''
  @DONETODO:
  Create an endpoint to POST a new question,
  which will require the question and answer text,
  category, and difficulty score.

  TEST: When you submit a question on the "Add" tab,
  the form will clear and the question will appear at the end of the last page
  of the questions list in the "List" tab.

  @DONETODO:
  Create a POST endpoint to get questions based on a search term.
  It should return any questions for whom the search term
  is a substring of the question.

  TEST: Search by any phrase. The questions list will update to include
  only question that include that string within their question.
  Try using the word "title" to start.
  @DOCUMENTED!
  '''

    @app.route("/questions", methods=['POST'])
    def add_question():
        data_new_question = request.get_json()
        search = request.args.get('search', None)
        # print(data_new_question)

        try:

            if search is None:

                if data_new_question is None:
                    abort(400)

                new_question = Question(
                    question=data_new_question['question'],
                    answer=data_new_question['answer'],
                    category=data_new_question['category'],
                    difficulty=data_new_question['difficulty']
                )
                new_question.insert()

                questions = Question.query.order_by(Question.id).all()
                current_questions = paginate(
                    request, questions, QUESTIONS_PER_PAGE)

                # print(new_question.format())
                # print(new_question.id)
                # new_question.insert()
                return jsonify({
                    'success': True,
                    'question_created': new_question.id,
                    'questions': current_questions,
                    'total_questions': len(questions),
                    'search': search
                })

            else:
                print("SEARCHED WORD" + search)
                print(len(search))
                if (len(search) == 0 or search == "" or search is None):
                    print("hast aqui")
                    questions = Question.query.order_by(Question.id).all()
                    current_questions = paginate(
                        request, questions, QUESTIONS_PER_PAGE)
                    return jsonify({
                        'success': True,
                        'questions': current_questions,
                        'total_questions': len(questions),
                        'search': None
                    })
                else:
                    questions = Question.query.order_by(Question.id).all()
                    # Search values:
                    questions_filtered = Question.query.order_by(Question.id).filter(
                        Question.question.ilike('%{}%'.format(search))).all()
                    current_questions = paginate(
                        request, questions_filtered, QUESTIONS_PER_PAGE)

                    return jsonify({
                        'success': True,
                        'questions': current_questions,
                        'total_questions': len(questions),
                        'search': search
                    })
        except:
            abort(422)

    '''
  @DONETODO: 
  Create a GET endpoint to get questions based on category. 

  TEST: In the "List" tab / main screen, clicking on one of the 
  categories in the left column will cause only questions of that 
  category to be shown. 
  @DOCUMENTED!
  '''
    @app.route("/categories/<int:category_id>/questions", methods=['GET'])
    def questions_by_category(category_id):
        category = Category.query.get(category_id)
        if category is None:
            abort(404)
        questions_filtered = Question.query.order_by(
            Question.id).filter(Question.category == category_id).all()

        paginated_filtered_questions = paginate(
            request, questions_filtered, QUESTIONS_PER_PAGE)

        return jsonify({
            'success': True,
            'questions': paginated_filtered_questions,
            'total_questions': len(questions_filtered),
            'current_category': category_id
        })

    '''
  @DONETODO: 
  Create a POST endpoint to get questions to play the quiz. 
  This endpoint should take category and previous question parameters 
  and return a random questions within the given category, 
  if provided, and that is not one of the previous questions. 

  TEST: In the "Play" tab, after a user selects "All" or a category,
  one question at a time is displayed, the user is allowed to answer
  and shown whether they were correct or not. 
  @DOCUMENTED!
  '''

    @app.route("/quizzes", methods=['POST'])
    def get_quizzes():
        body = request.get_json()
        try:
            prev_questions = body.get('previous_questions')

            quiz_category = body.get('quiz_category')['id']

            if (prev_questions is None):
                abort(400)

            questions = []
            if quiz_category == 0:
                questions = Question.query.filter(
                    Question.id.notin_(prev_questions)).all()
            else:
                category = Category.query.get(quiz_category)
                if category is None:
                    abort(404)
                questions = Question.query.filter(Question.id.notin_(
                    prev_questions), Question.category == quiz_category).all()
            current_question = None
            if (len(questions) > 0):
                index = random.randrange(0, len(questions))
                current_question = questions[index].format()
            return jsonify({
                'success': True,
                'question': current_question,
                'total_questions': len(questions)
            })

        except:
            abort(400)

    '''
  @DONETODO: 
  Create error handlers for all expected errors 
  including 404 and 422. 
  @DOCUMENTED!
  '''

    @app.errorhandler(404)
    def not_found(error):
        return jsonify({
            'success': False,
            'error': 404,
            'message': 'Not found.'
        }), 404

    @app.errorhandler(403)
    def forbidden(error):
        return jsonify({
            'success': False,
            'error': 403,
            'message': 'Forbidden'
        }), 403

    @app.errorhandler(422)
    def unprocessable(error):
        return jsonify({
            'success': False,
            'error': 422,
            'message': 'Unprocessable'
        }), 422
    # Added the 400 Error Bad request:
    @app.errorhandler(400)
    def bad_request(error):
        return jsonify({
            'success': False,
            'error': 400,
            'message': 'Bad request'
        }), 400

    @app.errorhandler(500)
    def internal_error(error):
        return jsonify({
            'success': False,
            'error': 500,
            'message': 'Internal server error.'
        }), 500

    @app.errorhandler(502)
    def bad_gateway(error):
        return jsonify({
            'success': False,
            'error': 502,
            'message': 'Bad gateway.'
        }), 502

    @app.errorhandler(503)
    def service_unavailable(error):
        return jsonify({
            'success': False,
            'error': 503,
            'message': 'Service unavailable'
        }), 503

    @app.errorhandler(504)
    def gateway_out(error):
        return jsonify({
            'success': False,
            'error': 504,
            'message': 'Gateway timed out'
        }), 504

    return app
