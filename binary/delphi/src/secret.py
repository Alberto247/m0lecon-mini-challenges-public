from flask import Flask, render_template, request, make_response
app = Flask(__name__)


@app.route("/")
def delphi():
    resp = make_response(render_template("index.html"))
    return resp

@app.route("/secret", methods = ['POST'])
def secret():
    password = "magic_is_fake"
    secret = request.form['secret']
    if (secret == password):
      return "Here's the prophecy, I forecast some points for you :)\n ptm{l3t5_g0_t0_gr33c3}"
    if password.startswith(secret):
      return "Something's missing..."
    else:
      return "Wrong secret :("

if __name__ == "__main__":
    app.run(host = '0.0.0.0', debug = False)
