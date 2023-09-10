from flask import Flask
from adafruit_servokit import ServoKit

app = Flask(__name__)
kit = ServoKit(channels=16)
servo = 2

lr_pos = 90  # starting position for servo 0 (left-right)
ud_pos = 90  # starting position for servo 1 (up-down)

@app.route('/up')
def move_up():
    global ud_pos
    if ud_pos < 180:
        ud_pos -= 5
        kit.servo[1].angle = ud_pos
    return "Moved Up"

@app.route('/down')
def move_down():
    global ud_pos
    if ud_pos > 0:
        ud_pos += 5
        kit.servo[1].angle = ud_pos
    return "Moved Down"

@app.route('/left')
def move_left():
    global lr_pos
    if lr_pos > 0:
        lr_pos += 5
        kit.servo[0].angle = lr_pos
    return "Moved Left"

@app.route('/right')
def move_right():
    global lr_pos
    if lr_pos < 180:
        lr_pos -= 5
        kit.servo[0].angle = lr_pos
    return "Moved Right"

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5500)
