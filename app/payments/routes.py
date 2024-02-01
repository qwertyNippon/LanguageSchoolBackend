from flask import Blueprint, request, jsonify
import json
import os
import stripe
from ..models import Movie

payments = Blueprint('payments', __name__, url_prefix='/pay')

stripe.api_key = os.environ.get('STRIPE_KEY')


def check_total(cart):
    total = 0
    for movie in cart['movies']:
        m = Movie.query.get(cart['movies'][movie]['data']['id']).price
        total += m * cart['movies'][movie]['quantity']
    print(f"TOTAL----->{total}")
    return int(total * 100)
    
def getCustomer(user):
    """
    Kind like our pokemon here. . . 
    check stripe for existing customer data else create a new stripe customer
    """
    try:
        customer = stripe.Customer.retrieve(user['uid'])
    except:
        customer = stripe.Customer.create(id=user['uid'], name=user['displayName'], email=user['email'])
    return customer

@payments.route('/create-payment-intent', methods=['POST'])
def create_payment():
    try:
        data = json.loads(request.data)
        print(data)
        # Create a PaymentIntent with the order amount and currency
        intent = stripe.PaymentIntent.create(
            amount=check_total(data['cart']),
            customer=getCustomer(data['user']),
            currency='usd',
            payment_method_types=['card']
        )
        return jsonify({'clientSecret': intent['client_secret']}), 200
    except Exception as e:
        return jsonify(error=str(e)), 403