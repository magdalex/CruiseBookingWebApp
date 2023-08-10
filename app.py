import csv

import bcrypt
from flask import Flask, render_template, redirect, flash, session, url_for
from flask_sqlalchemy import SQLAlchemy
from forms import LoginForm, RegisterForm
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from data import line_list, line_images, line_intros, detail_images, line_details
import secrets
from datetime import date

app = Flask(__name__)
secret_key = secrets.token_hex(16)
app.config['SECRET_KEY'] = secret_key

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'
app.config['SQLALCHEMY_DATABASE_URI'] = r'sqlite:///testdatabaseUPDATE2.sqlite'
db = SQLAlchemy(app)

from models import Customer, Card, Cart, ProductCart, Product, Purchases


@app.route('/')
def index():
    allproducts = Product.query.all()
    num_rows = len(allproducts) // 3 + bool(len(allproducts) % 3)
    return render_template('base.html', allproducts=allproducts, num_rows=num_rows, min=min)


class SessionUser(UserMixin):
    def __init__(self, customer_email, customer_first_name, customer_last_name, customer_phone, customer_password=None):
        self.id = customer_email
        self.first_name = customer_first_name
        self.last_name = customer_last_name
        self.phone = customer_phone
        self.password = customer_password


@login_manager.user_loader
def load_user(user_id):
    user = find_user(user_id)
    if user:
        user.password = None
    return user


def find_user(email):
    res = Customer.query.get(email)
    if res:
        user = SessionUser(res.customer_email, res.customer_first_name, res.customer_last_name, res.customer_phone,
                           res.customer_password)
    else:
        user = None
    return user


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = find_user(form.email.data)
        if user and bcrypt.checkpw(form.password.data.encode(), user.password.encode()):
            login_user(user)
            next_page = session.get('next', '/')
            session['next'] = '/'
            return redirect(next_page)
        else:
            flash('Error. Try again.')
    return render_template('login.html', form=form, customer_email=session.get('customer_email'))


@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        user = find_user(form.email.data)
        if not user:
            cart = Cart()  # creating user related cart
            db.session.add(cart)
            db.session.commit()
            salt = bcrypt.gensalt()
            password = bcrypt.hashpw(form.password.data.encode(), salt)
            user = Customer(customer_email=form.email.data, customer_first_name=form.first_name.data,
                            customer_last_name=form.last_name.data, customer_phone=form.phone.data,
                            customer_password=password.decode(), cart_id=cart.cart_id)
            # TODO: Denis, this doesn't get saved into user and isn't displayed. Make the association
            card = Card(customer_email=form.email.data, card_number=form.card_number.data,
                        card_issuer=form.credit_card.data,
                        card_name=form.cardholder_name.data, card_expiry_month=form.expiration_month.data,
                        card_expiry_year=form.expiration_year.data, card_cvv=form.cvv.data)
            db.session.add(user)
            db.session.add(card)
            db.session.commit()
            return redirect('/login')
        else:
            flash('Email already in use')
    return render_template('register.html', form=form)


@app.route('/account', methods=['GET', 'PUT'])
@login_required
def account():
    email = current_user.id
    card = Card.query.filter_by(customer_email=email).one()
    try:
        purchases = Purchases.query.filter_by(purchase_customer_email=current_user.id).all()
        for p in purchases:
            product_price = Product.query.filter_by(product_id=p.purchase_product_id).all()
        else:
            product_price = None
    except:
        purchases = None
        product_price = None

    return render_template('account.html', customer_email=session.get('customer_email'),
                           customer_first_name=session.get('customer_first_name'),
                           customer_last_name=session.get('customer_last_name'),
                           customer_phone=session.get('customer_phone'),
                           # TODO: Dennis, this doesn't get saved into user and isn't displayed. Make the association
                           card_number=card.card_number,
                           card_name=card.card_name,
                           card_issuer=card.card_issuer,
                           card_expiry_month=card.card_expiry_month,
                           card_expiry_year=card.card_expiry_year,
                           purchases=purchases, product_price=product_price)


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect('/')


@app.route('/productList/<input>') #filter by port
def product_list_filter(input):
    allproducts = Product.query.filter_by(product_port=input).all()
    return render_template('productList.html', allproducts=allproducts)


@app.route('/productListRegion/<region>') #filter by region
def product_list_region(region):
    allproducts = Product.query.filter_by(product_region=region).all()
    return render_template('productList.html', allproducts=allproducts)


app.route('/productList')
def product_list():
    allproducts = Product.query.all()

    return render_template('productList.html', allproducts=allproducts)


@app.route('/lines')
def lines():
    return render_template('lines.html', line_list=line_list, line_images=line_images, line_intros=line_intros)


