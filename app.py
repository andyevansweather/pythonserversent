# @app.route("/")
# def index():
#     debug_template = """
#      <html>
#        <head>
#        </head>
#        <body>
#          <h1>Server sent events</h1>
#          <div id="event"></div>
#          <script type="text/javascript">
#
#          var eventOutputContainer = document.getElementById("event");
#          var evtSrc = new EventSource("/subscribe");
#
#             var source = new EventSource("{{ url_for('sse.stream') }}");
#             source.addEventListener('greeting', function(event) {
#                 var data = JSON.parse(event.data);
#                 // do what you want with this data
#             }, false);
#
#          </script>
#        </body>
#      </html>
#     """
#     return(debug_template)

from __future__ import print_function
import gevent
import gevent.monkey
from gevent.pywsgi import WSGIServer
gevent.monkey.patch_all()
from time import sleep
from flask import Flask, request, Response, render_template
from flask_cors import CORS

app = Flask(__name__)

# Allow CORS for client to access server sent events
CORS(app)

def kill_motors():
    return 'done'

def event_stream():
    count = 0
    while True:
        gevent.sleep(0.01)

        yield 'data: %s\n\n' % count
        count += 1

def move_backwards():
    count = 0
    while True:
        gevent.sleep(0.01)
        yield 'data: %s\n\n' % count
        count += 1

def move_right():
    count = 0
    while True:
        gevent.sleep(0.01)
        yield 'data: %s\n\n' % count
        count += 1

def move_left():
    count = 0
    while True:
        gevent.sleep(0.01)
        yield 'data: %s\n\n' % count
        count += 1

def event_end():
    count = 0
    while True:
        gevent.sleep(0.1)
        yield 'data: %s\n\n' % count
        count = 0

@app.route('/my_event_source')
def sse_request():
    return Response(
        event_stream(),
        mimetype='text/event-stream')

@app.route('/backwards')
def sse_backwards():
    return Response(
        move_backwards(),
        mimetype='text/event-stream')

@app.route('/right')
def sse_right():
    return Response(
        move_right(),
        mimetype='text/event-stream')

@app.route('/left')
def sse_left():
    return Response(
        move_left(),
        mimetype='text/event-stream')

@app.route('/end_motor_source')
def event_end():
    kill_motors()
    print('entered!!')
    return 'end'

@app.route('/')
def page():
    return render_template('index.html')

if __name__ == '__main__':
    http_server = WSGIServer(('0.0.0.0', 80), app)
    http_server.serve_forever()