from flask import (
    Flask,
    render_template
)
import connexion

# Create the application instance
#app = Flask(__name__, template_folder="templates")

# Create the application instance
app = connexion.App(__name__, specification_dir='./')

# Read the swagger.yml
app.add_api('swagger.yml')

@app.route('/')
def home():
    return render_template('home.html')

if __name__ == '__main__':
    app.run(debug=True)
