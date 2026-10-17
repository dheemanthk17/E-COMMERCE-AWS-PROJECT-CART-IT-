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

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS orders (
            id INT AUTO_INCREMENT PRIMARY KEY,
            user_id INT,
            items_summary TEXT,
            total_price VARCHAR(50),
            payment_method VARCHAR(50),
            delivery_details TEXT,
            status VARCHAR(100) DEFAULT 'Processing - Preparing to Dispatch',
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES users(id)
        );
    """)

    print("Orders table created successfully")

except Exception as e:
    print(f"Error: {e}")
finally:
    if 'conn' in locals() and conn.is_connected():
        cursor.close()
        conn.close()