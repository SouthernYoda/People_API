from flask import render_template

import config

# Create the application instance
#app = Flask(__name__, template_folder="templates")

# Create the application instance
connex_app = config.connex_app

# Read the swagger.yml
connex_app.add_api('swagger.yml')

@connex_app.route('/')
def home():
    return render_template('home.html')

if __name__ == "__main__":
    connex_app.run(debug=True)
