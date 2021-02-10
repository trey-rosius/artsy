

from flask import (
    Blueprint, current_app, flash, g, redirect, render_template, url_for
)

import firestore

from forms.profile import ProfileForm
import storage

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


@bp.route('/<user_id>/view')
def view_profile(user_id: str):
    user = firestore.readUserInfo(user_id)

    return render_template('profile/profile.html', user=user)


@bp.route('/<user_id>/update', methods=['GET', 'POST'])
def update_profile(user_id: str):
    form = ProfileForm()
    user_to_dict = firestore.readUserInfo(user_id)

    if form.validate_on_submit():
        try:
            filename = secure_filename(form.photo.data.filename)
            image_url = upload_image_file(form.photo.data)
            data = {
                u'full_names': form.full_names.data,
                u'phone_number': form.phone_number.data,
                u'address': form.address.data,
                u'profile_pic': image_url
            }
            userInfo = firestore.createUserProfile(data, user_id)
            flash(userInfo)
            return redirect(url_for('profile.view_profile', user_id=user_id))

        except Exception as err:
            flash(err)

    form.email.data = user_to_dict["email"]
    if 'full_names' in user_to_dict:
        form.full_names.data = user_to_dict['full_names']
    else:
        form.full_names.data = ''

    if 'address' in user_to_dict:
        form.address.data = user_to_dict["address"]
    else:
        form.address.data = ''
    if 'phone_number' in user_to_dict:
        form.phone_number.data = user_to_dict["phone_number"]
    else:
        form.phone_number.data = ''
    if 'profile_pic' in user_to_dict:
        form.phone_number.data = user_to_dict["profile_pic"]
    else:
        form.photo.data = ''

    return render_template('profile/update_profile.html', form=form)
