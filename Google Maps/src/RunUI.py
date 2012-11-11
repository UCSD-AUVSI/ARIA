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
	server.app.stop()
	return

def ui():
	app = QtGui.QApplication(sys.argv)
	MainWindow = QtGui.QMainWindow()
	ui = Ui_MainWindow()
	ui.setupUi(MainWindow)
	MainWindow.show()
	sys.exit(app.exec_())
	return

if __name__ == '__main__':
	import sys

	centerMap = Coordinate(0,0)
	coordList = [Coordinate(0,0), Coordinate(10,-20), Coordinate(120,24)]

	mapObject = GoogleMapsPy(centerMap, 5, 'ROADMAP', coordList)

	#Create polygons
	coordList2 = [Coordinate(0,0), Coordinate(30,-30), Coordinate(100,0)]
	poly2 = Polygon(coordList2)

	# mapObject.createPolygon(poly)
	mapObject.createPolygon(poly2)

	# mapObject.setPath(coordList)

	file = open('static/gmaps.html', 'w')
	file.write(mapObject.getHtml())
	file.close()

	t1 = threading.Thread(target=ui)
	t2 = threading.Thread(target=ser)
	t1.start()
	t2.start()
