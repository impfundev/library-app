python3.9 -m venv env
python3.9 source env/bin/activate
pip install -r requirements.txt --root-user-action=ignore
python3.9 manage.py collectstatic --noinput