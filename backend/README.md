## Backend - Full Stack Trivia API 

### Installing Dependencies for the Backend

1. **Python 3.7** - Follow instructions to install the latest version of python for your platform in the [python docs](https://docs.python.org/3/using/unix.html#getting-and-installing-the-latest-version-of-python)


2. **Virtual Enviornment** - We recommend working within a virtual environment whenever using Python for projects. This keeps your dependencies for each project separate and organaized. Instructions for setting up a virual enviornment for your platform can be found in the [python docs](https://packaging.python.org/guides/installing-using-pip-and-virtual-environments/)


3. **PIP Dependencies** - Once you have your virtual environment setup and running, install dependencies by naviging to the `/backend` directory and running:
```bash
pip install -r requirements.txt
```
This will install all of the required packages we selected within the `requirements.txt` file.


4. **Key Dependencies**
 - [Flask](http://flask.pocoo.org/)  is a lightweight backend microservices framework. Flask is required to handle requests and responses.

 - [SQLAlchemy](https://www.sqlalchemy.org/) is the Python SQL toolkit and ORM we'll use handle the lightweight sqlite database. You'll primarily work in app.py and can reference models.py. 

 - [Flask-CORS](https://flask-cors.readthedocs.io/en/latest/#) is the extension we'll use to handle cross origin requests from our frontend server. 

### Database Setup
With Postgres running, restore a database using the trivia.psql file provided. From the backend folder in terminal run:
```bash
psql trivia < trivia.psql
```

### Running the server

From within the `./src` directory first ensure you are working using your created virtual environment, example './venv' directory.

### How to Start environment example (windows):
```
python -m venv venv
.\venv\Scripts\activate.bat
```

### Install python libraries:
```
pip install -r requirements.txt
```

### Install the database in local with database username example (running in port 5433 and using custom User):
```
psql -h localhost -p 5433 -U Alejandro trivia < trivia.psql
```
Enter your password and here you go!

To run the server, execute:

```command line
set FLASK_APP=flaskr
set FLASK_ENV=development
set FLASK_DEBUG=true
flask run
```

Setting the `FLASK_ENV` variable to `development` will detect file changes and restart the server automatically.
Setting the `FLASK_APP` variable to `flaskr` tells flask to use the `flaskr` directory to use the `__init__.py` file to find the application. 

If you use the `flask run --reload` flag will detect file changes and restart the server automatically, otherwise you can set FLASK_DEBUG=true and it will do the same.

## ToDo Tasks

One note before you delve into your tasks: for each endpoint you are expected to define the endpoint and response data. The frontend will be a plentiful resource because it is set up to expect certain endpoints and response data formats already. You should feel free to specify endpoints in your own way; if you do so, make sure to update the frontend or you will get some unexpected behavior. 

1. Use Flask-CORS to enable cross-domain requests and set response headers. 
2. Create an endpoint to handle GET requests for questions, including pagination (every 10 questions). This endpoint should return a list of questions, number of total questions, current category, categories. 
3. Create an endpoint to handle GET requests for all available categories. 
4. Create an endpoint to DELETE question using a question ID. 
5. Create an endpoint to POST a new question, which will require the question and answer text, category, and difficulty score. 
6. Create a POST endpoint to get questions based on category. 
7. Create a POST endpoint to get questions based on a search term. It should return any questions for whom the search term is a substring of the question. 
8. Create a POST endpoint to get questions to play the quiz. This endpoint should take category and previous question parameters and return a random questions within the given category, if provided, and that is not one of the previous questions. 
9. Create error handlers for all expected errors including 400, 404, 422 and 500. 


## API Reference

### Getting Started
- Base URL: this app is hosted locally at `http://127.0.0.1:5000/`, which is set as a proxy in the frontend configuration. 
- Authentication: no authentication required. 

### Error Handling
Errors are returned as JSON objects:
```
{
    "success": False, 
    "error": 404,
    "message": "Not Found."
}
```
returned error codes:
- 400: Bad Request
- 403: Forbidden
- 404: Not Found
- 422: Unprocessable
- 500: Internal Server Error
- 502: Bad Gateway
- 503: Service unavailable
- 504: Gateway timed out

### Endpoints 
### GET / 
- General:
    - Returns the urls for "categories" and "questions" and their total number
- Sample: `curl http://127.0.0.1:5000`

``` 
{
  "categories": "http://127.0.0.1:5000/categories",
  "questions": "http://127.0.0.1:5000/questions",
  "total_categories": 6,
  "total_questions": 26
}
```
#### GET /categories
- General:
    - Returns  categories as a List of dictionaries and success value
- Sample: `curl http://127.0.0.1:5000/categories`

``` 
{
  "categories": [
    {
      "id": 1,
      "type": "Science"
    },
    {
      "id": 2,
      "type": "Art"
    },
    {
      "id": 3,
      "type": "Geography"
    },
    {
      "id": 4,
      "type": "History"
    },
    {
      "id": 5,
      "type": "Entertainment"
    },
    {
      "id": 6,
      "type": "Sports"
    }
  ],
  "success": true
}
```

#### POST /categories
- General:
    - Creates a new category using the submitted type. Returns the id of the created category , success value and total categories.
- `curl http://127.0.0.1:5000/categories -X POST -H "Content-Type: application/json" -d '{"type":"new Category"}'`
```
{
  "created": 7,
  "success": true,
  "total_categories": 7
}
```
#### DELETE /categories/{category_id}
- General:
    - Deletes the category of the given ID if it exists. Returns the id of the deleted category , success value and total categories 
- `curl -X DELETE http://127.0.0.1:5000/categories/8`
```
{
  "deleted": 8,
  "success": true,
  "total_categories": 6
}
```
#### GET /questions
- General:
    - Returns available questions list, how many question objects for the given page number, success value, categories, next page route (only if exists) and total number of questions.
    - Results are paginated in groups of 10 but can be changed with QUESTIONS_PER_PAGE constant. Include a request argument to choose page number, starting from 1. 
- Sample: `curl http://127.0.0.1:5000/questions?page=2`

``` 
{
  "categories": [
    {
      "id": 1,
      "type": "Science"
    },
    {
      "id": 2,
      "type": "Art"
    },
    {
      "id": 3,
      "type": "Geography"
    },
    {
      "id": 4,
      "type": "History"
    },
    {
      "id": 5,
      "type": "Entertainment"
    },
    {
      "id": 6,
      "type": "Sports"
    }
  ],
  "items_per_page": 10,
  "list_of_questions": [
    {
      "answer": "Tom Cruise",
      "category": 5,
      "difficulty": 4,
      "id": 4,
      "question": "What actor did author Anne Rice first denounce, then praise in the role of her beloved Lestat?"
    },
    {
      "answer": "Maya Angelou",
      "category": 4,
      "difficulty": 2,
      "id": 5,
      "question": "Whose autobiography is entitled 'I Know Why the Caged Bird Sings'?"
    },
    {
      "answer": "Edward Scissorhands",
      "category": 5,
      "difficulty": 3,
      "id": 6,
      "question": "What was the title of the 1990 fantasy directed by Tim Burton about a young man with multi-bladed appendages?"
    },
    {
      "answer": "Muhammad Ali",
      "category": 4,
      "difficulty": 1,
      "id": 9,
      "question": "What boxer's original name is Cassius Clay?"
    },
    {
      "answer": "Brazil",
      "category": 6,
      "difficulty": 3,
      "id": 10,
      "question": "Which is the only team to play in every soccer World Cup tournament?"
    },
    {
      "answer": "Uruguay",
      "category": 6,
      "difficulty": 4,
      "id": 11,
      "question": "Which country won the first ever soccer World Cup in 1930?"
    },
    {
      "answer": "George Washington Carver",
      "category": 4,
      "difficulty": 2,
      "id": 12,
      "question": "Who invented Peanut Butter?"
    },
    {
      "answer": "Lake Victoria",
      "category": 3,
      "difficulty": 2,
      "id": 13,
      "question": "What is the largest lake in Africa?"
    },
    {
      "answer": "The Palace of Versailles",
      "category": 3,
      "difficulty": 3,
      "id": 14,
      "question": "In which royal palace would you find the Hall of Mirrors?"
    },
    {
      "answer": "Agra",
      "category": 3,
      "difficulty": 2,
      "id": 15,
      "question": "The Taj Mahal is located in which Indian city?"
    }
  ],
  "next_page": "http://127.0.0.1:5000/questions?page=2",
  "success": true,
  "total_questions": 26
}
```

#### POST /questions
- General:
    - Creates a new question using the submitted question, answer, difficulty and category. Returns the id of the created question, success value, total questionss, and question list based on current page.
	- `curl http://127.0.0.1:5000/questions?page=2-X POST -H "Content-Type: application/json" -d '{"question": "??Why are you reading this?", "answer": "Because I'm testing this app :D", "category": 2, "difficulty": 7}'`
```
{
  "question_created": 31,
  "questions": [
    {
      "answer": "Tom Cruise",
      "category": 5,
      "difficulty": 4,
      "id": 4,
      "question": "What actor did author Anne Rice first denounce, then praise in the role of her beloved Lestat?"
    },
    {
      "answer": "Maya Angelou",
      "category": 4,
      "difficulty": 2,
      "id": 5,
      "question": "Whose autobiography is entitled 'I Know Why the Caged Bird Sings'?"
    },
    {
      "answer": "Edward Scissorhands",
      "category": 5,
      "difficulty": 3,
      "id": 6,
      "question": "What was the title of the 1990 fantasy directed by Tim Burton about a young man with multi-bladed appendages?"
    },
    {
      "answer": "Muhammad Ali",
      "category": 4,
      "difficulty": 1,
      "id": 9,
      "question": "What boxer's original name is Cassius Clay?"
    },
    {
      "answer": "Brazil",
      "category": 6,
      "difficulty": 3,
      "id": 10,
      "question": "Which is the only team to play in every soccer World Cup tournament?"
    },
    {
      "answer": "Uruguay",
      "category": 6,
      "difficulty": 4,
      "id": 11,
      "question": "Which country won the first ever soccer World Cup in 1930?"
    },
    {
      "answer": "George Washington Carver",
      "category": 4,
      "difficulty": 2,
      "id": 12,
      "question": "Who invented Peanut Butter?"
    },
    {
      "answer": "Lake Victoria",
      "category": 3,
      "difficulty": 2,
      "id": 13,
      "question": "What is the largest lake in Africa?"
    },
    {
      "answer": "The Palace of Versailles",
      "category": 3,
      "difficulty": 3,
      "id": 14,
      "question": "In which royal palace would you find the Hall of Mirrors?"
    },
    {
      "answer": "Agra",
      "category": 3,
      "difficulty": 2,
      "id": 15,
      "question": "The Taj Mahal is located in which Indian city?"
    }
  ],
  "search": null,
  "success": true,
  "total_questions": 26
}
```
- POST Questions SEARCH: 
	Given a search term, returns the questions matching the string (case insensitive), success value, search term used and the total number of questions matching the search term.
	- `curl http://127.0.0.1:5000/questions?search=soccer -X POST -H "Content-Type: application/json"'`
```
{
  "questions": [
    {
      "answer": "Brazil",
      "category": 6,
      "difficulty": 3,
      "id": 10,
      "question": "Which is the only team to play in every soccer World Cup tournament?"
    },
    {
      "answer": "Uruguay",
      "category": 6,
      "difficulty": 4,
      "id": 11,
      "question": "Which country won the first ever soccer World Cup in 1930?"
    }
  ],
  "search": "soccer",
  "success": true,
  "total_questions": 25
}
```
#### DELETE /questions/{id}
- General:
    - Deletes the question of the given ID if it exists. Returns the id of the deleted question "question_deleted" as an int, success value and total questions.
- `curl -X DELETE http://127.0.0.1:5000/questions/4`
```
{
  "question_deleted": 4,
  "questions": [
    {
      "answer": "Maya Angelou",
      "category": 4,
      "difficulty": 2,
      "id": 5,
      "question": "Whose autobiography is entitled 'I Know Why the Caged Bird Sings'?"
    },
    {
      "answer": "Edward Scissorhands",
      "category": 5,
      "difficulty": 3,
      "id": 6,
      "question": "What was the title of the 1990 fantasy directed by Tim Burton about a young man with multi-bladed appendages?"
    },
    {
      "answer": "Muhammad Ali",
      "category": 4,
      "difficulty": 1,
      "id": 9,
      "question": "What boxer's original name is Cassius Clay?"
    },
    {
      "answer": "Brazil",
      "category": 6,
      "difficulty": 3,
      "id": 10,
      "question": "Which is the only team to play in every soccer World Cup tournament?"
    },
    {
      "answer": "Uruguay",
      "category": 6,
      "difficulty": 4,
      "id": 11,
      "question": "Which country won the first ever soccer World Cup in 1930?"
    },
    {
      "answer": "George Washington Carver",
      "category": 4,
      "difficulty": 2,
      "id": 12,
      "question": "Who invented Peanut Butter?"
    },
    {
      "answer": "Lake Victoria",
      "category": 3,
      "difficulty": 2,
      "id": 13,
      "question": "What is the largest lake in Africa?"
    },
    {
      "answer": "The Palace of Versailles",
      "category": 3,
      "difficulty": 3,
      "id": 14,
      "question": "In which royal palace would you find the Hall of Mirrors?"
    },
    {
      "answer": "Agra",
      "category": 3,
      "difficulty": 2,
      "id": 15,
      "question": "The Taj Mahal is located in which Indian city?"
    },
    {
      "answer": "Escher",
      "category": 2,
      "difficulty": 1,
      "id": 16,
      "question": "Which Dutch graphic artist???initials M C was a creator of optical illusions?"
    },
    {
      "answer": "Mona Lisa",
      "category": 2,
      "difficulty": 3,
      "id": 17,
      "question": "La Giaconda is better known as what?"
    },
    {
      "answer": "One",
      "category": 2,
      "difficulty": 4,
      "id": 18,
      "question": "How many paintings did Van Gogh sell in his lifetime?"
    },
    {
      "answer": "Jackson Pollock",
      "category": 2,
      "difficulty": 2,
      "id": 19,
      "question": "Which American artist was a pioneer of Abstract Expressionism, and a leading exponent of action painting?"
    },
    {
      "answer": "The Liver",
      "category": 1,
      "difficulty": 4,
      "id": 20,
      "question": "What is the heaviest organ in the human body?"
    },
    {
      "answer": "Alexander Fleming",
      "category": 1,
      "difficulty": 3,
      "id": 21,
      "question": "Who discovered penicillin?"
    },
    {
      "answer": "Blood",
      "category": 1,
      "difficulty": 4,
      "id": 22,
      "question": "Hematology is a branch of medicine involving the study of what?"
    },
    {
      "answer": "Scarab",
      "category": 4,
      "difficulty": 4,
      "id": 23,
      "question": "Which dung beetle was worshipped by the ancient Egyptians?"
    }
  ],
  "success": true
}
```
#### GET /categories/{category_id}/questions
- General:
    - gets all questions belonging to the given category, returns the current category, a list of the questions, success value and total number of questions in the category. if no questions found the request is still processed and returns a total number of 0 and an empty questions list
- `curl http://127.0.0.1:5000/categories/3/questions`
```
{
  "current_category": 3,
  "questions": [
    {
      "answer": "Lake Victoria",
      "category": 3,
      "difficulty": 2,
      "id": 13,
      "question": "What is the largest lake in Africa?"
    },
    {
      "answer": "The Palace of Versailles",
      "category": 3,
      "difficulty": 3,
      "id": 14,
      "question": "In which royal palace would you find the Hall of Mirrors?"
    },
    {
      "answer": "Agra",
      "category": 3,
      "difficulty": 2,
      "id": 15,
      "question": "The Taj Mahal is located in which Indian city?"
    }
  ],
  "success": true,
  "total_questions": 3
}
```
#### POST /quizzes
- General:
    - takes a  list of previous_questions and a quiz_category and returns a random question belonging to the given category and is not in the previous questions list, total number of questions left(including the returned question) and success value. if category is zero, the request queries all the questions that are not in the previous questions list.
 
 - Example1 :
	- `curl http://127.0.0.1:5000/quizzes -H "Content-Type: application/json" -d '{"previous_questions":[], "quiz_category":{"id":"6"}}`
```
{
  "question": {
    "answer": "Uruguay",
    "category": 6,
    "difficulty": 4,
    "id": 11,
    "question": "Which country won the first ever soccer World Cup in 1930?"
  },
  "success": true,
  "total_questions": 2
}
```

#### Author:
Alejandro Gallego - Udacity Student.



## Testing
To run the tests, run
```
dropdb trivia_test
createdb trivia_test
psql trivia_test < trivia.psql
python test_flaskr.py
```
