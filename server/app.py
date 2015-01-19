from flask import Flask, render_template
app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/add', methods=['POST'])
def add():
    pass

@app.route('/remove', methods=['POST'])
def remove():
    pass

@app.route('/sign-up', methods=['POST'])
def sign_up():
    pass

@app.route('/log-in', methods=['POST'])
def log_in():
    pass

if __name__ == '__main__':
    app.run(host='0.0.0.0')