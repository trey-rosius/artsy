import functools
import os

from flask import (
    Blueprint, current_app, flash, g, redirect, render_template, request, session, url_for, json
)
from pathlib import Path
import pyrebase
import firestore
from forms.add_item import AddItemForm
from forms.login import LoginForm
from forms.profile import ProfileForm
import google.cloud.logging
import storage
from forms.register import RegisterForm

# firebase = pyrebase.initialize_app(config)
from werkzeug.utils import secure_filename

bp = Blueprint('cart', __name__)

def add_to_cart(user_id:str,cart_id:str):
    data ={
        u'user_id':user_id,
        u'cart_id':cart_id,

    }
    cart_item = firestore.add_to_cart(data=data,user_id=user_id, cart_id=cart_id)
