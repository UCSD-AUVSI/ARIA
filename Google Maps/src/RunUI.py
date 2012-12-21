from PyQt4 import QtWebKit, QtCore, QtGui
from UiWindow import Ui_MainWindow
from flask import Flask, url_for
from GoogleMapsPy import GoogleMapsPy
from GoogleMapsObjects import Coordinate, Polygon, PolyLine
import threading
import server
import os

with server.app.app_context():
    url_for('static', filename='gmaps.html')

def ser():
    server.app.run()

def ui():
    app = QtGui.QApplication(sys.argv)
    MainWindow = QtGui.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())

if __name__ == '__main__':
    import sys

    centerMap = Coordinate(0,0)
    coordList = [Coordinate(0,0), Coordinate(10,-10), Coordinate(10,10)]

    mapObject = GoogleMapsPy(centerMap, 5, 'ROADMAP')

    #Create polygons
    # coordList2 = [Coordinate(0,0), Coordinate(10,-10), Coordinate(10,10)]
    # poly2 = Polygon(coordList2)
    # mapObject.createPolygon(poly2)

    cwd = os.curdir
    with open(cwd+'/static/gmaps.html', 'w') as file:
      file.write(mapObject.getHtml())

    uiThread = threading.Thread(name="ui thread", target=ui)
    serverThread = threading.Thread(name="server thread", target=ser)
    serverThread.setDaemon(True)

    uiThread.start()
    serverThread.start()
