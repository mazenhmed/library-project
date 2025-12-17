from flask import Flask, render_template
from flask_cors import CORS
from backend.database import init_db, db
from backend.models import Admin, Category
from backend.routes import api_bp

app = Flask(__name__)
CORS(app)

# Configuration
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///stationery.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'dev-secret-key'

# Initialize Database
init_db(app)

# Seed Database
with app.app_context():
    # Create default admin
    if not Admin.query.filter_by(username='admin').first():
        admin = Admin(username='admin', email='admin@example.com')
        admin.set_password('admin123')
        db.session.add(admin)
        
    # Create default categories
    categories = ['أقلام', 'دفاتر', 'أدوات رسم', 'أدوات قص', 'حقائب', 'آلات حاسبة']
    for cat_name in categories:
        if not Category.query.filter_by(name=cat_name).first():
            category = Category(name=cat_name)
            db.session.add(category)
            
    db.session.commit()

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
