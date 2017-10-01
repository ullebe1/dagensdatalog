from flask import Flask,jsonify, send_from_directory, render_template
from tinydb import TinyDB, Query

import os
import datetime
import random

wd = os.path.dirname(os.path.realpath(__file__))
dbpath = os.path.join(wd, 'db.json')

app = Flask(__name__)
db = TinyDB(dbpath)

#
# Routes
#

@app.route('/picture/<path>')
def send_picture(path):
    return send_from_directory('pictures', path)

@app.route('/api/date/<date>')
def api_specific(date):
    try:
        date = datetime.datetime.strptime(date, "%d-%m-%Y").date()
    except ValueError:
        return jsonify({'error': 'invalid date'})

    return jsonify(get_picture(date))

@app.route('/api/<n>')
def api_n(n):
    try:
        return jsonify(get_pictures(int(n)))
    except ValueError:
        return jsonify({'error': 'invalid number'})
        
@app.route('/api')
def api():
    return jsonify(get_pictures())

@app.route('/favicon.ico')
def favicon():
    return send_from_directory(wd, 'favicon.ico', mimetype='image/vnd.microsoft.icon')

@app.route('/<date>')
def index_specific(date):
    picture = None

    try:
        date = datetime.datetime.strptime(date, "%d-%m-%Y").date()

        if date > datetime.date.today():
            return render_template('notfound.html', nopicture=True), 404
        else:
            picture = get_picture(date)['image']

    except ValueError:
        return render_template('notfound.html'), 404

    return render_template('index.html', picture=picture, datetime=datetime, date=date)

@app.route('/')
def index():
    date = datetime.date.today()
    picture = get_picture(date)['image']

    return render_template('index.html', picture=picture, datetime=datetime, date=date)

@app.errorhandler(404)
def page_not_found(e):
    return render_template('notfound.html')

#
# Helping methods
#

def get_picture(date):
    picture = db.search((Query().date == str(date.strftime("%d-%m-%Y"))))
    picture = picture[0] if picture else None

    if not picture:
        picture = select_new_picture(date)

    return picture

def select_new_picture(date):
    datestr = str(date.strftime("%d-%m-%Y"))

    if not db.search((Query().date == datestr)):
        pictures = os.listdir(os.path.join(wd, 'pictures'))

        if pictures:
            old_pictures = list(map(lambda p: p['image'], get_pictures(30)))
            old_pictures = list(set(pictures) - set(old_pictures))

            picture = random.choice(old_pictures)
            obj = {"image": picture, "date": datestr}
            db.insert(obj)

            return obj;

def get_pictures(n=10):
    pictures = db.all()
    return sorted(pictures, key=lambda p: datetime.datetime.strptime(p['date'], "%d-%m-%Y").date(), reverse=True)[:n]

if __name__ == '__main__':
    app.run()
