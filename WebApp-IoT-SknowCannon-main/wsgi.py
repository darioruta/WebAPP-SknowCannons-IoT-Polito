import cherrypy
import os
from webserver import *
import sys


if __name__ == '__main__':
	
		
	conf={
		'/':{
				'request.dispatch':cherrypy.dispatch.MethodDispatcher(),
				'tools.staticdir.root': os.path.abspath(os.getcwd()),
			},
		 '/css':{
		 'tools.staticdir.on': True,
		 'tools.staticdir.dir':'css'
		 },
		 '/js':{
		 'tools.staticdir.on': True,
		 'tools.staticdir.dir':'js'
		 },
          '/images':{
		 'tools.staticdir.on': True,
		 'tools.staticdir.dir':'images'
		 },
          '/fonts':{
		 'tools.staticdir.on': True,
		 'tools.staticdir.dir':'fonts'
		 },
	}
	
	#cherrypy.config.update({"server.socket_port": 8199})
	cherrypy.tree.mount(webServer("ciao"),'/',conf)
	cherrypy.engine.start()
	cherrypy.engine.block()