#!/usr/bin/env python3
# tasks.py, a simple tasks manager.
# Author: Julien Pecqueur (julien@peclu.net)
# License: GPL
# Icons from http://www.icone-png.com

# Imports
import bottle, ui, config

# Create a bottle application
app = bottle.Bottle()

# Errors
@app.error(404)
def error404(error):
    return('(404) nothing here... are you lost?')

#@app.error(500)
def error500(error):
    return('(500) stupid programmer!')

# Static files
@app.route('/s/<filename>')
def server_static(filename):
    return(bottle.static_file(filename, root='./static/'))

# Routes
@app.route('/')
@app.route('/<page>')
@app.route('/<page>/<mode>')
@app.route('/<page>/<mode>/<oid>')
def tasks(page='tasks', mode=None, oid=None):
    return(ui.process(bottle.request, page, mode, oid))

# Run the application
if __name__ == "__main__":
    bottle.run(app, host=config.HOST, port=config.PORT, \
               debug=config.DEBUG, reloader=config.RELOADER)
