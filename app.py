from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/hello', methods=['POST'])
def hello():
    name = request.form.get('name')
    return render_template('home.html', name=name)

if __name__ == '__main__':
    app.run(debug=True)



# index.html
# register.html
# profile.html


