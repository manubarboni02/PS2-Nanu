from flask import Flask, render_template, request
import serial
import serial.tools.list_ports
from datetime import datetime

app = Flask(__name__)
ports = serial.tools.list_ports.comports()
serialInst = serial.Serial()
portsList = []
temperature = 25
messages = ''

for one in ports:
    portsList.append(str(one))
    print(str(one))

com = input("Select port #: ")
for i in range(len(portsList)):
    if portsList[i].startswith("COM" + str(com)):
        use = "COM" + str(com)
        print(use)

serialInst.baudrate = 9600
serialInst.port = use
serialInst.open()

def get_messages_from_arduino():
    serialInst.write(b'm')
    messages = []
    for _ in range(10):  # Assuming you want to retrieve the last 10 messages
        message = serialInst.readline(30).decode("utf-8").strip()
        if message:
            messages.append(message)
    return messages

def send_message_to_arduino(message):
    serialInst.write(message.encode())

@app.route('/')
def index():
   try:
        messages = get_messages_from_arduino()
        #messages = [message if message is not None else "" for message in messages]
        return render_template('index.html', messages = messages)
   except Exception as e:
        print("Error:", e)  # Print the error for debugging purposes
        return "An error occurred while fetching messages."


@app.route('/update', methods=['POST'])
def update():
    if request.form['action'] == 'on':
        serialInst.write(b'1')
    elif request.form['action'] == 'off':
        serialInst.write(b'0')
    elif request.form['action'] == 'read_temp':
        temperature = serialInst.readline().decode('utf-8').strip()
        return temperature
    elif request.form['action'] == 'get_temp_now':
        serialInst.write(b'r')
        temperature = serialInst.readline().decode('utf-8').strip()
        return temperature
    #elif request.form['action'] == 'get_messages':
        #messages = get_messages_from_arduino()
        #return messages
    elif request.form.get('action') == 'send_message':
        message = request.form.get('message') 
        current_time = datetime.now()
        current_time_string = current_time.strftime('%Y%m%d/%H/%M/%S')
        data_to_send = 'w ' + current_time_string + '|' + message
        serialInst.write(data_to_send.encode('utf-8'))
    return 'OK'

if __name__ == '__main__':
    app.run(debug=True)
