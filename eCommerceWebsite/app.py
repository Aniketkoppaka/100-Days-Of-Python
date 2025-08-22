from flask import Flask, render_template, request, redirect, url_for, session, flash
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash
import stripe
import os
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)

app.config['SECRET_KEY'] = os.getenv('FLASK_SECRET_KEY')
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///shop.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

stripe.api_key = os.getenv('STRIPE_SECRET_KEY')
stripe_publishable_key = os.getenv('STRIPE_PUBLISHABLE_KEY')

class User(UserMixin, db.Model):
    """User model for authentication."""
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(150), unique=True, nullable=False)
    password_hash = db.Column(db.String(150), nullable=False)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

class Product(db.Model):
    """Product model for items in the store."""
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    price = db.Column(db.Float, nullable=False)
    description = db.Column(db.Text, nullable=False)
    image_file = db.Column(db.String(30), nullable=False, default='default.jpg')
    stripe_price_id = db.Column(db.String(100))

@login_manager.user_loader
def load_user(user_id):
    """Loads user for Flask-Login."""
    return User.query.get(int(user_id))

@app.route('/')
def home():
    """Renders the home page with all products."""
    products = Product.query.all()
    return render_template('index.html', products=products)

@app.route('/product/<int:product_id>')
def product(product_id):
    """Renders the product detail page."""
    product = Product.query.get_or_404(product_id)
    return render_template('product.html', product=product)

@app.route('/register', methods=['GET', 'POST'])
def register():
    """Handles user registration."""
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = User.query.filter_by(username=username).first()
        if user:
            flash('Username already exists.', 'danger')
            return redirect(url_for('register'))
        new_user = User(username=username)
        new_user.set_password(password)
        db.session.add(new_user)
        db.session.commit()
        flash('Registration successful! Please log in.', 'success')
        return redirect(url_for('login'))
    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    """Handles user login."""
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = User.query.filter_by(username=username).first()
        if user and user.check_password(password):
            login_user(user, remember=True)
            return redirect(url_for('home'))
        else:
            flash('Login Unsuccessful. Please check username and password', 'danger')
    return render_template('login.html')

@app.route('/logout')
@login_required
def logout():
    """Handles user logout."""
    logout_user()
    return redirect(url_for('home'))

@app.route('/add_to_cart/<int:product_id>')
def add_to_cart(product_id):
    """Adds a product to the shopping cart."""
    product = Product.query.get_or_404(product_id)
    cart = session.get('cart', {})

    cart[str(product_id)] = cart.get(str(product_id), 0) + 1

    session['cart'] = cart
    flash(f'{product.name} has been added to your cart!', 'success')
    return redirect(request.referrer or url_for('home'))

@app.route('/cart')
def view_cart():
    """Displays the shopping cart."""
    cart = session.get('cart', {})
    cart_items = []
    total_price = 0

    for product_id, quantity in cart.items():
        product = Product.query.get(product_id)
        if product:
            item_total = product.price * quantity
            cart_items.append({
                'id': product.id,
                'name': product.name,
                'price': product.price,
                'quantity': quantity,
                'image_file': product.image_file,
                'item_total': item_total
            })
            total_price += item_total

    return render_template('cart.html', cart_items=cart_items, total_price=total_price)

@app.route('/remove_from_cart/<int:product_id>')
def remove_from_cart(product_id):
    """Removes an item from the cart."""
    cart = session.get('cart', {})
    if str(product_id) in cart:
        del cart[str(product_id)]
        session['cart'] = cart
        flash('Item removed from cart.', 'info')
    return redirect(url_for('view_cart'))

@app.route('/update_cart/<int:product_id>', methods=['POST'])
def update_cart(product_id):
    """Updates the quantity of an item in the cart."""
    cart = session.get('cart', {})
    quantity = int(request.form.get('quantity', 1))

    if str(product_id) in cart:
        if quantity > 0:
            cart[str(product_id)] = quantity
        else:
            del cart[str(product_id)]
        session['cart'] = cart

    return redirect(url_for('view_cart'))

@app.route('/create-checkout-session')
def create_checkout_session():
    """Creates a Stripe checkout session and redirects the user."""
    cart = session.get('cart', {})
    line_items = []

    for product_id, quantity in cart.items():
        product = Product.query.get(product_id)
        if product and product.stripe_price_id:
            line_items.append({
                'price': product.stripe_price_id,
                'quantity': quantity,
            })

    if not line_items:
        flash('Your cart is empty.', 'warning')
        return redirect(url_for('view_cart'))

    try:
        checkout_session = stripe.checkout.Session.create(
            payment_method_types=['card'],
            line_items=line_items,
            mode='payment',
            success_url=url_for('success', _external=True) + '?session_id={CHECKOUT_SESSION_ID}',
            cancel_url=url_for('cancel', _external=True),
        )
        return redirect(checkout_session.url, code=303)
    except Exception as e:
        flash(f'Error creating checkout session: {e}', 'danger')
        return redirect(url_for('view_cart'))

@app.route('/success')
def success():
    """Handles successful payment."""
    session.pop('cart', None)
    return render_template('success.html')

@app.route('/cancel')
def cancel():
    """Handles canceled payment."""
    return render_template('cancel.html')

def setup_database(app):
    with app.app_context():
        db.create_all()
        if Product.query.count() == 0:
            products = [
                Product(name='Shadowfang Katana', price=250.00,
                        description='Forged in darkness, this blade is said to absorb the light around it. Its edge is unnaturally sharp.',
                        image_file='katana_shadowfang.jpg',
                        stripe_price_id='price_1RyzGZ5KWotXcEzfBXys0wED'),
                Product(name='Stormcaller Katana', price=320.50,
                        description='A legendary blade that hums with the power of a brewing storm. The steel has a unique, cloudy pattern.',
                        image_file='katana_stormcaller.jpg',
                        stripe_price_id='price_1RyzKx5KWotXcEzfoloFAy01'),
                Product(name='Gilded Moonveil', price=450.00,
                        description='An ornate and deadly weapon. The handle is wrapped in gold leaf, and the blade glows faintly in moonlight.',
                        image_file='katana_moonveil.jpg',
                        stripe_price_id='price_1RyzPS5KWotXcEzfuUt1WWkp'),
                Product(name='Crimson Edge Nodachi', price=380.00,
                        description='A longer, two-handed field katana. The blade has a distinctive red temper line, a mark of its master smith.',
                        image_file='katana_crimson_edge.jpg',
                        stripe_price_id='price_1RyzSB5KWotXcEzfTpRLoqrU'),
            ]
            db.session.bulk_save_objects(products)
            db.session.commit()
        print("Database and products are set up.")


if __name__ == '__main__':
    setup_database(app)
    app.run(debug=True)
