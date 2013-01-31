from PyQt4 import QtWebKit, QtCore, QtGui
from flask import Flask, url_for
import threading
import os
import sys

from gmappy import Gmappy, Coordinate, Map, Polyline, Marker
from UiWindow import Ui_MainWindow
import server

with server.app.app_context():
    url_for('static', filename='gmappy.html')

def ser():
    server.app.run()

def ui():
    app = QtGui.QApplication(sys.argv)
    MainWindow = QtGui.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())

if __name__=="__main__":

    center = Coordinate(latitude=0, longitude=0, altitude=0, ctype="waypoint", duration=0)

    map_options = {
        "center"    : center,
        "zoom"      : 5,
        "mapTypeId" : 'roadmap',
    }
    map_ = Map(options = map_options)


    path_array = [
        Coordinate(latitude=0, longitude=0, altitude=0, ctype="takeoff", duration=0),
        Coordinate(latitude=10, longitude=10, altitude=0, ctype="waypoint", duration=0),
        Coordinate(latitude=15, longitude=-15, altitude=0, ctype="loiter", duration=5),
        Coordinate(latitude=0, longitude=0, altitude=0, ctype="land", duration=0),
    ]
    path_options = {
        "path"  : path_array
    }
    path = Polyline(options = path_options)

    marker_options = {
        "position"  : Coordinate(latitude=0, longitude=0, altitude=10, ctype="waypoint", duration=0),
        "title"     : "marker 1"
    }
    marker = Marker(options = marker_options)

    API_KEY = "AIzaSyDUqZDJn8yWjIKJ4nUsHQGuEAvZHar41rs"

    gmappy = Gmappy(map_, API_KEY, path)
    gmappy.add_marker(marker)

    gmappy.write()

    uiThread = threading.Thread(name="ui thread", target=ui)
    serverThread = threading.Thread(name="server thread", target=ser)
    serverThread.setDaemon(True)

    serverThread.start()
    ui()
