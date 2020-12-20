# Full Stack Trivia API Backend

## Getting Started

### Installing Dependencies

#### Python 3.7

Follow instructions to install the latest version of python for your platform in the [python docs](https://docs.python.org/3/using/unix.html#getting-and-installing-the-latest-version-of-python)

#### Virtual Enviornment

We recommend working within a virtual environment whenever using Python for projects. This keeps your dependencies for each project separate and organaized. Instructions for setting up a virual enviornment for your platform can be found in the [python docs](https://packaging.python.org/guides/installing-using-pip-and-virtual-environments/)

#### PIP Dependencies

Once you have your virtual environment setup and running, install dependencies by naviging to the `/backend` directory and running:

```bash
pip install -r requirements.txt
```

This will install all of the required packages we selected within the `requirements.txt` file.

##### Key Dependencies

- [Flask](http://flask.pocoo.org/)  is a lightweight backend microservices framework. Flask is required to handle requests and responses.

- [SQLAlchemy](https://www.sqlalchemy.org/) is the Python SQL toolkit and ORM we'll use handle the lightweight sqlite database. You'll primarily work in app.py and can reference models.py. 

- [Flask-CORS](https://flask-cors.readthedocs.io/en/latest/#) is the extension we'll use to handle cross origin requests from our frontend server. 

## Database Setup
With Postgres running, restore a database using the trivia.psql file provided. From the backend folder in terminal run:
```bash
psql trivia < trivia.psql
```
## Running the server

From within the `backend` directory first ensure you are working using your created virtual environment.

To run the server, execute:

```bash
export FLASK_APP=flaskr
export FLASK_ENV=development
flask run
```
Setting the `FLASK_ENV` variable to `development` will detect file changes and restart the server automatically.
Setting the `FLASK_APP` variable to `flaskr` directs flask to use the `flaskr` directory and the `__init__.py` file to find the application. 


Please provide the following environment variables for your specific database:
Here the app itself
```bash
export PROD_USERNAME=<your database username>
export PROD_PASSWORD=<your database password>
export PROD_SERVER=<your database server>
export PROD_PORT=<your database port>
```

and for the testing scenario:
```bash
export TEST_USERNAME=<your database username>
export TEST_PASSWORD=<your database password>
export TEST_SERVER=<your database server>
export TEST_PORT=<your database port>
```

## Testing
To run the tests, run:
```
dropdb trivia_test
createdb trivia_test
psql trivia_test < trivia.psql
python test_flaskr.py
```

## Endpoint Overview
Here is the list of all available Endpoints:
1. GET '/categories'
2. GET '/categories/<int:category_id>'
3. POST '/categories/<int:category_id>/play'
4. GET '/questions'
5. POST '/questions'
6. DELETE '/questions/<int:question_id>'
7. POST '/questions/search'

## Detailed Description of the Endpoints:
### 1. GET '/categories'
- Fetches a dictionary of categories in which the keys are the ids and the value is the corresponding string of the category
- Request Arguments: None
- Returns: An object with a single key, categories, that contains an object of id: category_string key:value pairs. 
```json
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
**Example request:** (localhost:5000 might be replaced in your setup)
```bash
curl --request GET http://localhost:5000/categories
```

### 2. GET '/categories/<int:category_id>'
- Fetches detailed information for a specific category_id passed. It will return a json with key: 'questions' for all questions in that category_id
- Request Arguments: category_id (int) in the url
- Returns: An json object (all questions in that category) with success key to True and a key 'questions' with the following structure:
```json
{
    "questions": [
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
        }
    ],
    "success": true
}
```
**Example request:** (localhost:5000 might be replaced in your setup)
```bash
curl --request GET http://localhost:5000/categories/1
```

### 3. POST '/categories/<int:category_id>/play'
- Fetches a list of questions to a specific category_id passed. Additionally you can pass a list of query-ids that you want to exclude from the resultset.
- Request Arguments: 
  - category_id (int) in the url
  - a list of questions_ids in a json_dict with key: previous_question - that you want to exclude from the resultset
- Returns: An json object (all questions in that category - filtered) with success key to True and a key 'list_of_questions_to_play' with the following structure:
```json
  "list_of_questions_to_play": [
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
    }
  ],
  "success": true
}
```
**Example request:** (localhost:5000 might be replaced in your setup)
```bash
curl --header "Content-Type: application/json" --request POST --data '{"previous_question":[1,2,3,4]}' http://localhost:5000/categories/1/play
```

### 4. GET '/questions'
- Fetches a dictionary of questions with all sorts of information regarding a question
- Request Arguments: None
- Returns: An json object (10 questions per page) with keys: id, question, answer, category, difficulty
```json
{
    "questions": [
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
        }
    ],
    "success": true
}
```
**Example request:** (localhost:5000 might be replaced in your setup)
```bash
curl --request GET http://localhost:5000/questions
```

### 5. POST '/questions'
- Inserts a new question into the database
- Request Arguments: json object with the following keys: question, answer, category, difficulty
- Returns: An json object with a success message
```json
{
    "success": True,
    "message": 'Question successfully inserted'
}
```
**Example request:** (localhost:5000 might be replaced in your setup)
```bash
curl --header "Content-Type: application/json" --request POST --data '{"question":"What is the name of Michael Knights car?","answer":"KITT", "category": 5, "difficulty": 3}' http://localhost:5000/questions
```

### 6. DELETE '/questions/<int:question_id>'
- Deletes the question by the question_id provided. 
- Request Arguments: question_id int in url
- Returns: json object with success message
```json
{
    "success": True,
    "message": 'Question successfully deleted'
}
```
**Example request:** (localhost:5000 might be replaced in your setup)
```bash
curl --request DELETE http://localhost:5000/questions/13
```

### 7. POST '/questions/search'
- Searches inside of the question text for a provided search term.
- Request Arguments: url parameter with name 'title' (string)
- Returns: json object with a list of questions that match the search term e.g:
```json
{
    "questions": [
        {
            "answer": "Muhammad Ali",
            "category": 4,
            "difficulty": 1,
            "id": 9,
            "question": "What boxer's original name is Cassius Clay?"
        },
        {
            "answer": "Tom Cruise",
            "category": 5,
            "difficulty": 4,
            "id": 4,
            "question": "What actor did author Anne Rice first denounce, then praise in the role of her beloved Lestat?"
        },
        {
            "answer": "Edward Scissorhands",
            "category": 5,
            "difficulty": 3,
            "id": 6,
            "question": "What was the title of the 1990 fantasy directed by Tim Burton about a young man with multi-bladed appendages?"
        },
        {
            "answer": "Lake Victoria",
            "category": 3,
            "difficulty": 2,
            "id": 13,
            "question": "What is the largest lake in Africa?"
        },
        {
            "answer": "Mona Lisa",
            "category": 2,
            "difficulty": 3,
            "id": 17,
            "question": "La Giaconda is better known as what?"
        },
        {
            "answer": "The Liver",
            "category": 1,
            "difficulty": 4,
            "id": 20,
            "question": "What is the heaviest organ in the human body?"
        },
        {
            "answer": "Blood",
            "category": 1,
            "difficulty": 4,
            "id": 22,
            "question": "Hematology is a branch of medicine involving the study of what?"
        },
        {
            "answer": "KITT",
            "category": 5,
            "difficulty": 3,
            "id": 24,
            "question": "What is the name of Michael Knights car?"
        },
        {
            "answer": "KITT",
            "category": 5,
            "difficulty": 3,
            "id": 45,
            "question": "What is the name of Michael Knights car?"
        }
    ],
    "success": true
}
```
**Example request:** (localhost:5000 might be replaced in your setup)
```bash
curl --request POST http://localhost:5000/questions?title=what
```