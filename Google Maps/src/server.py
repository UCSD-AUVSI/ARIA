from flask import Flask, url_for, request
app = Flask(__name__)

app.config["SERVER_NAME"] = "localhost:5000"

@app.route("/", methods=['GET', 'POST'])
def getFlightPlan():
	list = []
	index = 0

	while True:
		lat = "path[" + str(index) +"][lat]"
		lng = "path["+ str(index) +"][lng]"
		if lat in request.form.keys() and lng in request.form.keys():
			list += [(request.form[lat],request.form[lng])]
		else:
			break 
		index += 1

	return str(list)

with app.app_context():
	url_for('static', filename='gmaps.html')
if __name__ == "__main__":
	app.run()