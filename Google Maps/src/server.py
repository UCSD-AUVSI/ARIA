from flask import Flask, url_for, request
from werkzeug.contrib.cache import SimpleCache
app = Flask(__name__)
cache = SimpleCache()

app.config["SERVER_NAME"] = "localhost:5000"

@app.route("/", methods=['GET', 'POST'])
def getFlightPlan():
    list = []
    index = 0

    while True:
        lat = "data[" + str(index) +"][lat]"
        lng = "data["+ str(index) +"][lng]"
        typeField = "data[" + str(index) + "][type]"
        if lat in request.form.keys() and lng in request.form.keys():
            list += [{
                "latitude": request.form[lat],
                "longitude": request.form[lng],
                "type": request.form[typeField]
            }]
        else:
            break
        index += 1

    for dictItem in list:
        print "longitude : " + str(dictItem["longitude"])
        print "latitude : " + str(dictItem["latitude"])
        print "type : " + str(dictItem["type"])
        print

    return list

with app.app_context():
    url_for('static', filename='gmaps.html')
if __name__ == "__main__":
    app.run()