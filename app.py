from flask import Flask, render_template
from flask_cors import CORS
from backend.database import init_db
from backend.routes import api_bp

app = Flask(__name__)
CORS(app)

# Configuration
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///stationery.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'dev-secret-key'

# Initialize Database
init_db(app)

# Register Blueprints
app.register_blueprint(api_bp, url_prefix='/api')

# Routes for Pages
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/admin')
def admin():
    return render_template('admin.html')

@app.route('/admin-login')
def admin_login():
    return render_template('admin-login.html')

@app.route('/test-logo')
def test_logo():
    return render_template('test-logo.html')

if __name__ == '__main__':
    app.run(debug=True, port=5000)
