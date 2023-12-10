from core import db
import string
from datetime import datetime
from random import choices
from datetime import datetime

class New_URLs(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    created_at = db.Column(db.DateTime(), default=datetime.now(), nullable=False)
    original_url = db.Column(db.String(500), nullable=False)
    CID = db.Column(db.String(20), nullable=False, unique=True)
    new_url = db.Column(db.String(500), nullable=False)
    #visits = db.Column(db.Integer, default=0 , nullable=False)
    #all of the stuff from new hottness
    
    
def __init__(self, *args, **kwargs):
    super(New_URLs, self).__init__(*args, **kwargs)

def __repr__(self):
    return '<URL %s>' % self.old