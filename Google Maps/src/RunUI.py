from PyQt4 import QtWebKit, QtCore, QtGui
from GoogleMapsPy import Coordinate, GoogleMapsPy, Polygon
from UiWindow import Ui_MainWindow
from flask import Flask, url_for
import threading
import server

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

	mapObject = GoogleMapsPy(centerMap, 5, 'ROADMAP', coordList)

	#Create polygons
	coordList2 = [Coordinate(0,0), Coordinate(10,-10), Coordinate(10,10)]
	poly2 = Polygon(coordList2)
	mapObject.createPolygon(poly2)

	with open('static/gmaps.html', 'w') as file:
		file.write(mapObject.getHtml())

	t1 = threading.Thread(name="ui thread", target=ui)
	t2 = threading.Thread(name="server thread", target=ser)
	t2.setDaemon(True)

	t1.start()
	t2.start()
