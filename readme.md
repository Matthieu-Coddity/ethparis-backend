#install
python3 -m venv env
source env/bin/activate
pip install -r requirements.txt
python3 manage.py db init
python3 manage.py db migrate
python3 manage.py db upgrade
python3 manage.py runserver