from flask import Flask, render_template, redirect, url_for, request, flash, session,jsonify
from werkzeug.security import generate_password_hash, check_password_hash
import os
from models import db, Product , User
from flask_sqlalchemy import SQLAlchemy
from flask_login import current_user,LoginManager, UserMixin,login_required
from flask_migrate import Migrate




app = Flask(__name__)
app.secret_key = os.environ.get('SECRET_KEY', 'supersecretkey')  # Use environment variable for secret key
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

migrate = Migrate(app, db)

from models import Product, User

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "login"  # Specify the vie



class User(UserMixin, db.Model):
    __tablename__ = 'users'  # Ensure the table name is correct
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(128), nullable=False)
    security_question = db.Column(db.String(255), nullable=False)
    security_answer = db.Column(db.String(128), nullable=False)
    
    # Define the relationship between User and Product using backref
    products = db.relationship('Product', backref='user', lazy=True)


class Product(db.Model):
    __tablename__ = 'products'  # Ensure this matches your database table name
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.String(200), nullable=False)
    price = db.Column(db.Float, nullable=False)
    time_period = db.Column(db.String(50))
    image = db.Column(db.String(200))
    is_added_by_seller = db.Column(db.Boolean, default=False)
    
    # ForeignKey relationship with the User model
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    # The 'user' is automatically set up by backref in the User model




def __repr__(self):
    #return f'<Product {self.name}>'
    return f"Product('{self.name}', '{self.price}')"

with app.app_context():
    db.create_all()  # Create the database and tables




class Order(db.Model):
    __tablename__ = 'orders'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    product_id = db.Column(db.Integer, db.ForeignKey('products.id'), nullable=False)
    quantity = db.Column(db.Integer, nullable=False)
    total_price = db.Column(db.Float, nullable=False)
    status = db.Column(db.String(50), default="Pending")  # Order status, e.g., 'Pending', 'Shipped'

    user = db.relationship('User', backref='orders')
    product = db.relationship('Product', backref='orders')

    def __repr__(self):
        return f"Order('{self.id}', '{self.user_id}', '{self.product_id}', '{self.quantity}', '{self.total_price}')"






@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

def get_products():
    return Product.query.all()

# Function to get added products (may need to adjust if there's a specific condition)
def get_added_products():
    # Assuming you want to fetch all products; modify if you have a specific condition
    #return Product.query.all()
    return Product.query.filter_by(is_added_by_seller=True).all()



# Dummy database for users and products
users = {}



# Home route
@app.route('/')
def home():

    
    products = Product.query.all() 
    products = get_products()  # Get existing products
    added_products = get_added_products()  # Get added products
   # print("Added Products: ", added_products)
   
    
    if 'email' in session:
        return render_template('home.html', products=products , added_products=added_products)
    else:
        flash("Please create an account before logging in.", "danger")
        return redirect(url_for('login'))
    





@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
       
        email = request.form['email']
        password = request.form['password']

        # Fetch the user from the database
        user = User.query.filter_by(email=email).first()

        if user and check_password_hash(user.password, password):
            

            session['email'] = user.email
            
            flash("Log in successfully!", "success")
            return redirect(url_for('home'))
        else:
            flash("Incorrect email or password.", "danger")
            return redirect(url_for('login'))

    return render_template('login.html')





@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        # Get form data
        
        email = request.form['email']
        password = request.form['password']
        security_question = request.form['security_question']
        security_answer = request.form['security_answer']
        
        # Check if all fields are filled
        if not email or not password or not security_question or not security_answer:
            flash("All fields are required.", "error")
            return redirect(url_for('signup'))

        # Hash password and security answer
        hashed_password = generate_password_hash(password)
        hashed_answer = generate_password_hash(security_answer)

        # Check if user already exists in the database
        if User.query.filter_by(email=email).first():
            flash("User already exists! Please login.", "danger")
            return redirect(url_for('login'))
        
        # Create new user instance
        new_user = User(
            email=email,
            password=hashed_password,
            security_question=security_question,
            security_answer=hashed_answer
        )

        # Add user to the database
        try:
            db.session.add(new_user)
            db.session.commit()
            flash("Account created successfully!", "success")
            return redirect(url_for('login'))  # Redirect to login page after successful signup
        except Exception as e:
            db.session.rollback()
            flash(f"Error: {str(e)}", "danger")
            return redirect(url_for('signup'))

    return render_template('signup.html')





@app.route('/logout')
def logout():
    session.pop('email', None)
    flash("Logged out successfully!", "success")
    return redirect(url_for('login'))




@app.route('/cart')
def cart_view():
    # Check if the user is logged in
    if 'email' not in session:
        flash("Please log in to view your cart.", "danger")
        return redirect(url_for('login'))

    # Get the cart from the session
    cart = session.get('cart', [])

    # Calculate the total price of items in the cart
    total_price = sum(item['product'].price * item['quantity'] for item in cart) if cart else 0

    # Render the cart page with the cart items and total price
    return render_template('cart.html', cart=cart, total_price=total_price)






