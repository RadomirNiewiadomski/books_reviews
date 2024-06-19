# Books review

Web application that allows users to browse books, add reviews, and rate books.


## Project Assumptions:

#### Homepage:

Display a list of books with filtering options by category and search by title or author.
Each book entry include the title, author, image, a short description, and the average rating.

#### Book Details:

Show detailed information about a book, including a longer description and author details.
Display a list of user reviews with ratings.
Provide a form for adding a new review with a rating (only for logged in users)

#### Add new book / author / category:

Provide a form for adding a new book or author or category (only for administrators)

### Additional information:

1. Project was integrated with Github Actions.
2. The application was made according to the TDD methodology.
3. Authorization is accessible thru Token Authentication.
4. AJAX was implemented to allow asynchronous review submission and updating of the average rating without page reload.

### Technologies:
- Python version: 3.9
- Django version: 4.0.1
- Django REST framework version: 3.13.1
- Docker version: 20.10.22
- Psycopg2 version: 2.9.3 (PostgreSQL)
- HTML5
- CSS3
- Bootstrap version: 5.1.3
- JavaScript
- Others: see 'requirements.txt'

## Setup instruction:
After installing docker and cloning git repository,
build application locally by entering:

```
docker-compose up --build
```

## Accessing the application:

Homepage:
```
http://localhost:8000/
```

Admin site
```
http://localhost:8000/admin/
```

Default created admin account:
```
email: admin@example.com
password: password123
```

#### Testing:

To run tests:
```
docker-compose run --rm app sh -c "python manage.py test"
```

#### REST API:

Application is also created in form of REST API (for future proofing)

API documentation - Swagger:
(To access POST, PUT, PATCH, DELETE methods you need to provide Token Authentication.)
```
http://localhost:8000/api/docs/
```

## Created by:
Radomir Niewiadomski
