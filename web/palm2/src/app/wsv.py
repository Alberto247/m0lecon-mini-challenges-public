from flask import Flask, render_template, flash, request, redirect, url_for
import os
import random
import string
from werkzeug.utils import secure_filename
from base64 import b64encode

UPLOAD_FOLDER = '/app/uploads'

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

def get_random_string(length):
    letters = string.ascii_lowercase
    result_str = ''.join(random.choice(letters) for i in range(length))
    return result_str


@app.route("/", methods=['GET'])
def main():
    fried = request.args.get('f')
    if fried != None:
        out = os.path.join(fried.rsplit('/', 1)[0], "out.png")
        print(f"OUT: {out}")
        os.system(f"python /app/fryer/main.py /app/uploads/{fried} 2 1 0 200 /app/uploads/{out}")
        file = open(f'/app/uploads/{out}', "rb")
        img = b64encode(file.read()).decode("utf-8")
        return render_template("img.html", img_data=img)

    return render_template("index.html")

@app.route('/', methods=['POST'])
def upload_file():
    if request.method == 'POST':
        dnm = get_random_string(40)
        # check if the post request has the file part
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['file']
        # If the user does not select a file, the browser submits an
        # empty file without a filename.
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        if file:
            filename = secure_filename(file.filename)
            try:
                os.makedirs(os.path.join(app.config['UPLOAD_FOLDER'], dnm))
            except FileExistsError:
                pass

            file.save(os.path.join(app.config['UPLOAD_FOLDER'], dnm, filename))
            print(f"file saved {os.path.join(app.config['UPLOAD_FOLDER'], dnm, filename)}")
            return redirect( url_for('main', f=os.path.join(dnm, filename), _scheme='https', _external=True) )

if __name__ == '__main__':
    app.run(debug=False, host='0.0.0.0')
