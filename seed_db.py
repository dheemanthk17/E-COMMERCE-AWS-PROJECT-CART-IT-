import mysql.connector

# The complete 31-item catalog
catalog = [
    { "category": "Mobiles", "name": "Apple iPhone 15 Pro Titanium", "price": "₹1,34,900", "image": "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcT8qGVgq7CaWEAvsghzNU9hLtF44EnczjrU43B-3T8dtg&s" },
    { "category": "Mobiles", "name": "Apple iPhone 17 Pro Max", "price": "₹2,50,000", "image": "https://www.apple.com/newsroom/images/2025/09/apple-unveils-iphone-17-pro-and-iphone-17-pro-max/article/Apple-iPhone-17-Pro-camera-close-up-250909_big.jpg.large_2x.jpg" },
    { "category": "Mobiles", "name": "Samsung Galaxy S24 Ultra", "price": "₹1,29,999", "image": "https://images.unsplash.com/photo-1610945415295-d9bbf067e59c?w=500" },
    { "category": "Mobiles", "name": "Samsung Galaxy Z Fold 5", "price": "₹1,54,999", "image": "https://www.designinfo.in/wp-content/uploads/2024/07/275464_0_idt1q1.webp" },
    { "category": "Mobiles", "name": "Google Pixel 8 Pro Obsidian", "price": "₹1,06,999", "image": "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcR4qlyASsM0lfSQR_UavzDNM_eLzc63fexRidVEs8mksA&s=10" },
    { "category": "Mobiles", "name": "Nothing Phone (2) Dark", "price": "₹44,999", "image": "https://m.media-amazon.com/images/I/61cZJcKweLL._AC_UF1000,1000_QL80_.jpg" },
    { "category": "Laptops", "name": "Apple MacBook Pro 16-inch M3", "price": "₹2,49,900", "image": "https://images.unsplash.com/photo-1517336714731-489689fd1ca8?w=500" },
    { "category": "Laptops", "name": "Dell XPS 15 OLED", "price": "₹1,89,000", "image": "https://images.unsplash.com/photo-1593642632823-8f785ba67e45?w=500" },
    { "category": "Laptops", "name": "Lenovo ThinkPad X1 Carbon", "price": "₹1,55,000", "image": "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcRv02CsUYnLh82GAQsfXMWPS0WC9RokK8x8_rJxRYt-HUDKnSFbVG4e7RY&s=10" },
    { "category": "Laptops", "name": "Asus ROG Zephyrus G14", "price": "₹1,75,000", "image": "https://images.unsplash.com/photo-1603302576837-37561b2e2302?w=500" },
    { "category": "Supplements", "name": "Whey Protein Isolate 2kg", "price": "₹2,400", "image": "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcTKNQ7Jb-WNcMqsGqNh_dxziaWCx6K_3ULDMz-HgZovEA&s=10" },
    { "category": "Supplements", "name": "Creatine Monohydrate Powder", "price": "₹850", "image": "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcR9TGadN_nPn9miX-qK9YetLN7Kpu3Pygcw4cAc0q45cA&s=10"},
    { "category": "Supplements", "name": "High-Protein Peanut Butter", "price": "₹450", "image": "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcQBkecs6CyW886qCLtTA1A4oPsTvRxeD3zr__o7Bdvv8g&s=10" },
    { "category": "Supplements", "name": "Rolled Oats 1kg Pack", "price": "₹300", "image": "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcT7HwwJPEwhHK15AqCsGCmh4zG6oLQIp-ux3m67mqnQ1A&s=10" },
    { "category": "Supplements", "name": "Soya Chunks High Protein", "price": "₹150", "image": "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcQMwnx0BRHWGbz1LAhKIQU8I-KcBylQVNWfskTw6Hn4wg&s" },
    { "category": "Books", "name": "Python Object-Oriented Programming", "price": "₹1,200", "image": "https://images.unsplash.com/photo-1526379095098-d400fd0bf935?w=500" },
    { "category": "Books", "name": "Linux Red Hat Administration", "price": "₹950", "image": "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcQPKE61DWzATS4cpL4A1eCZzkT1cMWyEsCzFk7r4_MdAQ&s=10" },
    { "category": "Books", "name": "A Game of Thrones (Hardcover)", "price": "₹850", "image": "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcQCRq9_aEGHc7BEcVHw953KULMET-XCY5U6-0R-cHD6i3JyGot8uHWqkdY&s=10" },
    { "category": "Books", "name": "Harry Potter & The Sorcerer's Stone", "price": "₹600", "image": "https://res.cloudinary.com/bloomsbury-atlas/image/upload/w_360,c_scale,dpr_1.5/jackets/9781408855652.jpg" },
    { "category": "Books", "name": "Atomic Habits by James Clear", "price": "₹450", "image": "https://images.unsplash.com/photo-1589829085413-56de8ae18c73?w=500" },
    { "category": "Clothes", "name": "White Premium Cotton Shirt", "price": "₹899", "image": "https://images.unsplash.com/photo-1521572163474-6864f9cf17ab?w=500" },
    { "category": "Clothes", "name": "Navy Blue Casual Polo", "price": "₹1,100", "image": "https://13thirtystudios.com/cdn/shop/files/13THIRTY_ClubHouse_NavyPiquePolo_Front_02.png?v=1779215237&width=990" },
    { "category": "Clothes", "name": "Black Essential T-Shirt", "price": "₹650", "image": "https://images.unsplash.com/photo-1583743814966-8936f5b7be1a?w=500" },
    { "category": "Clothes", "name": "Maroon Henley Long Sleeve", "price": "₹950", "image": "https://encrypted-tbn1.gstatic.com/shopping?q=tbn:ANd9GcTgLHakcqPwOKt9Y2CaSntnTS17SiN9YJcjDKmdcEtlQyBGUUZNw4UZB2sOpSjmtPVu1-fh5UYL2rrAJ6lM8xzOGlQ0K17D8HTLeYeXXso" },
    { "category": "Clothes", "name": "Slim Fit Blue Denim Jeans", "price": "₹2,200", "image": "https://images.unsplash.com/photo-1542272604-787c3835535d?w=500" },
    { "category": "Clothes", "name": "Black Cotton Chinos", "price": "₹1,800", "image": "https://images.unsplash.com/photo-1624378439575-d8705ad7ae80?w=500" },
    { "category": "Clothes", "name": "Grey Activewear Joggers", "price": "₹1,400", "image": "https://images.unsplash.com/photo-1517438476312-10d79c077509?w=500" },
    { "category": "Shoes", "name": "Nike Air Max Red/Black", "price": "₹8,500", "image": "https://images.unsplash.com/photo-1542291026-7eec264c27ff?w=500" },
    { "category": "Shoes", "name": "Adidas Ultraboost White", "price": "₹11,000", "image": "https://encrypted-tbn2.gstatic.com/shopping?q=tbn:ANd9GcTFeG0wBtPzLlark8R5A0qOVuqs51ZnJ1O3dhDYORUmBzkn6CYtjBHNlcFCfmlhuq736sNd4VMQMezeCad0ugAT0RNQLcd1XIW3QOp3hGvIVMT3P9yx8yj8oc0dvXZ_wDRDtg70rkY&usqp=CAc" },
    { "category": "Shoes", "name": "Puma RS-X Multicolor", "price": "₹6,500", "image": "https://images.unsplash.com/photo-1608231387042-66d1773070a5?w=500" },
    { "category": "Shoes", "name": "Nike Air jordan", "price": "₹12,500", "image": "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcQCOHuk7a8Z_Fo51JLQGnk0RYMlV4xjhz1Imdzgo5siMA&s=10" }
]

try:
    conn = mysql.connector.connect(
        host='cart-it-db.cvq0ec8i6o9q.ap-south-1.rds.amazonaws.com',
        database='cart_it_store',
        user='admin',
        password='YOUR_PASSWORD',
        ssl_ca='./global-bundle.pem'
    )
    cursor = conn.cursor()

    # Clear old data so we don't get duplicates
    cursor.execute("DELETE FROM products;")

    # Insert all 31 items
    for item in catalog:
        cursor.execute(
            "INSERT INTO products (category, name, price, image_url) VALUES (%s, %s, %s, %s)",
            (item['category'], item['name'], item['price'], item['image'])
        )

    conn.commit()
    print(f"Success! {cursor.rowcount} products added to the database.")

except Exception as e:
    print(f"Error: {e}")
finally:
    if 'conn' in locals() and conn.is_connected():
        cursor.close()
        conn.close()