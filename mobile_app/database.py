import sqlite3
import os

class Database:
    def __init__(self):
        self.db_name = "mobile_app.db"
        self.conn = None
        self.create_tables()

    def connect(self):
        self.conn = sqlite3.connect(self.db_name)
        self.conn.row_factory = sqlite3.Row
        return self.conn

    def create_tables(self):
        conn = self.connect()
        cursor = conn.cursor()

        # Categories
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS categories (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT UNIQUE NOT NULL,
                icon TEXT
            )
        ''')

        # Products
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS products (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                price REAL NOT NULL,
                category_id INTEGER,
                image TEXT,
                rating REAL DEFAULT 0.0,
                FOREIGN KEY (category_id) REFERENCES categories (id)
            )
        ''')

        # Ads
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS ads (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT NOT NULL,
                description TEXT NOT NULL,
                icon TEXT
            )
        ''')

        # Offers
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS offers (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT NOT NULL,
                discount TEXT NOT NULL,
                icon TEXT
            )
        ''')

        # Orders
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS orders (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                total_amount REAL NOT NULL,
                items_count INTEGER NOT NULL,
                date TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')

        
        # Admin
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS admin (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT UNIQUE NOT NULL,
                password TEXT NOT NULL
            )
        ''')

        # Seed default data if empty
        cursor.execute("SELECT count(*) FROM categories")
        if cursor.fetchone()[0] == 0:
            categories = [
                ('أقلام', 'pencil'),
                ('دفاتر', 'book-open-page-variant'),
                ('أدوات رسم', 'palette'),
                ('أدوات قص', 'scissors-cutting'),
                ('حقائب', 'bag-personal'),
                ('آلات حاسبة', 'calculator')
            ]
            cursor.executemany("INSERT INTO categories (name, icon) VALUES (?, ?)", categories)
            
            # Default Admin
            cursor.execute("INSERT INTO admin (username, password) VALUES (?, ?)", ('admin', 'admin123'))

        conn.commit()
        conn.close()

    # --- CRUD Operations ---

    def get_categories(self):
        conn = self.connect()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM categories")
        rows = cursor.fetchall()
        conn.close()
        return rows

    def get_products(self, category_id=None):
        conn = self.connect()
        cursor = conn.cursor()
        if category_id:
            cursor.execute("SELECT * FROM products WHERE category_id = ?", (category_id,))
        else:
            cursor.execute("SELECT * FROM products")
        rows = cursor.fetchall()
        conn.close()
        return rows

    def add_product(self, name, price, category_id, image=None):
        conn = self.connect()
        cursor = conn.cursor()
        cursor.execute("INSERT INTO products (name, price, category_id, image) VALUES (?, ?, ?, ?)",
                       (name, price, category_id, image))
        conn.commit()
        conn.close()

    def get_ads(self):
        conn = self.connect()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM ads")
        rows = cursor.fetchall()
        conn.close()
        return rows

    def get_offers(self):
        conn = self.connect()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM offers")
        rows = cursor.fetchall()
        conn.close()
        return rows
        
    def check_login(self, username, password):
        conn = self.connect()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM admin WHERE username = ? AND password = ?", (username, password))
        user = cursor.fetchone()
        conn.close()
        return user

    def add_category(self, name, icon=None):
        conn = self.connect()
        cursor = conn.cursor()
        try:
            cursor.execute("INSERT INTO categories (name, icon) VALUES (?, ?)", (name, icon))
            conn.commit()
            return True
        except sqlite3.IntegrityError:
            return False
        finally:
            conn.close()

    def delete_category(self, category_id):
        conn = self.connect()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM categories WHERE id = ?", (category_id,))
        conn.commit()
        conn.close()

    def delete_product(self, product_id):
        conn = self.connect()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM products WHERE id = ?", (product_id,))
        conn.commit()
        conn.close()

    def add_ad(self, title, description, icon=None):
        conn = self.connect()
        cursor = conn.cursor()
        cursor.execute("INSERT INTO ads (title, description, icon) VALUES (?, ?, ?)", (title, description, icon))
        conn.commit()
        conn.close()

    def delete_ad(self, ad_id):
        conn = self.connect()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM ads WHERE id = ?", (ad_id,))
        conn.commit()
        conn.close()

    def add_offer(self, title, discount, icon=None):
        conn = self.connect()
        cursor = conn.cursor()
        cursor.execute("INSERT INTO offers (title, discount, icon) VALUES (?, ?, ?)", (title, discount, icon))
        conn.commit()
        conn.close()

    def delete_offer(self, offer_id):
        conn = self.connect()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM offers WHERE id = ?", (offer_id,))
        conn.commit()
        conn.close()

    def add_order(self, total_amount, items_count):
        conn = self.connect()
        cursor = conn.cursor()
        cursor.execute("INSERT INTO orders (total_amount, items_count) VALUES (?, ?)", (total_amount, items_count))
        conn.commit()
        conn.close()

    def get_stats(self):
        conn = self.connect()
        cursor = conn.cursor()
        
        stats = {}
        
        # Categories count
        cursor.execute("SELECT COUNT(*) FROM categories")
        stats['categories_count'] = cursor.fetchone()[0]
        
        # Products count
        cursor.execute("SELECT COUNT(*) FROM products")
        stats['products_count'] = cursor.fetchone()[0]
        
        # Orders count
        cursor.execute("SELECT COUNT(*) FROM orders")
        stats['orders_count'] = cursor.fetchone()[0]
        
        # Ads count
        cursor.execute("SELECT COUNT(*) FROM ads")
        stats['ads_count'] = cursor.fetchone()[0]
        
        # Offers count
        cursor.execute("SELECT COUNT(*) FROM offers")
        stats['offers_count'] = cursor.fetchone()[0]
        
        # Products per category
        cursor.execute('''
            SELECT c.name, COUNT(p.id) as count 
            FROM categories c 
            LEFT JOIN products p ON c.id = p.category_id 
            GROUP BY c.id
        ''')
        stats['products_per_category'] = cursor.fetchall()
        
        conn.close()
        return stats
