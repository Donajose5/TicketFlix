# TicketFlix 

A multi-user application for movie ticket management and booking, with admin and user functionalities.
Project for Modern Application Development 2 course in IITM.

## Techonologies Used
- Flask – used to facilitate web development in python
- Vue.js – framework used to develop the frontend and UI
- Flask-SQLAlchemy – to support the use of SQLAlchemy in the application
- Flask-security  -  to ensure authentication of the users
- Flask-Restful – used to create REST API
- sqlite3 – used for the database
- Celery -  for tasks and job management
- Redis -  for caching

## Local Setup

- Run `pip install -r requirements.txt` to install all dependencies and libraries written in `requirements.txt` .

## Local Development Run

- `python3 app.py` in backened to start the flask app in `development` mode.
- `npm run serve` in frontend for serving the app from frontend on Vue.
- `redis-server` to start the redis server in terminal.
- `celery -A app.celery worker -l info ` in the backend to start the celery workers.
- `celery -A app.celery beat --max-interval 1 -l info` in backend folder to start the celery beat and scheduler.

## Folder Structure

- `apispecification.yaml` - contains the api specification for the project.
- `backend` - the folder which contains the main python file, the api definitions, the database 'database.sqlite3', models.
- `frontend` - folder which contains the views, the router and the components of the application.
- `requirements.txt` - contains the frameworks and libraries which need to be installed.
- `Project Documentation.pdf` - the project documentation.

```
Project
|-- apispecification.yaml
|-- backend
|   |-- api.py
|   |-- app.py
|   |-- cache.py
|   |-- cachingdata.py
|   |-- celerybeat-schedule
|   |-- database.py
|   |-- database.sqlite3
|   |-- emailgenr.py
|   |-- instance
|   |   `-- database.sqlite3
|   |-- models.py
|   |-- static
|   |-- tasks.py
|   |-- templates
|   |   |-- booking_ticket.html
|   |   |-- daily_reminder.html
|   |   `-- monthly_report.html
|   `-- workers.py
|-- frontend
|-- |-- node_modules
|   |-- README.md
|   |-- babel.config.js
|   |-- jsconfig.json
|   |-- package-lock.json
|   |-- package.json
|   |-- public
|   |   |-- favicon.ico
|   |   `-- index.html
|   |-- src
|   |   |-- App.vue
|   |   |-- assets
|   |   |   `-- logo.png
|   |   |-- components
|   |   |   |-- AdminNavbar.vue
|   |   |   |-- AdminSummary.vue
|   |   |   |-- BookingsPage.vue
|   |   |   |-- HelloWorld.vue
|   |   |   |-- LogIn.vue
|   |   |   |-- MoviePage.vue
|   |   |   |-- ProfilePage.vue
|   |   |   |-- SearchPage.vue
|   |   |   |-- ShowPage.vue
|   |   |   |-- SignUp.vue
|   |   |   |-- StartPage.vue
|   |   |   |-- UserNavbar.vue
|   |   |   |-- UserShow.vue
|   |   |   |-- UserVenue.vue
|   |   |   `-- VenuePage.vue
|   |   |-- main.js
|   |   |-- router
|   |   |   `-- index.js
|   |   |-- store
|   |   |   `-- index.js
|   |   `-- views
|   |       |-- AdminView.vue
|   |       |-- HomeView.vue
|   |       `-- StartView.vue
|   `-- vue.config.js
|-- Project Documentation.pdf
|-- readme.md
`-- requirements.txt
```
