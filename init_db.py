from app import app
from backend.database import db
from backend.models import Admin, Category, Product, Ad, Offer, Order

def init_database():
    with app.app_context():
        db.drop_all()
        db.create_all()
        
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
        print("Database initialized successfully!")

if __name__ == '__main__':
    init_database()
