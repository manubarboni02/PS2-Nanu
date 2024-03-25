from flask import Flask, render_template, url_for, request, jsonify

led_state = False
temperature = 60

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html', temperature=temperature, led_state=led_state)

@app.route('/toggle_led', methods=['POST'])
def toggle_led():
    global led_state
    led_state = not led_state  # Inversarea starii LED-ului
    return jsonify({'led_state': 'on' if led_state else 'off'})

if __name__ == "__main__":
    app.run(debug=True)