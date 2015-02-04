from flask import Flask
# Only requirement from Flask constructor is the name of the main module.
# Flask uses this to determine the root path of the app 
# so that it can find resource files relative to the location of the app.
app = Flask(__name__)

@app.route('/')
def hello():
    return "Hello, World!"

if __name__ == '__main__':
    # If you do'nt include '0.0.0.0', this application won't 
    # be visible from outside of this machine (e.g. host machine).
    app.run(host='0.0.0.0');
