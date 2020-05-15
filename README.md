Project Setup

1. Create project foler
2. Create python virtual enviornment
    python -m venv env
3. Enter Virtual Enviornment
    cmd /k ".\env\Scripts\activate.bat"
4. Leave virtual Env
    cmd /k ".\env\Scripts\deactivate.bat"

Install Flask
  python -m pip install Flask==1.1.1
  python -m pip freeze > requirements.txt

Run flask
  python app.py
