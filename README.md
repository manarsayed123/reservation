# reservation
to get the project working
1-create virtual environment
2- activate env
3-run this command pip install -r requirements.txt
4 - create .env file add on it database url with this key DJANGO_DATABASE_URL
5- run this command ./manage.py migrate
6 - run this command ./manage.py runserver

Note i added swagger documentation to access it through this url on local host http://127.0.0.1:8000/docs/

Note for permissions i created custom permission class is doctor this will be true if user role is Admin