@app.route('/add_to_cart/<int:product_id>', methods=['POST'])
def add_to_cart(product_id):
    if 'email' not in session:
        flash("Please log in to add items to your cart.", "danger")
        return redirect(url_for('login'))

    cart = session.get('cart', [])
    product = Product.query.get(product_id)  # Fetch the product from the database by product_id

    if product:
        # Look for an existing item in the cart
        cart_item = next((item for item in cart if item['product']['id'] == product_id), None)
        if cart_item:
            cart_item['quantity'] += 1  # Increase quantity if already in the cart
        else:
            cart.append({'product': product, 'quantity': 1})  # Add new item with quantity 1
        
        session['cart'] = cart
        flash(f"{product.name} added to cart!", "success")
    else:
        flash("Product not found.", "danger")

    return redirect(url_for('cart_view'))  # Redirect to the cart view



@app.route('/remove_from_cart/<int:product_id>', methods=['POST'])
def remove_from_cart(product_id):
    cart = session.get('cart', [])
    cart = [item for item in cart if item['product']['id'] != product_id]
    session['cart'] = cart  # Update session cart
    flash("Item removed from cart.", "success")
    return redirect(url_for('cart_view'))

@app.route('/update_cart/<int:product_id>', methods=['POST'])
def update_cart(product_id):
    quantity = request.form.get('quantity', type=int)
    cart = session.get('cart', [])
    cart_item = next((item for item in cart if item['product']['id'] == product_id), None)

    if cart_item and quantity > 0:
        cart_item['quantity'] = quantity
        flash("Cart updated successfully!", "success")
    elif cart_item and quantity <= 0:
        cart = [item for item in cart if item['product']['id'] != product_id]
        flash("Item removed from cart.", "success")
    
    session['cart'] = cart  # Update session cart
    return redirect(url_for('cart_view'))





        
@app.route('/forgot_password', methods=['GET', 'POST'])
def forgot_password():
    if request.method == 'POST':
        email = request.form['email']
        security_answer = request.form['security_answer']

        # Fetch the user from the database
        user = User.query.filter_by(email=email).first()
        
        if user and check_password_hash(user.security_answer, security_answer):  # Check if the answer matches
            session['email'] = user.email  # Store email in session
            return redirect(url_for('change_password'))  # Redirect to password change page
        else:
            flash("Incorrect details entered. Please try again.", "danger")
            return redirect(url_for('forgot_password'))

    return render_template('forgot_password.html')



@app.route('/change_password', methods=['GET', 'POST'])
def change_password():
    if 'email' not in session:
        flash("Please log in to change your password.", "danger")
        return redirect(url_for('login'))

    if request.method == 'POST':
        new_password = request.form['new_password']
        confirm_password = request.form['confirm_password']
        email = session['email']

        if new_password != confirm_password:
            flash("New passwords do not match.", "danger")
            return redirect(url_for('change_password'))

        user = User.query.filter_by(email=email).first()
        user.password = generate_password_hash(new_password)  # Update password
        db.session.commit()

        flash("Your password has been changed successfully! Please log in with your new password.", "success")
        session.pop('email', None)  # Clear session
        return redirect(url_for('login'))

    return render_template('change_password.html')






@app.route('/settings')
def settings():
    if 'email' not in session:
        flash("Please log in to view settings.", "danger")
        return redirect(url_for('login'))
    return render_template('settings.html')


@app.route('/seller')
def seller():
    if 'email' not in session:
        flash("Please log in to access seller options.", "danger")
        return redirect(url_for('login'))
    
   
    return render_template('seller.html')


@app.route('/product/<int:product_id>')
def product(product_id):
    # Here you can add logic to fetch product details based on product_id
    return render_template('product.html', product_id=product_id)

@app.route('/privacy')
def privacy():
    return render_template('privacy.html')  # Ensure you have a corresponding HTML template




@app.route('/help')
def help():
    return render_template('help.html')  # Make sure you have this template

@app.route('/search')
def search():
    query = request.args.get('query')
    # Implement search logic here, e.g., filter FAQs or other resources
    return render_template('search_results.html', query=query)


@app.route('/about')
def about():
    return render_template('about.html')  # Make sure you have this template


@app.route('/contact')
def contact():
    return render_template('contact.html')


@app.route('/submit_contact', methods=['POST'])
def submit_contact():
    name = request.form['name']
    email = request.form['email']
    message = request.form['message']
    
    # Process the contact form data (e.g., save to a database, send an email, etc.)
    
    return redirect(url_for('contact'))  # Redirect back to the contact page or to a thank you page




@app.route('/')
def index():
    products = Product.query.all()  # Get all products from the database
    return render_template('index.html', products=products)




@app.route('/test')
def test():
    user = User.query.first()  # Get the first user from the database
    if user:
        user_products = user.products  # Get all products of this user
        return f"User's products: {user_products}"  # Display the user's products
    else:
        return "No user found"



