from flask import Flask, render_template, request, redirect, url_for, flash, session, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, IntegerField, SubmitField
from wtforms.validators import DataRequired, Email, NumberRange, Length
from datetime import datetime
import os
import time

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your-secret-key-here'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///yourpalette.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# Add cache busting for static files
@app.context_processor
def override_url_for():
    return dict(url_for=dated_url_for)

def dated_url_for(endpoint, **values):
    if endpoint == 'static':
        filename = values.get('filename', None)
        if filename:
            file_path = os.path.join(app.root_path, endpoint, filename)
            try:
                values['q'] = int(os.stat(file_path).st_mtime)
            except OSError:
                values['q'] = int(time.time())
    return url_for(endpoint, **values)

# Models
class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=False)
    price = db.Column(db.Numeric(10, 2), nullable=False)
    image_url = db.Column(db.String(200), nullable=False)
    stock_quantity = db.Column(db.Integer, default=0)
    category = db.Column(db.String(50), nullable=False)
    brand = db.Column(db.String(50), nullable=False)
    
    def __repr__(self):
        return f'<Product {self.name}>'

class Order(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    customer_name = db.Column(db.String(100), nullable=False)
    customer_email = db.Column(db.String(120), nullable=False)
    customer_phone = db.Column(db.String(20), nullable=False)
    customer_address = db.Column(db.Text, nullable=False)
    order_date = db.Column(db.DateTime, default=datetime.utcnow)
    total_amount = db.Column(db.Numeric(10, 2), nullable=False)
    
    order_details = db.relationship('OrderDetail', backref='order', lazy=True)
    
    def __repr__(self):
        return f'<Order {self.id}>'

class OrderDetail(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    order_id = db.Column(db.Integer, db.ForeignKey('order.id'), nullable=False)
    product_id = db.Column(db.Integer, db.ForeignKey('product.id'), nullable=False)
    quantity = db.Column(db.Integer, nullable=False)
    price = db.Column(db.Numeric(10, 2), nullable=False)
    
    product = db.relationship('Product', backref='order_details', lazy=True)
    
    def __repr__(self):
        return f'<OrderDetail {self.id}>'

# Forms
class SearchForm(FlaskForm):
    search = StringField('Search Products', validators=[Length(max=100)])
    submit = SubmitField('Search')

class CheckoutForm(FlaskForm):
    name = StringField('Full Name', validators=[DataRequired(), Length(min=2, max=100)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    phone = StringField('Phone Number', validators=[DataRequired(), Length(min=10, max=20)])
    address = TextAreaField('Address', validators=[DataRequired(), Length(min=10, max=500)])
    submit = SubmitField('Complete Order')

# Routes
@app.route('/')
def home():
    search_form = SearchForm()
    search_query = request.args.get('search', '')
    category_filter = request.args.get('category', '')
    price_range = request.args.get('price_range', '')
    stock_filter = request.args.get('stock_filter', '')
    
    # Start with base query
    query = Product.query
    
    # Apply search filter
    if search_query:
        query = query.filter(
            Product.name.contains(search_query) | 
            Product.description.contains(search_query)
        )
    
    # Apply category filter
    if category_filter:
        query = query.filter(Product.category == category_filter)
    
    # Apply price range filter
    if price_range:
        if price_range == '0-15':
            query = query.filter(Product.price < 15)
        elif price_range == '15-25':
            query = query.filter(Product.price >= 15, Product.price <= 25)
        elif price_range == '25-35':
            query = query.filter(Product.price >= 25, Product.price <= 35)
        elif price_range == '35+':
            query = query.filter(Product.price > 35)
    
    # Apply stock filter
    if stock_filter:
        if stock_filter == 'in_stock':
            query = query.filter(Product.stock_quantity > 0)
        elif stock_filter == 'low_stock':
            query = query.filter(Product.stock_quantity <= 10, Product.stock_quantity > 0)
        elif stock_filter == 'high_stock':
            query = query.filter(Product.stock_quantity > 20)
    
    products = query.all()
    
    return render_template('index.html', 
                         products=products, 
                         search_form=search_form, 
                         search_query=search_query)

@app.route('/product/<int:product_id>')
def product_detail(product_id):
    product = Product.query.get_or_404(product_id)
    related_products = Product.query.filter(Product.id != product_id).limit(4).all()
    return render_template('product_detail.html', product=product, related_products=related_products)

@app.route('/add_to_basket', methods=['POST'])
def add_to_basket():
    product_id = request.form.get('product_id')
    quantity = int(request.form.get('quantity', 1))
    
    if 'basket' not in session:
        session['basket'] = {}
    
    basket = session['basket']
    
    if str(product_id) in basket:
        basket[str(product_id)] += quantity
    else:
        basket[str(product_id)] = quantity
    
    session['basket'] = basket
    flash('Product added to basket successfully!', 'success')
    
    return redirect(request.referrer or url_for('home'))

@app.route('/basket')
def basket():
    basket_items = []
    total = 0
    
    if 'basket' in session:
        for product_id, quantity in session['basket'].items():
            product = Product.query.get(int(product_id))
            if product:
                item_total = float(product.price) * quantity
                basket_items.append({
                    'product': product,
                    'quantity': quantity,
                    'total': item_total
                })
                total += item_total
    
    # Create a dummy form for CSRF token
    form = SearchForm()
    
    return render_template('basket.html', basket_items=basket_items, total=total, form=form)

@app.route('/remove_from_basket/<int:product_id>')
def remove_from_basket(product_id):
    if 'basket' in session:
        basket = session['basket']
        if str(product_id) in basket:
            del basket[str(product_id)]
            session['basket'] = basket
            flash('Product removed from basket', 'info')
    
    return redirect(url_for('basket'))

@app.route('/update_basket_quantity', methods=['POST'])
def update_basket_quantity():
    try:
        data = request.get_json()
        product_id = str(data.get('product_id'))
        new_quantity = int(data.get('quantity'))
        
        if 'basket' not in session:
            return jsonify({'success': False, 'error': 'No basket found'})
        
        if new_quantity < 1 or new_quantity > 10:
            return jsonify({'success': False, 'error': 'Invalid quantity'})
        
        basket = session['basket']
        
        if product_id not in basket:
            return jsonify({'success': False, 'error': 'Product not in basket'})
        
        # Update quantity
        basket[product_id] = new_quantity
        session['basket'] = basket
        
        # Calculate totals
        product = Product.query.get(int(product_id))
        item_total = float(product.price) * new_quantity
        
        basket_total = 0
        basket_count = 0
        for pid, qty in basket.items():
            p = Product.query.get(int(pid))
            if p:
                basket_total += float(p.price) * qty
                basket_count += qty
        
        return jsonify({
            'success': True,
            'item_total': item_total,
            'basket_total': basket_total,
            'basket_count': basket_count
        })
        
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)})

@app.route('/checkout', methods=['GET', 'POST'])
def checkout():
    form = CheckoutForm()
    
    if 'basket' not in session or not session['basket']:
        flash('Your basket is empty', 'warning')
        return redirect(url_for('home'))
    
    if form.validate_on_submit():
        # Create order
        order = Order(
            customer_name=form.name.data,
            customer_email=form.email.data,
            customer_phone=form.phone.data,
            customer_address=form.address.data,
            order_date=datetime.utcnow(),
            total_amount=0
        )
        
        db.session.add(order)
        db.session.flush()
        
        total_amount = 0
        
        # Create order details
        for product_id, quantity in session['basket'].items():
            product = Product.query.get(int(product_id))
            if product:
                order_detail = OrderDetail(
                    order_id=order.id,
                    product_id=product.id,
                    quantity=quantity,
                    price=product.price
                )
                db.session.add(order_detail)
                total_amount += float(product.price) * quantity
        
        # Update order total
        order.total_amount = total_amount
        db.session.commit()
        
        # Clear basket
        session.pop('basket', None)
        
        flash(f'Order #{order.id} completed successfully! Thank you for your purchase.', 'success')
        return redirect(url_for('order_confirmation', order_id=order.id))
    
    # Calculate total and get basket items for display
    total = 0
    basket_items = []
    if 'basket' in session:
        for product_id, quantity in session['basket'].items():
            product = Product.query.get(int(product_id))
            if product:
                item_total = float(product.price) * quantity
                basket_items.append({
                    'product': product,
                    'quantity': quantity,
                    'total': item_total
                })
                total += item_total
    
    return render_template('checkout.html', form=form, total=total, basket_items=basket_items)

@app.route('/order_confirmation/<int:order_id>')
def order_confirmation(order_id):
    order = Order.query.get_or_404(order_id)
    return render_template('order_confirmation.html', order=order)

# Initialize database and add sample data
def init_db():
    db.create_all()
    
    # Check if products already exist
    if Product.query.count() == 0:
        products = [
            Product(
                name='Professional Makeup Mixing Palette',
                description='Professional-grade stainless steel mixing palette perfect for creating custom makeup shades.',
                price=18.99,
                image_url='img/makeup-palette.jpg',
                stock_quantity=23,
                category='Palettes',
                brand='Beauty of Joseon'
            ),
            Product(
                name='Korean Spatula',
                description='Stainless Steel Spatula for smooth foundation application',
                price=24.99,
                image_url='img/korean-spatula.jpg',
                stock_quantity=15,
                category='Spatulas',
                brand='Beauty of Joseon'
            ),
            Product(
                name='Mini Palette',
                description='Miniature version of the infamous mixing palette',
                price=12.50,
                image_url='img/mini-palette.jpg',
                stock_quantity=30,
                category='Palettes',
                brand='Beauty of Joseon'
            ),
            Product(
                name='Lip Kit',
                description='Lip pick with included spatula for easy application',
                price=15.75,
                image_url='img/lip-kit.jpg',
                stock_quantity=20,
                category='Lip Tools',
                brand='Beauty of Joseon'
            ),
            Product(
                name='LED Compact Mirror',
                description='Portable mirror with LED lighting for perfect makeup application',
                price=32.00,
                image_url='img/led-mirror.jpg',
                stock_quantity=12,
                category='Accessories',
                brand='Beauty of Joseon'
            )
        ]
        
        for product in products:
            db.session.add(product)
        
        db.session.commit()

if __name__ == '__main__':
    with app.app_context():
        init_db()
    app.run(debug=True)