

from flask import (
    Blueprint,  render_template,
)


import firestore


bp = Blueprint('home', __name__)


@bp.route('/')
def index():
    items = firestore.load_items()

    return render_template('index.html', items=items)
