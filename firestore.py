# Copyright 2019 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

# [START bookshelf_firestore_client_import]
from google.cloud import firestore


# [END bookshelf_firestore_client_import]


def document_to_dict(doc):
    if not doc.exists:
        return None
    doc_dict = doc.to_dict()
    doc_dict['id'] = doc.id
    return doc_dict


def load_items(limit=100):
    #  db = firestore.Client()
    db = firestore.Client.from_service_account_json('/Users/imac/documents/service_acc/service_account.json')

    query = db.collection(u'Items').limit(limit).order_by(u'item_id')

    docs = query.stream()
    docs = list(map(document_to_dict, docs))

    return docs


"""

def next_page(limit=10, start_after=None):
    #  db = firestore.Client()
    db = firestore.Client.from_service_account_json('/Users/imac/documents/service_acc/service_account.json')

    query = db.collection(u'Book').limit(limit).order_by(u'title')

    if start_after:
        # Construct a new query starting at this document.
        query = query.start_after({u'title': start_after})

    docs = query.stream()
    docs = list(map(document_to_dict, docs))

    last_title = None
    if limit == len(docs):
        # Get the last document from the results and set as the last title.
        last_title = docs[-1][u'title']
    return docs, last_title

"""


def readUserInfo(user_id):
    db = firestore.Client()
    user_ref = db.collection(u'Users').document(user_id)
    snapshot = user_ref.get()
    return document_to_dict(snapshot)


def add_to_cart(data: dict, user_id: str, item_id: str):
    db = firestore.Client()
    cart_ref = db.collection(u'Cart').document(item_id).set(data, merge=True)
    user_cart_ref = db.collection(u'Users').document(user_id).collection(u'Cart').document(item_id)
    user_cart_ref.set(data, merge=True)
    return document_to_dict(user_cart_ref.get())


def get_single_item(item_id: str):
    db = firestore.Client()
    item_ref = db.collection(u'Items').document(item_id)
    snapshot = item_ref.get()

    return document_to_dict(snapshot)


def get_cart_items(user_id: str, limit: int = 100):
    db = firestore.Client()

    query = db.collection(u'Users').document(user_id).collection(u'Cart').limit(limit).order_by(u'item_id')

    docs = query.stream()
    docs = list(map(document_to_dict, docs))

    return docs


def read(book_id):
    # [START bookshelf_firestore_client]
    db = firestore.Client()
    book_ref = db.collection(u'Book').document(book_id)
    snapshot = book_ref.get()
    # [END bookshelf_firestore_client]
    return document_to_dict(snapshot)


def update(data, book_id=None):
    db = firestore.Client()
    book_ref = db.collection(u'Book').document(book_id)
    book_ref.set(data)
    return document_to_dict(book_ref.get())


def createUserProfile(data, user_id=None):
    db = firestore.Client()
    user_ref = db.collection(u'Users').document(user_id)
    user_ref.set(data, merge=True)
    return document_to_dict(user_ref.get())


def addItem(data, item_id=None):
    db = firestore.Client()
    item_ref = db.collection(u'Items').document(item_id)
    item_ref.set(data, merge=True)

    return document_to_dict(item_ref.get())


def delete(id):
    db = firestore.Client()
    book_ref = db.collection(u'Book').document(id)
    book_ref.delete()
