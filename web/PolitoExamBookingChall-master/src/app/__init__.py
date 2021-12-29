from flask import Flask, render_template, Response, request, jsonify

app = Flask(__name__)


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/nope')
def nope():
    response = Response()
    response.headers['Refresh'] = '5; url=./'
    response.data = 'You don\'t need this'
    return response


@app.route('/bakand',  methods=['GET', 'POST'])
def bakand():
    appelli = [
        {'id_verbale': 736, 'cod_ins': 'B0000M', 'data_appello': '2021-07-13', 'docente': 'NELLO SICUREZZA'},
        {'id_verbale': 999, 'cod_ins': '<3CYCL3S', 'data_appello': '2021-07-14', 'docente': 'CEFFO BRUTTO'},
        {'id_verbale': 532, 'cod_ins': '01ELEET', 'data_appello': '2021-07-05', 'docente': 'ROBOT MR'},
    ]
    if request.method == 'POST':
        content = request.json
        if not any(d['id_verbale'] == content['id_verbale'] for d in appelli):
            return "Error!<br>No exam with such id"
        else:
            appello = next((a for a in appelli if a['id_verbale'] == content['id_verbale']), None)
            if appello is None:
                return "Error!<br>Something went wrong, please try again"
            else:
                if appello['cod_ins'] != content['cod_ins']:
                    return "Error!<br>Course codes mismatch"
                elif appello['data_appello'] != content['data_appello']:
                    return "Error!<br>Exam dates mismatch"
                elif appello['docente'] != content['docente']:
                    return "Error!<br>Exam teachers mismatch"
                else:
                    msg = "Success!<br>You will shortly be registered to the exam"
                    if content['id_verbale'] == 532:
                        msg += "<br>ptm{S3rveR_s1d3_v4liDa7ion_go3s_bRRRRRR}"
                    return msg

    else:
        msg = 'You broke something :('
    return msg


if __name__ == '__main__':
    app.run(host='0.0.0.0')
