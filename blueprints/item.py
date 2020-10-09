import functools

from flask import (
    Blueprint, current_app, flash, g, redirect, render_template, request, session, url_for, json
)

import pyrebase
import firestore
from forms.add_item import AddItemForm
from forms.login import LoginForm
from forms.profile import ProfileForm
import google.cloud.logging
import storage
from forms.register import RegisterForm

firebase = pyrebase.initialize_app(json.load(open('fbconfig.json')))
# firebase = pyrebase.initialize_app(config)
from werkzeug.utils import secure_filename

bp = Blueprint('item', __name__)


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


@bp.route('/addItem', methods=['GET', 'POST'])
def add_item():
    form = AddItemForm()

    if form.validate_on_submit():
        try:
            filename = secure_filename(form.photo.data.filename)
            image_url = upload_image_file(form.photo.data)
            data = {
                u'name': form.name.data,
                u'description': form.desc.data,
                u'price': form.price.data,
                u'image_url': image_url
            }
            userInfo = firestore.addItem(data)
            flash(userInfo)
            return redirect(url_for('profile.view_profile'))

        except Exception as err:
            flash(err)

    return render_template('item/add_item.html', form=form)
