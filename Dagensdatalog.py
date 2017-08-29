from flask import Flask,jsonify,send_from_directory
from pathlib import Path
import os
import datetime
import json
import random
import io

app = Flask(__name__)
print(os.getcwd())
wd = os.path.dirname(os.path.realpath(__file__))

try:
    to_unicode = unicode
except NameError:
    to_unicode = str

@app.route('/pictures/<path:path>')
def send_picture(path):
    return send_from_directory('pictures', path)

@app.route('/')
def hello_world():
    return '<!DOCTYPE html> <html> <head> <title>Dagensdatalog</title> <style type="text/css"> html, body { height: 100%; width: 100%; padding: 0px; margin: 0px; background-image: url("/pictures/' + get_picture() + '"); background-repeat: no-repeat; background-position: center; background-size: contain; background-color: #000; } </style> </head> <body> </body> </html>'

@app.route('/api')
def api():
    json_data = open_json()
    return jsonify(json_data)

def open_json():
    p = Path(os.path.join(wd, 'image.json'))
    with p.open() as json_data:
        return json.load(json_data)

def get_picture():
    json_data = open_json()
    today = str(datetime.date.today())
    available_pictures = os.listdir('pictures')
    latest_pictures = json_data['latest_pictures']

    if json_data['update_time'] == today:
        picture = latest_pictures[0]
    else :
        picture = random.choice(available_pictures)
        latest_pictures.reverse()
        latest_pictures.append(picture)
        latest_pictures.reverse()
        if len(latest_pictures) > 5:
            latest_pictures.pop()

        json_data = {'update_time': today,
                     'latest_pictures': latest_pictures}
        with io.open('image.json', 'w', encoding='utf8') as outfile:
            str_ = json.dumps(json_data,
                              indent=4, sort_keys=True,
                              separators=(',', ': '), ensure_ascii=False)
            outfile.write(to_unicode(str_))



    return picture

if __name__ == '__main__':
    app.run()
