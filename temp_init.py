
import app
with app.app.app_context():
    app.init_db()
    print("Database initialized with sample products!")
    print(f"Total products: {app.Product.query.count()}")
