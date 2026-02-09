# Explore "flask" module and create a web server using Flask and Python

# pip install flask


from flask import Flask

app = Flask(__name__)


@app.route("/")
def hello_world():
    return "<p>Hello, World!</p>"


app.run()