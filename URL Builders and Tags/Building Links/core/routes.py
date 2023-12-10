from datetime import datetime
from core.models import New_URLs
from core import app, db
from random import choice
import string
from flask import render_template, request, flash, redirect, url_for


def generate_CID(num_of_chars: int):
    """Function to generate CID of specified number of characters"""
    return ''.join(choice(string.ascii_letters+string.digits) for _ in range(num_of_chars))





@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        url = request.form['url']
        CID = request.form['custom_id']
        #medium = request.form['medium']
        #source = request.form['source']
        
        if CID and New_URLs.query.filter_by(CID=CID).first() is not None:
            flash('Please enter different custom id!')
            return redirect(url_for('index'))
        if not url:
            flash('The URL is required!')
            return redirect(url_for('index'))
        if not CID:
            CID = generate_CID(8)
        new_url = url + "?CID=" + CID
        new_link = New_URLs(
            original_url=url, CID=CID, created_at=datetime.now(), new_url=new_url)
        db.session.add(new_link)
        db.session.commit()
        return render_template('index.html', new_url=new_url)
    return render_template('index.html')



@app.route('/<CID>')
def redirect_url(CID):
    link = New_URLs.query.filter_by(CID=CID).first()
    if link:
        link.visits = link.visits + 1
        db.session.add(link)
        db.session.commit()
        return redirect(link.original_url)
    else:
        flash('Invalid URL')
    return redirect(url_for('index'))

# @app.route('/<CID>')
# def redirect_url(CID):
#     link = New_URLs.query.filter_by(CID=CID).first_or_404()
#     if link:
#         link.visits = link.visits + 1
#         db.session.commit()
#         return redirect(link.original_url)
#     else:
#         flash('Invalid URL')
#     return redirect(url_for('index'))

# @app.route('/<stats>')
# def stats():
#     links = New_URLs.query.all()

#     return render_template('index.html', links=links)



# @app.route('/stats')
# def stats():
#     links = New_URLs.query.all()

#     return render_template('index.html', links=links)

# @app.errorhandler(404)
# def page_not_found(e):
#     return render_template('404.html'), 404