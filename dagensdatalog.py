from flask import Flask, jsonify, send_from_directory, render_template, request, Response
from flask_compress import Compress
from flask_dropzone import Dropzone

from werkzeug.utils import secure_filename

from functools import wraps

from tinydb import TinyDB, Query

import os, datetime, random, shutil, uuid

wd = os.path.dirname(os.path.realpath(__file__))
dbpath = os.path.join(wd, 'db.json')

startDate = datetime.date(2017, 10, 1) # Do not show pictures before this date

compress = Compress()
app = Flask(__name__)
dropzone = Dropzone(app)
db = TinyDB(dbpath)

compress.init_app(app)

#
# Configure dropzone file uploads
#

app.config['DROPZONE_ALLOWED_FILE_CUSTOM'] = True
app.config['DROPZONE_ALLOWED_FILE_TYPE'] = 'image/*'
app.config['DROPZONE_MAX_FILE_SIZE'] = 5 # max 5mb files
app.config['DROPZONE_INPUT_NAME'] = 'images'
app.config['DROPZONE_DEFAULT_MESSAGE'] = 'Drop images here to upload'

#
# Slogans
#

slogans = [
    'Når du studerer for sjov',
    'P = NP',
    'www.dropud.nu',
    'P er LIG med NP, P er ikke en DELMÆNGDE af NP',
    'TÅGEKAMRET',
    'It\'s a unix system, i know this!',
    'I\'d just like to interject for a moment...',
    'ME TOO THANKS',
    'Grøn kage',
    'undefined',
    'Mere swag',
    'Rubber duck debugging',
    'Balmer peaking',
    'Dovs med sovs',
    'segmentation fault (core dumped)',
    'reduce-reduce error',
    'AU - Alchoholics united',
    '#AUpassende',
]

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
        return jsonify({'error': 'invalid date'}), 400

    if date > datetime.date.today():
        return jsonify({'error': 'date is in the future'}), 400
    else:
        return jsonify(get_picture(date))

@app.route('/api/<n>')
def api_n(n):
    try:
        n = int(n)

        if n > 256 or n < 1:
            return jsonify({'error': 'number out of range 1-255'}), 400

        return jsonify(get_pictures(int(n)))
    except ValueError:
        return jsonify({'error': 'invalid number'}), 400
        
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

        if date > datetime.date.today() or date < startDate:
            return render_template('notfound.html', nopicture=True), 404
        else:
            picture = get_picture(date)['image']

    except ValueError:
        return render_template('notfound.html'), 404

    slogan = get_slogan()

    return render_template('index.html', picture=picture, datetime=datetime, date=date, startDate=startDate, slogan=slogan)

@app.route('/')
def index():
    date = datetime.date.today()
    picture = get_picture(date)['image']
    slogan = get_slogan()

    return render_template('index.html', picture=picture, datetime=datetime, date=date, startDate=startDate, slogan=slogan)

@app.route('/upload', methods=['GET', 'POST'])
def upload():
    if request.method == 'GET':
        count, waiting = get_count()
        slogan = get_slogan()

        return render_template('upload.html', count=count, waiting=waiting, slogan=slogan)

    elif request.method == 'POST':
        f = request.files['images']
        ext = os.path.splitext(secure_filename(f.filename))[1] or ''
        f.save(os.path.join('./uploads', str(uuid.uuid1()) + ext))
        return '', 200

@app.route('/api/doc')
def api_about():
    slogan = get_slogan()

    return render_template('api.html', slogan=slogan)

#
# Admin page
#

def check_auth(username, password):
    return (os.environ['ADMIN_USER'] == username and os.environ['ADMIN_PASSWORD'] == password)

def authenticate():
    """Sends a 401 response that enables basic auth"""
    return Response(
    'Could not verify your access level for that URL.\n'
    'You have to login with proper credentials', 401,
    {'WWW-Authenticate': 'Basic realm="Login Required"'})

def requires_auth(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        auth = request.authorization
        if not auth or not check_auth(auth.username, auth.password):
            return authenticate()
        return f(*args, **kwargs)
    return decorated

@app.route('/admin')
@requires_auth
def admin():
    pictures = os.listdir(os.path.join(wd, 'uploads'))
    pictures = [pic for pic in pictures if not pic.endswith('.gitkeep')] # remove the .gitkeep file...
    slogan = get_slogan()
    return render_template('admin.html', pictures=pictures, slogan=slogan)

@app.route('/admin/picture/<path>')
@requires_auth
def admin_picture(path):
    return send_from_directory('uploads', path)

@app.route('/admin/approve/<name>', methods=['POST'])
@requires_auth
def admin_picture_approve(name):
    upload_path = os.path.join(wd, 'uploads', name);

    if os.path.exists(upload_path):
        shutil.move(upload_path, os.path.join(wd, 'pictures', name))
        return '', 200
    else:
        return '', 404

@app.route('/admin/disapprove/<name>', methods=['POST'])
@requires_auth
def admin_picture_disapprove(name):
    upload_path = os.path.join(wd, 'uploads', name);

    if os.path.exists(upload_path):
        os.remove(upload_path)
        return '', 200
    else:
        return '', 404


#
# Error handling
# 

@app.errorhandler(404)
def page_not_found(e):
    return render_template('notfound.html')

@app.errorhandler(500)
def page_not_found(e):
    return render_template('notfound.html')

#
# Helping methods
#

def get_count():
    return (len(os.listdir(os.path.join(wd, 'pictures'))), len(os.listdir(os.path.join(wd, 'uploads'))) - 1)

def get_slogan():
    return random.choice(slogans)

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
