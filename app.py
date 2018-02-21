# author: oskar.blom@gmail.com
#
# Make sure your gevent version is >= 1.0
from gevent.wsgi import WSGIServer
from flask import Flask
from flask_sse import sse

app = Flask(__name__)
app.config["REDIS_URL"] = "redis://localhost"
app.register_blueprint(sse, url_prefix='/stream')

@app.route('/send')
def send_message():
    sse.publish({"message": "Hello!"}, type='greeting')
    return "Message sent!"


# Client code consumes like this.
@app.route("/")
def index():
    debug_template = """
     <html>
       <head>
       </head>
       <body>
         <h1>Server sent events</h1>
         <div id="event"></div>
         <script type="text/javascript">

         var eventOutputContainer = document.getElementById("event");
         var evtSrc = new EventSource("/subscribe");

            var source = new EventSource("{{ url_for('sse.stream') }}");
            source.addEventListener('greeting', function(event) {
                var data = JSON.parse(event.data);
                // do what you want with this data
            }, false);

         </script>
       </body>
     </html>
    """
    return(debug_template)


if __name__ == "__main__":
    app.debug = True
    server = WSGIServer(("", 80), app)
    server.serve_forever()
    # Then visit http://localhost:5000 to subscribe 
    # and send messages by visiting http://localhost:5000/publish