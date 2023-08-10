from app import db
# import datetime


# class CruiseLine(db.Model):
#     __tablename__ = 'cruise_lines'
#     company_id = db.Column(db.Integer(), primary_key=True)
#     company_name = db.Column(db.Text(), nullable=False)
#     company_description = db.Column(db.Text(), nullable=False)
#     company_insurance = db.Column(db.Text(), nullable=False)
#     company_payment_and_refund = db.Column(db.Text(), nullable=False)
#     company_other_info = db.Column(db.Text())
#     ships = db.relationship('Ship', backref='cruise_lines', lazy=True)
#
#     def __repr__(self):
#         return f'<Cruise Line #{self.company_id}: {self.company_name}>'
#
#
# class Ship(db.Model):
#     __tablename__ = 'ships'
#     ship_id = db.Column(db.Integer(), primary_key=True)
#     company_id = db.Column(db.Integer(), db.ForeignKey('cruise_lines.company_id'))
#     ship_name = db.Column(db.Text(), nullable=False)
#     ship_description = db.Column(db.Text(), nullable=False)
#     ship_year = db.Column(db.Integer(), nullable=False)
#     ship_capacity = db.Column(db.Integer(), nullable=False)
#     ship_rating = db.Column(db.Float(), nullable=False)
#     itineraries = db.relationship('Itinerary', backref='ships', lazy=True)
#
#     def __repr__(self):
#         return f'<Ship #{self.ship_id}: {self.ship_name}>'
#
#
# class Itinerary(db.Model):
#     __tablename__ = "itineraries"
#     it_id = db.Column(db.Integer(), primary_key=True)
#     ship_id = db.Column(db.Integer(), db.ForeignKey('ships.ship_id'))
#     it_start_date = db.Column(db.DateTime(), nullable=False, default=datetime.datetime.now)
#     it_end_date = db.Column(db.DateTime(), nullable=False, default=datetime.datetime.now)
#     it_destination = db.Column(db.Text(), nullable=False)
#     #Repeat of ship_rating?
#     it_price = db.Column(db.Float(), nullable=False)
#     it_discount = db.Column(db.Float(), nullable=False, default=00.00)
#     orders = db.relationship('Order', backref='itineraries', lazy=True)
#
#     def __repr__(self):
#         return f'<Itinerary #{self.it_id}: from {self.it_start_date} to {self.it_end_date}>'


class Customer(db.Model):
    __tablename__ = "customers"
    customer_email = db.Column(db.Text(), primary_key=True)
    customer_first_name = db.Column(db.Text(), nullable=False)
    customer_last_name = db.Column(db.Text(), nullable=False)
    customer_phone = db.Column(db.Text(), nullable=False)
    customer_password = db.Column(db.Text(), nullable=False)
    cart_id = db.Column(db.Integer(),db.ForeignKey('cart.cart_id'))    #added for add2card/checkout
    cards = db.relationship('Card', backref='customers', lazy=True)
    # orders = db.relationship('Order', backref='customers', lazy=True)

    def __repr__(self):
        return f'<Customer Email: {self.customer_email}, Name: {self.customer_last_name}, {self.customer_first_name}. ' \
               f'Phone: {self.customer_phone}>'


class Card(db.Model):
    __tablename__ = "cards"
    card_number = db.Column(db.Text(), primary_key=True)
    customer_email = db.Column(db.Text(), db.ForeignKey('customers.customer_email'))
    card_issuer = db.Column(db.Text(), nullable=False)
    card_name = db.Column(db.Text(), nullable=False)
    card_expiry_month = db.Column(db.Text(), nullable=False)
    card_expiry_year = db.Column(db.Text(), nullable=False)
    card_cvv = db.Column(db.Text(), nullable=False)
    # orders = db.relationship('Order', backref='cards', lazy=True)

    def __repr__(self):
        return f'<Card number: {self.card_number}, Cardholder Name: {self.card_name}, Cardholder Issuer: {self.card_issuer}>'

#
# class Order(db.Model):
#     __tablename__ = "orders"
#     order_id = db.Column(db.Text(), primary_key=True)
#     customer_email = db.Column(db.Integer(), db.ForeignKey('customers.customer_email'))
#     it_id = db.Column(db.Integer(), db.ForeignKey('itineraries.it_id'))
#     card_number = db.Column(db.Text(), db.ForeignKey('cards.card_number'))
#     order_date = db.Column(db.Date(), nullable=False, default=datetime.datetime.now)
#     order_number_guests = db.Column(db.Integer(), nullable=False)
#     order_price_before_tax = db.Column(db.Float(), nullable=False)
#     order_tax = db.Column(db.Float(), nullable=False)
#     order_price_after_tax = db.Column(db.Float(), nullable=False)
#
#     def __repr__(self):
#         return f'<Order ID: {self.order_id} for Customer {self.customer_email}' \
#                f'Order details: Itinerary ID: {self.it_id}, Number of guests: {self.order_number_guests}' \
#                f'Order date: {self.order_date}' \
#                f'Price: {self.order_price_before_tax}' \
#                f'Tax: {self.order_tax}' \
#                f'Total: {self.order_price_after_tax}>'


#--------------------- add2cart / checkout -------------------------
class Product(db.Model):
    __tablename__ = 'product'
    product_id = db.Column(db.Integer(), primary_key=True, autoincrement=True)
    product_name = db.Column(db.Text())
    product_booking_number = db.Column(db.Integer())
    product_cruise_line = db.Column(db.Text())
    product_price = db.Column(db.Text())
    product_year_built = db.Column(db.Text())
    product_length = db.Column(db.Text())
    product_number_of_nights = db.Column(db.Text())
    product_capacity = db.Column(db.Text())
    product_port = db.Column(db.Text())
    product_description = db.Column(db.Text())
    product_tonnage = db.Column(db.Text())
    product_currency = db.Column(db.Text())
    product_casino = db.Column(db.Text())
    product_bar = db.Column(db.Text())
    product_number_of_inside_cabins = db.Column(db.Text())
    product_number_of_outside_cabins = db.Column(db.Text())
    product_number_of_suites = db.Column(db.Text())
    product_crew_size = db.Column(db.Text())
    product_region = db.Column(db.Text())
    product_rating = db.Column(db.Text())


class Cart(db.Model):
    __tablename__ = 'cart'
    cart_id = db.Column(db.Integer(), primary_key=True, autoincrement=True)


class ProductCart(db.Model):
    __tablename__ = 'product_cart'
    product_id = db.Column(db.Integer(), db.ForeignKey('product.product_id'), primary_key=True)
    cart_id = db.Column(db.Integer(), db.ForeignKey('cart.cart_id'), primary_key=True)
    quantity = db.Column(db.Integer(), default=1)


class Purchases(db.Model):
    __tablename__ = 'purchases'
    purchase_id = db.Column(db.Integer(), primary_key=True, autoincrement=True)
    purchase_customer_email = db.Column(db.Text(), db.ForeignKey('customers.customer_email'))
    purchase_product_id = db.Column(db.Integer(), db.ForeignKey('product.product_id'))
    purchase_name = db.Column(db.Text())
    purchase_quantity = db.Column(db.Integer())
    purchase_price = db.Column(db.Text())
    purchase_date = db.Column(db.Text())

