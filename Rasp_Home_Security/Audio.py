from flask import Flask, jsonify
import tensorflow as tf
import numpy as np
import csv
import pyaudio
import io

# Function to get class names from YAMNet CSV
def class_names_from_csv(class_map_csv_text):
    class_map_csv = io.StringIO(class_map_csv_text)
    class_names = [display_name for (class_index, mid, display_name) in csv.reader(class_map_csv)]
    return class_names[1:]  # Skip CSV header

app = Flask(__name__)

# YAMNet setup
interpreter = tf.lite.Interpreter('lite-model_yamnet_tflite_1.tflite')
input_details = interpreter.get_input_details()
waveform_input_index = input_details[0]['index']
output_details = interpreter.get_output_details()
scores_output_index = output_details[0]['index']

class_names = class_names_from_csv(open('yamnet_class_map.csv').read())

# Audio setup
RATE = 16000
RECORD_SECONDS = 2
CHUNKSIZE = 1024
audio = pyaudio.PyAudio()
mic_index = 1  # Adjust if necessary

@app.route('/get_prediction', methods=['GET'])
def get_prediction():
    # Capture and process audio
    stream = audio.open(format=pyaudio.paInt16, channels=1, rate=RATE, input=True, frames_per_buffer=CHUNKSIZE, input_device_index=mic_index)
    frames = [stream.read(CHUNKSIZE) for _ in range(0, int(RATE / CHUNKSIZE * RECORD_SECONDS))]
    stream.stop_stream()
    stream.close()

    # Process audio for YAMNet
    waveform = np.hstack([np.frombuffer(frame, dtype=np.int16) for frame in frames])
    waveform = waveform.astype(np.float32, order='C') / 32768.0
    interpreter.resize_tensor_input(waveform_input_index, [len(waveform)], strict=True)
    interpreter.allocate_tensors()
    interpreter.set_tensor(waveform_input_index, waveform)
    interpreter.invoke()
    scores = interpreter.get_tensor(scores_output_index)

    # Get predictions
    prediction = np.mean(scores, axis=0)
    top_5 = np.argsort(prediction)[::-1][:5]
    prediction_dict = {class_names[i]: f"{prediction[i]*100:.0f}%" for i in top_5}
    
    return jsonify(prediction_dict)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=9900)
