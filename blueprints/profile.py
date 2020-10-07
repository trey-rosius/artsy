import functools

from flask import (
    Blueprint, current_app, flash, g, redirect, render_template, request, session, url_for, json
)

import pyrebase
import firestore
from forms.login import LoginForm
from forms.profile import ProfileForm
import google.cloud.logging
import storage
from forms.register import RegisterForm

firebase = pyrebase.initialize_app(json.load(open('fbconfig.json')))
# firebase = pyrebase.initialize_app(config)
from werkzeug.utils import secure_filename
bp = Blueprint('profile', __name__, url_prefix='/profile')

def upload_image_file(img):
    """
    Upload the user-uploaded file to Google Cloud Storage and retrieve its
    publicly-accessible URL.
    """
    if not img:
        return None

    public_url = storage.upload_file(
        img.read(),
        img.filename,
        img.content_type
    )

    current_app.logger.info(
        'Uploaded file %s as %s.', img.filename, public_url)

    return public_url
# [END upload_image_file]


@bp.route('/<user_id/view')
def view_profile(user_id:str):
    user = firestore.readUserInfo(user_id)

    return render_template('profile/profile.html',user=user)


@bp.route('/<user_id>/update', methods=('GET', 'POST'))
def update_profile(user_id:str):
    user = firestore.readUserInfo(user_id)
    form = ProfileForm()
    form.full_names.data = user['full_names']
    form.email.data = user["email"]
    form.phone_number.data = user["phone_number"]
    form.address.data = user["address"]

    if form.validate_on_submit():
        filename = secure_filename(form.photo.data.filename)
        image_url = upload_image_file(form.photo.data)
        data ={
            u'full_names':form.full_names.data,
            u'phone_number':form.phone_number.data,
            u'address':form.address.data,
            u'profile_pic':image_url
        }
        userInfo = firestore.createUserProfile(data,user_id)
        return redirect(url_for('profile.view_profile',user_id=user_id))
    return render_template('profile/update_profile.html', form=form)