@app.route('/register', methods=['POST'])
def register():
    username = request.form['username']
    email = request.form['email']
    password = request.form['password']  # User's password input
    security_answer = request.form['security_answer']  # User's security answer input

    # Hash the password and security answer before saving the user
    hashed_password = generate_password_hash(password)
    hashed_security_answer = generate_password_hash(security_answer)

    # Create the user instance with the hashed password and security answer
    new_user = User(
        username=username,
        email=email,
        password=hashed_password,
        security_question="What is your mother's name?",  # Use your desired question here
        security_answer=hashed_security_answer
    )

    db.session.add(new_user)
    db.session.commit()

    return redirect(url_for('login'))  # Redirect to login after successful registration




@app.route('/delete_product/<int:product_id>', methods=['POST'])
def delete_product(product_id):
    if 'email' not in session:
        flash("Please log in to delete products.", "danger")
        return redirect(url_for('login'))

    # Fetch the product from the database by product_id
    product = Product.query.get(product_id)

    if product is None:
        flash("Product not found.", "danger")
        return redirect(url_for('home'))

    # Print product details for debugging
    print(f"Attempting to delete Product: {product.name}, Seller: {product.seller_email}")
    
    # Check if the logged-in user is the seller of the product
    if product.seller_email == session['email']:
        try:
            db.session.delete(product)  # Delete the product from the database
            db.session.commit()  # Commit the changes to the database
            flash(f"Product {product.name} has been deleted successfully.", "success")
        except Exception as e:
            db.session.rollback()  # Rollback if something goes wrong
            print(f"Error deleting product: {str(e)}")  # Print the error for debugging
            flash(f"An error occurred while deleting the product: {str(e)}", "danger")
    else:
        flash("You are not authorized to delete this product.", "danger")

    # Redirect to the seller page (or home page) after deletion
    return redirect(url_for('seller_page'))  # Or redirect to the home page if needed













#@app.route('/delete_product/<int:product_id>', methods=['POST'])
#def delete_product(product_id):
 #   if not current_user.is_authenticated:
  #      flash("Please log in to access this page.", "warning")
   #     return redirect(url_for('login'))

    ## Proceed with the deletion
    #product = Product.query.get(product_id)

    #if product is None:
     #   flash("Product not found.", "danger")
      #  return redirect(url_for('home'))

    ## Proceed with the deletion
    #try:
     #   db.session.delete(product)
      #  db.session.commit()
       # flash("Product deleted successfully.", "success")
  #  except Exception as e:
   #     db.session.rollback()  # Rollback if something goes wrong
    #    flash(f"An error occurred: {str(e)}", "danger")

    #return redirect(url_for('home'))


 #   #db.session.delete(product)
  #  #db.session.commit()
   # #flash("Product deleted successfully.", "success")
    
   # #return redirect(url_for('home'))  # This will take the user back to the home page







@app.route('/add_product', methods=['POST', 'GET'])
@login_required  # Optional: This replaces the manual login check
def add_product():
    # Handle product creation logic
    if request.method == 'POST':
        # Code to create and save the product
        new_product = Product(name=request.form['name'], user_id=current_user.id)
        db.session.add(new_product)
        db.session.commit()
        flash("Product added successfully!", "success")
        return redirect(url_for('home'))
    
    return render_template('add_product.html')


@app.route('/edit_product/<int:product_id>', methods=['POST', 'GET'])
@login_required  # Optional: This replaces the manual login check
def edit_product(product_id):
    product = Product.query.get_or_404(product_id)
    
    # Ensure the logged-in user owns the product
    if product.user_id != current_user.id:
        flash("You do not have permission to edit this product", "danger")
        return redirect(url_for('home'))
    
    if request.method == 'POST':
        # Handle product editing logic
        product.name = request.form['name']
        db.session.commit()
        flash("Product updated successfully!", "success")
        return redirect(url_for('home'))
    
    return render_template('edit_product.html', product=product)



@app.route('/place_order', methods=['POST'])
def place_order():
    if 'email' not in session:
        flash("Please log in to place an order.", "danger")
        return redirect(url_for('login'))

    cart = session.get('cart', [])
    if not cart:
        flash("Your cart is empty. Add products before placing an order.", "danger")
        return redirect(url_for('cart_view'))

    user = User.query.filter_by(email=session['email']).first()

    total_price = sum(item['product'].price * item['quantity'] for item in cart)
    
    try:
        # Create an order for each product in the cart
        for item in cart:
            order = Order(
                user_id=user.id,
                product_id=item['product'].id,
                quantity=item['quantity'],
                total_price=item['product'].price * item['quantity']
            )
            db.session.add(order)

        db.session.commit()

        # Clear the cart after placing the order
        session['cart'] = []

        flash(f"Your order has been placed successfully! Total: ${total_price}", "success")
        return redirect(url_for('home'))
    except Exception as e:
        db.session.rollback()
        flash(f"Error while placing the order: {str(e)}", "danger")
        return redirect(url_for('cart_view'))




@app.route('/chatbot')
def chatbot():
    # Logic to render chatbot interface
    return render_template('chatbot_ui.html')





@app.route('/chatbot')
def chatbot_ui():
    return render_template('chatbot_ui.html')









if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True) 