@app.route('/<line_name>')
def line_detail(line_name):
    line_intro = line_details[line_name]["intro"]
    line_detail1 = line_details[line_name]["detail1"]
    line_detail2 = line_details[line_name]["detail2"]
    line_detail3 = line_details[line_name]["detail3"]

    return render_template('linesDetail.html', detail_images=detail_images, line_name=line_name, line_intro=line_intro,
                           line_detail1=line_detail1,
                           line_detail2=line_detail2, line_detail3=line_detail3)


@app.route('/ships')
def ships():
    products = Product.query.all()  # fetch all products
    return render_template('ships.html',products=products)


@app.route('/regions')
def regions():
    return render_template('regions.html')


@app.route('/ports')
def ports():
    return render_template('ports.html')


@app.route('/reviews')
def reviews():
    with open('static/data/reviews.csv') as f:
        reader = csv.DictReader(f)
        news_items = [dict(row) for row in reader]
    return render_template('reviews.html', news_items=news_items)


@app.route('/help')
def help():
    return render_template('help.html')


@app.route('/orderResult')
@login_required
def order_result():
    date = today.strftime("%B %d, %Y")
    user = Customer.query.get(current_user.id)  # using pk to get user
    cart_id = user.cart_id
    total = calculate_order_amount(cart_id)
    tax_total = calculate_tax(total)

    allproducts = db.session.execute(
        db.select(Product.product_id, Product.product_name, Product.product_price, ProductCart.quantity)
        .where(ProductCart.cart_id == cart_id)
        .where(ProductCart.product_id == Product.product_id))

    try:
        for p in allproducts:  # adding to purchase history
            purchase = Purchases(
                purchase_customer_email=current_user.id,
                purchase_product_id=p.product_id,
                purchase_name=p.product_name,
                purchase_quantity=p.quantity,
                purchase_date=date,
                purchase_price=p.product_price)
            db.session.add(purchase)
            db.session.commit()
    except:
        print('nothing reached')

    products = db.session.execute(  # re-exec query to get data again
        db.select(Product.product_id, Product.product_name, Product.product_price, ProductCart.quantity)
        .where(ProductCart.cart_id == cart_id)
        .where(ProductCart.product_id == Product.product_id))
    return render_template('orderResult.html', cart_id=cart_id, products=products, total=total, tax_total=tax_total,
                           date=date)


def delete_cart():
    user = Customer.query.get(current_user.id)  # using pk to get user
    ProductCart.query.filter_by(cart_id=user.cart_id).delete()
    db.session.commit()


@app.route('/delete_cart')
@login_required
def delete_cart():
    user = Customer.query.get(current_user.id)  # using pk to get user
    ProductCart.query.filter_by(cart_id=user.cart_id).delete()
    db.session.commit()
    return redirect(url_for('index'))


def calculate_order_amount(cart_id):
    total = 0
    products = db.session.execute(
        db.select(Product.product_id, Product.product_name, Product.product_price, ProductCart.quantity)
        .where(ProductCart.cart_id == cart_id)
        .where(ProductCart.product_id == Product.product_id)
    )
    for p in products:
        total += int(p[2]) * int(p[3])  # convert to int!
    return total


def calculate_tax(total):
    tax_total = (total * 0.15)
    return tax_total


today = date.today()


@app.route('/cart')
@login_required
def cart():
    date = today.strftime("%B %d, %Y")
    user = Customer.query.get(current_user.id)  # using pk to get user
    cart_id = user.cart_id
    total = calculate_order_amount(cart_id)
    tax_total = calculate_tax(total)
    try:
        products = db.session.execute(
            db.select(Product.product_id, Product.product_name, Product.product_price, ProductCart.quantity)
            .where(ProductCart.cart_id == cart_id)
            .where(ProductCart.product_id == Product.product_id)
        )
    except:
        cart_id = None
        products = None
    return render_template('cart.html', cart_id=cart_id, products=products, total=total, tax_total=tax_total, date=date)


@app.route('/product/<int:id>')  # set the value being passed as int or else index will not work!
def product(id):  # purposely available while not loggedin

    allproducts = Product.query.all()
    index = id - 1  # -1 to properly reference database
    return render_template('product.html', allproducts=allproducts, index=index)


@app.route('/add_to_cart/<int:product_id>')
@login_required
def addToCart(product_id):
    user = Customer.query.get(current_user.id)  # get user
    cart = Cart.query.get(user.cart_id)
    product = Product.query.get(product_id)
    try:
        prodCart = ProductCart.query.filter_by(cart_id=cart.cart_id).filter_by(product_id=product.product_id).one()
        prodCart.quantity += 1  # add one to quantity of product if exists
    except:
        prodCart = ProductCart(product_id=product.product_id, cart_id=cart.cart_id)
    db.session.add(prodCart)
    db.session.commit()
    return redirect(url_for('cart'))


if __name__ == '__main__':
    app.run(debug=True)
