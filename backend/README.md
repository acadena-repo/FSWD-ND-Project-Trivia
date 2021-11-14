# Backend - Full Stack Trivia API 

### Installing Dependencies for the Backend

1. **Python 3.8** - Follow instructions to install the latest version of python for your platform in the [python docs](https://docs.python.org/3/using/unix.html#getting-and-installing-the-latest-version-of-python)


2. **Virtual Enviornment** - We recommend working within a virtual environment whenever using Python for projects. This keeps your dependencies for each project separate and organaized. Instructions for setting up a virual enviornment for your platform can be found in the [python docs](https://packaging.python.org/guides/installing-using-pip-and-virtual-environments/)


3. **PIP Dependencies** - Once you have your virtual environment setup and running, install dependencies by naviging to the `/backend` directory and running:
```bash
pip install -r requirements.txt
```
This will install all of the required packages we selected within the `requirements.txt` file.


4. **Key Dependencies**
 - [Flask](http://flask.pocoo.org/)  is a lightweight backend microservices framework. Flask is required to handle requests and responses.

 - [SQLAlchemy](https://www.sqlalchemy.org/) is the Python SQL toolkit and ORM we'll use handle the database. You'll primarily work in app.py and can reference models.py. 

 - [Flask-CORS](https://flask-cors.readthedocs.io/en/latest/#) is the extension we'll use to handle cross origin requests from our frontend server. 

### Database Setup
With Postgres running, restore a database using the trivia.psql file provided. From the backend folder in terminal run:
```bash
psql trivia < trivia.psql
```

### Running the server

From within the `./backend` directory first ensure you are working using your created virtual environment.

To run the server, execute:

```bash
export FLASK_APP=flaskr
flask run
```

## Trivia API
### Show Categories
Returns a json object with all categories, that contains id:category as key-value pairs.
- **URL:** `/categories`
- **Method:** `GET`
- **URL Params:** `None`
- **Success Response:**```
        Code: 200
        Content:
                {'1' : "Science",
                 '2' : "Art",
                 '3' : "Geography",
                 '4' : "History",
                 '5' : "Entertainment",
                 '6' : "Sports"}```
- **Error Response:** `None`

### Show Questions by page
Returns a json object with 10 questions according with the page number requested.
- **URL:** `/questions?page=1`
- **Method:** `GET`
- **URL Params:** `page=[integer]`
- **Success Response:**```
        Code: 200
        Content:
                {'questions' : "collection of 10 questions",
                 'total_questions' : "total number of questions in the database",
                 'categories' : "json object with all categories",
                 'current_category' : "category description of the first question in collection"}```
- **Error Response:**```
        Code: 404
        Content:
                {"success": False, "error": 404, "message": "resource not found"}```

### Show Questions by category
Returns a json object with all questions for category requested.
- **URL:** `/categories/:id/questions`
- **Method:** `GET`
- **URL Params:** `id=[integer]`
- **Success Response:**```
        Code: 200
        Content:
                {'questions' : "collection of questions fileted by category",
                 'total_questions' : "total number of questions in the collection",
                 'current_category' : "category description in the collection"}```
- **Error Response:**```
        Code: 404
        Content:
                {"success": False, "error": 404, "message": "resource not found"}```

### Add Question
Insert a new question into the database.
- **URL:** `/questions`
- **Method:** `POST`
- **URL Params:**```
                {'question':[string],
                 'answer':[string],
                 'difficulty':[integer],
                 'category':[integer]}```
- **Success Response:**```
        Code: 200
        Content:
                {'success': True}```
- **Error Response:**```
        Code: 422
        Content:
                {"success": False, "error": 422, "message": "unprocessable"}```

### Delete Question
Delete a question from the database.
- **URL:** `/questions/:id`
- **Method:** `DELETE`
- **URL Params:** `id=[integer]`
- **Success Response:**```
        Code: 200
        Content:
                {'success': True, 'id': question.id}```
- **Error Response:**```
        Code: 404
        Content:
                {"success": False, "error": 404, "message": "resource not found"}```

### Search Questions
Returns a json object with all questions found according the search term.
- **URL:** `/questions/search`
- **Method:** `POST`
- **URL Params:** `searchTerm=[string]`
- **Success Response:**```
        Code: 200
        Content:
                {'questions' : "collection of questions fileted by search term",
                 'total_questions' : "total number of questions in the collection",
                 'current_category' : "category description of the first question in collection"}```
- **Error Response:**```
        Code: 404
        Content:
                {"success": False, "error": 404, "message": "resource not found"}```

### Play a trivia quiz
Returns a json object with a question selected randomly for the category selected.
- **URL:** `/quizzes`
- **Method:** `POST`
- **URL Params:**```
                {'previous_question':[list],
                 'category_id':[integer]}```
- **Success Response:**```
        Code: 200
        Content:
                {'question': "object with question, answer, difficulty and category"}```
- **Error Response:** `None`

## Testing
To run the tests, run
```
dropdb trivia_test
createdb trivia_test
psql trivia_test < trivia.psql
python test_flaskr.py
```