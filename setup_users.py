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

    # Create the users table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INT AUTO_INCREMENT PRIMARY KEY,
            username VARCHAR(100) UNIQUE NOT NULL,
            email VARCHAR(255) UNIQUE NOT NULL,
            password VARCHAR(255) NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );
    """)

    print("Users table created successfully!")

except Exception as e:
    print(f"Error: {e}")
finally:
    if 'conn' in locals() and conn.is_connected():
        cursor.close()
        conn.close()