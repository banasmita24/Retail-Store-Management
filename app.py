from flask import  Flask, request, jsonify, render_template
import sqlite3

app = Flask(__name__)

with sqlite3.connect('Store.db') as conn:
        conn.execute("CREATE TABLE IF NOT EXISTS products"
                       "(id INTEGER PRIMARY KEY AUTOINCREMENT, name TEXT, price INTEGER, quantity INTEGER)")
        
@app.route('/')
def home():
    with sqlite3.connect('Store.db') as conn:
        products = conn.execute('SELECT * FROM products').fetchall()
    return render_template('retailStore.html', products = products)

@app.route('/add', methods=['POST'])
def add_product():
    name = request.form['name']
    price = int(request.form['price'])
    quantity = int(request.form['quantity'])
    with sqlite3.connect('Store.db') as conn:
        conn.execute('INSERT INTO products(name, price, quantity) VALUES (?, ?, ?)', (name, price, quantity))
    return 'Product added successfully!'

@app.route('/update', methods=['POST'])
def update_product():
    product_id = int(request.form['id'])
    name = request.form['name']
    price = int(request.form['price'])
    quantity = int(request.form['quantity'])
    with sqlite3.connect('Store.db') as conn:
        result = conn.execute('SELECT * FROM products WHERE id = ?', (product_id,)).fetchone()
        if result  is None:
            return 'NO items found to Update!'
        conn.execute('UPDATE products SET name = ?, price = ?, quantity = ? WHERE id = ?', (name, price, quantity, product_id))
    return 'Product updated successfully!'

@app.route('/delete', methods=['POST'])
def delete_product():
    product_id = int(request.form['id'])
    with sqlite3.connect('Store.db') as conn:
        result = conn.execute('SELECT * FROM products WHERE id = ?', (product_id,)).fetchone()
        if result  is None:
            return 'NO items found to Delete!'
        conn.execute('DELETE FROM products WHERE id = ?', (product_id,))
    return 'Product deleted successfully!'

@app.route('/search', methods=['GET'])
def search_products():
    search_query = request.args.get('query', '')
    with sqlite3.connect('Store.db') as conn:
        results = conn.execute('SELECT * FROM products WHERE name LIKE ? OR id LIKE ?', (f'%{search_query}%', f'%{search_query}%') ).fetchall()
        if results  is None:
            return 'NO items Found!'
    return jsonify(results)
