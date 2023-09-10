"""
Title: Stream video from a Raspberry Pi to a web browser
Author: Xukyo
Publication Date: 10 Aug 2023
Source: https://www.aranacorp.com/en/stream-video-from-a-raspberry-pi-to-a-web-browser/

Description:
This code is based on the article mentioned above. Some modifications have been made to fit specific requirements.
"""

# Streaming as a series of JPEG images using Flask and OpenCV, known as MJPEG streaming.

from flask import Flask, render_template, Response
import cv2
# import cvzone # Read the fps rate for tesing

app = Flask(__name__)

@app.route('/')
def index():
    """Video streaming home page."""
    return render_template('index.html')

def gen():
    """Video streaming generator function."""
    cap = cv2.VideoCapture(0)
    # Size that my webcam that supports
    cap.set(3,1280)
    cap.set(4,720)
    
    # FPS testing
    # fpsReader = cvzone.FPS()
    
    while True:
        ret,frame = cap.read()
        # fps, frame = fpsReader.update(frame,pos=(50,80),color=(0,255,0),scale=5,thickness=2)
        ret, jpeg = cv2.imencode('.jpg', frame)
        frame = jpeg.tobytes()
        yield (b'--frame\r\n'
        b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')
        
    vs.release()
    cv2.destroyAllWindows() 

@app.route('/video_feed')
def video_feed():
    """Video streaming route. Put this in the src attribute of an img tag."""
    return Response(gen(),mimetype='multipart/x-mixed-replace; boundary=frame')

if __name__ == '__main__': 
    app.run(host='0.0.0.0', port = 6600, debug=True, threaded=True)
