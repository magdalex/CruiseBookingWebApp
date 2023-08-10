from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, SelectField
from wtforms.fields import EmailField
from wtforms.validators import InputRequired, EqualTo, Email, Length


class LoginForm(FlaskForm):
    email = StringField('Email', validators=[InputRequired()])
    password = PasswordField('Password', validators=[InputRequired()])
    submit = SubmitField('Login')


class RegisterForm(FlaskForm):
    first_name = StringField('First Name', validators=[InputRequired()])
    last_name = StringField('Last Name', validators=[InputRequired()])
    credit_card = SelectField('Credit Card', validators=[InputRequired()],
                              choices=[('American Express', 'American Express'), ('Credit', 'Credit'),
                                       ('Visa', 'Visa')])
    cardholder_name = StringField('Cardholder Name', validators=[InputRequired()])
    card_number = StringField('Card Number', validators=[InputRequired(), Length(16)])
    expiration_month = SelectField('Month', validators=[InputRequired()],
                                   choices=[('January', 'January(01)'),
                                            ('February', 'February(02)'),
                                            ('March', 'March(03'),
                                            ('April', 'April(04)'),
                                            ('May', 'May(05)'),
                                            ('June', 'June(06)'),
                                            ('July', 'July(07)'),
                                            ('August', 'August(08)'),
                                            ('September', 'September(09)'),
                                            ('October', 'October(10)'),
                                            ('November', 'November(11)'),
                                            ('December', 'December(12)')
                                            ])
    expiration_year = SelectField('Year', validators=[InputRequired()],
                                  choices=[('2023', '2023'),
                                           ('2024', '2024'),
                                           ('2025', '2025'),
                                           ('2026', '2026'),
                                           ('2027', '2027')
                                           ])
    cvv = StringField('CVV', validators=[InputRequired()])
    email = EmailField('Email', validators=[InputRequired(), Email()])
    phone = StringField('Phone number', validators=[InputRequired()])
    password = PasswordField('Password', validators=[InputRequired(), Length(8)])
    password2 = PasswordField('Repeat password',
                              validators=[InputRequired(),
                                          EqualTo('password',
                                                  message='Passwords must match.')])
    submit = SubmitField('Register')
