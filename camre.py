import cv2
from flask import Flask, Response, render_template_string

app = Flask(__name__)

# HTML šablona s video streamem
HTML_TEMPLATE = '''
<!doctype html>
<html lang="en">
  <head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <title>Live Video Feed</title>
    <style>
      body {
        margin: 0;
        overflow: hidden;
      }
      #videoContainer {
        position: relative;
        width: 100vw;
        height: 100vh;
      }
      #videoFeed {
        width: 100%;
        height: 100%;
        object-fit: contain;
      }
      #controls {
        position: absolute;
        top: 10px;
        left: 10px;
        background: rgba(0, 0, 0, 0.5);
        padding: 5px;
        border-radius: 5px;
        color: white;
      }
    </style>
  </head>
  <body>
    <div id="videoContainer">
      <img id="videoFeed" src="{{ url_for('video_feed') }}" />
      <div id="controls">
        <button onclick="toggleFullScreen()">Full Screen</button>
        <input type="range" id="zoomSlider" min="1" max="5" step="0.1" value="1" />
        <label for="zoomSlider">Zoom</label>
      </div>
    </div>
    <script>
      // Toggle full screen mode
      function toggleFullScreen() {
        if (!document.fullscreenElement) {
          document.documentElement.requestFullscreen();
        } else if (document.exitFullscreen) {
          document.exitFullscreen();
        }
      }

      // Zoom functionality
      document.getElementById('zoomSlider').addEventListener('input', function() {
        var zoomLevel = this.value;
        document.getElementById('videoFeed').style.transform = 'scale(' + zoomLevel + ')';
      });
    </script>
  </body>
</html>
'''

def generate_frames():
    # Inicializace kamery (0 je obvykle výchozí kamera)
    camera = cv2.VideoCapture(0)

    while True:
        # Zachycení snímku
        success, frame = camera.read()
        if not success:
            break

        # Konverze snímku na JPEG
        ret, buffer = cv2.imencode('.jpg', frame)
        if not ret:
            break

        # Vytvoření rámce pro streamování
        frame = buffer.tobytes()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

@app.route('/')
def index():
    return render_template_string(HTML_TEMPLATE)

@app.route('/video_feed')
def video_feed():
    return Response(generate_frames(),
                    mimetype='multipart/x-mixed-replace; boundary=frame')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
