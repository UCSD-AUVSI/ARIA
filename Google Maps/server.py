from flask import Flask, url_for
app = Flask(__name__)

app.config["SERVER_NAME"] = "localhost:5000"

@app.route("/", methods=['GET', 'POST'])
def hello():
    return "Hello World!"
with app.app_context():
	url_for('static', filename='map.html')
if __name__ == "__main__":
    app.run()