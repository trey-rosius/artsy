import functools
import os

from flask import (
    Blueprint, current_app, flash, g, redirect, render_template, request, session, url_for, json, app
)
from pathlib import Path
import pyrebase
import firestore
from blueprints import auth;
from blueprints.auth import login_required
from forms.add_item import AddItemForm
from forms.login import LoginForm
from forms.profile import ProfileForm
import google.cloud.logging
import storage
from forms.register import RegisterForm

# firebase = pyrebase.initialize_app(config)
from werkzeug.utils import secure_filename

bp = Blueprint('cart', __name__)


@bp.route('/<user_id>/<item_id>/addToCart')
@login_required
def add_to_cart(user_id: str, item_id: str):
    item = firestore.get_single_item(item_id);
    data = {
        u'user_id': user_id,
        u'item_id': item_id,
        u'name': item['name'],
        u'description': item['description'],
        u'price': item['price'],
        u'image_url': item['image_url'],
        u'quantity': 1

    }
    firestore.add_to_cart(data=data, user_id=user_id, item_id=item_id)
    flash("Item successfully added to cart")
    return redirect(url_for('home.index'))


@bp.route('/<user_id>/cart')
@login_required
def view_cart(user_id: str):
    items = firestore.get_cart_items(user_id=user_id)

    return render_template('cart/cart.html', items=items)


@bp.route('/<user_id>/<item_id>/increment')
@login_required
def incrementItemQty(user_id: str, item_id: str):
    item = firestore.incrementItemQty(item_id=item_id,user_id=user_id)
    items = firestore.get_cart_items(user_id=user_id)

    flash("Item Incremented")
    return render_template('cart/cart.html', items=items)


@bp.route('/<user_id>/<item_id>/decrement')
@login_required
def decrementItemQty(user_id: str, item_id: str):
    item = firestore.decrementItemQty(item_id=item_id,user_id=user_id)
    items = firestore.get_cart_items(user_id=user_id)

    flash("Item decremented")
    return render_template('cart/cart.html', items=items)
@bp.route('/<user_id>/<item_id>/delete')
@login_required
def deleteItemFromCart(user_id: str, item_id: str):
    item = firestore.deleteItemFromCart(item_id=item_id,user_id=user_id)
    items = firestore.get_cart_items(user_id=user_id)

    flash("Item deleted")
    return render_template('cart/cart.html', items=items)
