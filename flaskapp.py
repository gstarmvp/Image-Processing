import os
import time
from flask import Flask, request, flash, url_for, redirect, \
     render_template, abort, send_from_directory, abort
from werkzeug import secure_filename
from werkzeug.exceptions import RequestEntityTooLarge
from filters.filters import open_file, get_matrix, apply_kernel, \
     produce_output, save_img
from datetime import datetime

ALLOWED_EXTENSIONS = set(['bmp'])

app = Flask(__name__)
run_config = 'dev'
app.config.from_pyfile('flaskapp.cfg')
app.config['UPLOAD_FOLDER'] = os.path.join(app.static_folder, 'img')
app.config['MAX_CONTENT_LENGTH'] = 512 * 1024

@app.route('/<path:resource>')
def serveStaticResource(resource):
    return send_from_directory('static/', resource)

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS

@app.route('/image/<filename>')
def image(filename):
    if os.path.isfile(os.path.join(app.config['UPLOAD_FOLDER'], filename)):
        return render_template('index.html', filename=filename)
    else:
        return abort(404)


@app.route('/', methods=['GET', 'POST'])
def upload():
    if request.method == 'POST':
        file = request.files['file']
        if file and allowed_file(file.filename):
            try:
                filename = secure_filename(file.filename)
                file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
                file.close()
                return redirect(url_for('image', filename=filename))
            except RequestEntityTooLarge as e:
                flash('data too large')
                return redirect(url_for('upload'))
        else:
            flash('File extension not allowed. Only .bmp files are supported')

    return render_template('index.html')


def convert(n):
    try:
        float(n)
        return float(n)
    except ValueError as v:
        return False


def parse(k):
    if '/' in k:
        fraction = k.split("/")
        numer = convert(fraction[0])
        denom = convert(fraction[1])
        if numer and denom:
            return numer/denom
        else:
            return False
    else:
        n = convert(k)
        return n


@app.route('/filter', methods=['POST'])
def filter():
    kernel = [[0,0,0], [0,0,0], [0,0,0]]
    counter = 0
    filename = request.form['filename']

    for k in range(len(kernel)):
         for j in range(len(kernel)):
            n = parse(request.form['k'+str(counter)])
            if n:
                kernel[k][j] = n
                counter += 1
            else:
                flash("Bad kernel value")
                return render_template('index.html', filename=filename)

    im, fp, width, height, pixels = open_file(os.path.join(app.config['UPLOAD_FOLDER'], filename))
    output = produce_output(kernel, pixels, width, height)
    new_file = save_img(width, height, im, output, filename)

    basedir = os.path.abspath(os.path.dirname(__file__))
    os.rename(new_file, os.path.join(app.config['UPLOAD_FOLDER'], new_file))
    return render_template('index.html', filename=filename, new_file=new_file)


if __name__ == '__main__':
    app.run()
