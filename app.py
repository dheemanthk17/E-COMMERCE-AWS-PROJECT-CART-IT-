from flask import Flask, jsonify, request
from flask_cors import CORS
import mysql.connector
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
CORS(app)

def get_db_connection():
    return mysql.connector.connect(
        host='cart-it-db.cvq0ec8i6o9q.ap-south-1.rds.amazonaws.com',
        database='cart_it_store',
        user='admin',
        password='YOUR_PASSWORD',
        ssl_ca='./global-bundle.pem'
    )

@app.route('/', methods=['GET'])
def home():
    return jsonify({"message": "Cart-It Backend is running!"})

@app.route('/api/products', methods=['GET'])
def get_products():
    try:
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM products;")
        products = cursor.fetchall()
        cursor.close()
        conn.close()
        return jsonify(products)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# --- AUTHENTICATION ROUTES ---

@app.route('/api/register', methods=['POST'])
def register():
    data = request.json
    username = data.get('username')
    email = data.get('email')
    password = data.get('password')

    if not username or not email or not password:
        return jsonify({"error": "All fields are required"}), 400

    hashed_password = generate_password_hash(password)

    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO users (username, email, password) VALUES (%s, %s, %s)",
            (username, email, hashed_password)
        )
        conn.commit()
        cursor.close()
        conn.close()
        return jsonify({"message": "User registered successfully!"}), 201
    except mysql.connector.Error as err:
        return jsonify({"error": "Username or email already exists."}), 409

@app.route('/api/login', methods=['POST'])
def login():
    data = request.json
    email = data.get('email')
    password = data.get('password')

    try:
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM users WHERE email = %s", (email,))
        user = cursor.fetchone()
        cursor.close()
        conn.close()

        if user and check_password_hash(user['password'], password):
            return jsonify({
                "message": "Login successful!",
                "user": {"id": user['id'], "username": user['username'], "email": user['email']}
            }), 200
        else:
            return jsonify({"error": "Invalid email or password"}), 401
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# --- CART & WISHLIST ROUTES ---

@app.route('/api/cart/add', methods=['POST'])
def add_to_cart():
    data = request.json
    user_id = data.get('user_id')
    product_name = data.get('product_name')

    if not user_id:
        return jsonify({"error": "Please login to add items to bag"}), 401

    try:
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)

        # Find the product ID based on the name
        cursor.execute("SELECT id FROM products WHERE name = %s", (product_name,))
        product = cursor.fetchone()

        if not product:
            return jsonify({"error": "Product not found"}), 404

        product_id = product['id']

        # Check if it is already in the cart
        cursor.execute("SELECT * FROM cart WHERE user_id = %s AND product_id = %s", (user_id, product_id))
        cart_item = cursor.fetchone()

        if cart_item:
            cursor.execute("UPDATE cart SET quantity = quantity + 1 WHERE id = %s", (cart_item['id'],))
        else:
            cursor.execute("INSERT INTO cart (user_id, product_id, quantity) VALUES (%s, %s, 1)", (user_id, product_id))

        conn.commit()
        cursor.close()
        conn.close()
        return jsonify({"message": "Added to bag successfully!"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500
@app.route('/api/cart/<int:user_id>', methods=['GET'])
def get_cart(user_id):
    try:
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        # Join cart and products tables to get names and images
        cursor.execute("""
            SELECT c.id as cart_id, c.quantity, p.name, p.price, p.image_url
            FROM cart c
            JOIN products p ON c.product_id = p.id
            WHERE c.user_id = %s
        """, (user_id,))
        cart_items = cursor.fetchall()
        cursor.close()
        conn.close()
        return jsonify(cart_items), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500
@app.route('/api/cart/update', methods=['POST'])
def update_cart_qty():
    data = request.json
    cart_id = data.get('cart_id')
    quantity = data.get('quantity')

    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        if quantity <= 0:
            cursor.execute("DELETE FROM cart WHERE id = %s", (cart_id,))
        else:
            cursor.execute("UPDATE cart SET quantity = %s WHERE id = %s", (quantity, cart_id))
        conn.commit()
        cursor.close()
        conn.close()
        return jsonify({"message": "Updated"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500
# --- ORDER ROUTES ---

@app.route('/api/orders/place', methods=['POST'])
def place_order():
    data = request.json
    user_id = data.get('user_id')
    items_summary = data.get('items_summary')
    total_price = data.get('total_price')
    payment_method = data.get('payment_method')
    delivery_details = data.get('delivery_details')

    try:
        conn = get_db_connection()
        cursor = conn.cursor()

        # Save the order with default "Processing" status
        cursor.execute(
            "INSERT INTO orders (user_id, items_summary, total_price, payment_method, delivery_details, status) VALUES (%s, %s, %s, %s, %s, 'Processing - Preparing for Dispatch')",
            (user_id, items_summary, total_price, payment_method, delivery_details)
        )

        # Clear the cart since the items are now ordered
        cursor.execute("DELETE FROM cart WHERE user_id = %s", (user_id,))

        conn.commit()
        cursor.close()
        conn.close()
        return jsonify({"message": "Order placed successfully!"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/orders/<int:user_id>', methods=['GET'])
def get_orders(user_id):
    try:
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        # Fetch orders from newest to oldest
        cursor.execute("SELECT * FROM orders WHERE user_id = %s ORDER BY created_at DESC", (user_id,))
        orders = cursor.fetchall()
        cursor.close()
        conn.close()
        return jsonify(orders), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)