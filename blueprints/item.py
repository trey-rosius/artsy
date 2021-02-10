
import os

from flask import (
    Blueprint, current_app, flash, g, redirect, render_template, url_for,
)
from pathlib import Path

import firestore
from forms.add_item import AddItemForm

import storage

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




@bp.route('/<user_id>/addItem', methods=['GET', 'POST'])
def add_item(user_id: str):
    form = AddItemForm()
    bucketname = 'ros-social-media_bucket'
    url = "https://storage.googleapis.com/"+bucketname+"/thumbs/"
    if form.validate_on_submit():
        try:
            filename = secure_filename(form.photo.data.filename)

            image_url = upload_image_file(form.photo.data)
            path_without = Path(image_url).stem

            print(path_without)
            url_200_x_200 = url + path_without + "_200x200" + os.path.splitext(filename)[1]
            url_400_x_400 = url + path_without + "_400x400" + os.path.splitext(filename)[1]
            url_600_x_600 = url + path_without + "_600x600" + os.path.splitext(filename)[1]
            data = {
                u'name': form.name.data,
                u'description': form.desc.data,
                u'price': form.price.data,
                u'image_url': image_url,
                u'user_id': user_id,
                u'image_url_200x200':url_200_x_200,
                u'image_url_400x400':url_400_x_400,
                u'image_url_600x600':url_600_x_600


            }
            item_info = firestore.addItem(data)
            data_id ={
                u'item_id':item_info['id']
            }
            #update the id of the item
            firestore.addItem(data_id,item_info['id'])
            flash(item_info)
            return redirect(url_for('home.index'))

        except Exception as err:
            flash(err)

    return render_template('item/add_item.html', form=form)


