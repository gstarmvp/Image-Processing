import os
from datetime import datetime
from flask import Flask, request, flash, url_for, redirect, \
     render_template, abort, send_from_directory, abort
from werkzeug import secure_filename
from werkzeug.exceptions import RequestEntityTooLarge

ALLOWED_EXTENSIONS = set(['txt', 'bmp', 'png', 'jpg', 'jpeg'])

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
def upload_file():
    if request.method == 'POST':
        file = request.files['file']
        if file and allowed_file(file.filename):
            try:
                filename = secure_filename(file.filename)
                file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
                file.close()
                flash('success')
                return redirect(url_for('image', filename=filename))
            except RequestEntityTooLarge as e:
                flash('data too large')
                return redirect(url_for('upload_file'))
           
    return render_template('upload.html')
if __name__ == '__main__':
    app.run()
