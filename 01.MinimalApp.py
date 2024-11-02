from flask import Flask

app = Flask(__name__)

@app.route("/")
def hello_world():
    return "<p>Hello, World!</p>"

@app.route("/products")
def products():
    return "<h1>Products page</h1>"

if __name__ == '__main__':
    app.run(debug=True, port=8000)