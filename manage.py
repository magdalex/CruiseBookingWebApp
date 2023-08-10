from app import app
from models import db, Customer, Card, Product, Cart, ProductCart, Purchase


@app.shell_context_processor
def make_shell_context():
    return dict(app=app, db=db, Card=Card , ProductCart = ProductCart, Customer=Customer, Product = Product, Cart = Cart, Purchases=Purchase)
