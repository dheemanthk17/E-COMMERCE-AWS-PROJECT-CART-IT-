import mysql.connector

try:
    conn = mysql.connector.connect(
        host='cart-it-db.cvq0ec8i6o9q.ap-south-1.rds.amazonaws.com',
        database='cart_it_store',
        user='admin',
        password='YOUR_PASSWORD',
        ssl_ca='./global-bundle.pem'
    )
    cursor = conn.cursor()

    # Recreate cart table linked to user_id
    cursor.execute("DROP TABLE IF EXISTS cart;")
    cursor.execute("""
        CREATE TABLE cart (
            id INT AUTO_INCREMENT PRIMARY KEY,
            user_id INT,
            product_id INT,
            quantity INT DEFAULT 1,
            FOREIGN KEY (user_id) REFERENCES users(id),
            FOREIGN KEY (product_id) REFERENCES products(id)
        );
    """)

    # Create wishlist table linked to user_id
    cursor.execute("DROP TABLE IF EXISTS wishlist;")
    cursor.execute("""
        CREATE TABLE wishlist (
            id INT AUTO_INCREMENT PRIMARY KEY,
            user_id INT,
            product_id INT,
            FOREIGN KEY (user_id) REFERENCES users(id),
            FOREIGN KEY (product_id) REFERENCES products(id)
        );
    """)

    print("Cart and Wishlist tables updated successfully, bhai!")

except Exception as e:
    print(f"Error: {e}")
finally:
    if 'conn' in locals() and conn.is_connected():
        cursor.close()
        conn.close()