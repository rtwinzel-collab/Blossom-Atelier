import sqlite3

db_file = "flower_shop.db"
conn = sqlite3.connect(db_file)
cursor = conn.cursor()

# Inventory Table
cursor.execute('''
    CREATE TABLE IF NOT EXISTS inventory (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        item_name TEXT UNIQUE NOT NULL,
        category TEXT NOT NULL,
        type TEXT NOT NULL,
        stock INTEGER NOT NULL,
        price REAL NOT NULL
    )
''')

# POS Sales History Table
cursor.execute('''
    CREATE TABLE IF NOT EXISTS pos_sales (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        item_name TEXT NOT NULL,
        quantity INTEGER NOT NULL,
        total_price REAL NOT NULL,
        payment_method TEXT DEFAULT 'Cash',
        date_created TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
''')

# Event Bookings Table
cursor.execute('''
    CREATE TABLE IF NOT EXISTS event_bookings (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        client_name TEXT NOT NULL,
        contact_num TEXT NOT NULL,
        event_type TEXT NOT NULL,
        event_date TEXT NOT NULL,
        package TEXT NOT NULL,
        custom_notes TEXT,
        payment_method TEXT DEFAULT 'Cash',
        status TEXT DEFAULT 'Pending',
        total_amount REAL NOT NULL,
        date_created TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
''')

items = [
    ("Ecuadorian Red Roses (Per Stem)", "Fresh Flowers", "Fresh", 150, 120.0),
    ("Dutch White Tulips (Per Stem)", "Fresh Flowers", "Fresh", 100, 150.0),
    ("Sunflowers (Per Stem)", "Fresh Flowers", "Fresh", 80, 90.0),
    ("Pink Carnations (Per Bunch)", "Fresh Flowers", "Fresh", 60, 250.0),
    ("Purple Phalaenopsis Orchids", "Fresh Flowers", "Fresh", 40, 450.0),
    ("Stargazer White Lilies", "Fresh Flowers", "Fresh", 50, 300.0),
    ("Baby's Breath / Gypsophila (Per Bundle)", "Fresh Flowers", "Fresh", 120, 200.0),
    ("Peonies Premium (Per Stem)", "Fresh Flowers", "Fresh", 30, 380.0),
    ("Soft Blue Hydrangeas (Per Stem)", "Fresh Flowers", "Fresh", 35, 350.0),
    ("Custom Fresh Flower Bouquet Arrangement", "Fresh Flowers", "Fresh", 999, 1500.0),
    ("Premium Silk Red Roses Bouquet", "Artificial Flowers", "Artificial", 50, 850.0),
    ("Velvet Artificial Tulips Set", "Artificial Flowers", "Artificial", 40, 650.0),
    ("Forever Sunflowers (Faux Silk)", "Artificial Flowers", "Artificial", 60, 450.0),
    ("Dried Preserved Flower Bouquet in Glass Dome", "Artificial Flowers", "Artificial", 25, 1800.0),
    ("Artificial Orchid Pot Arrangement", "Artificial Flowers", "Artificial", 30, 1200.0),
    ("Custom Artificial / Dried Floral Box", "Artificial Flowers", "Artificial", 999, 1250.0),
    ("Ceremony Floral Arch Structure Setup", "Decors & Hardware", "Decor", 10, 4500.0),
    ("Aisle Runner & Standing Flower Racks (Pair)", "Decors & Hardware", "Decor", 12, 2800.0),
    ("Luxury Crystal Glass Vase Set", "Decors & Hardware", "Decor", 30, 350.0),
    ("Aesthetic Flower Box & Ribbon Set", "Decors & Hardware", "Decor", 50, 250.0)
]

for item in items:
    cursor.execute('''
        INSERT OR IGNORE INTO inventory (item_name, category, type, stock, price)
        VALUES (?, ?, ?, ?, ?)
    ''', item)

conn.commit()
conn.close()
print("Database created successfully!")