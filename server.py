from flask import Flask, jsonify
from thermo import read_sensor

app = Flask(__name__, static_url_path='')
app.url_map.strict_slashes = False

@app.route('/')
def index():
    pass

# Retrieve Temperatures from the Thermo sensors
@app.route('/temps', methods=['GET'])
def temps():
    ## 
    return jsonify(Temp());

# Retrieve single temp from Thermo sensor
@app.route('/temp/{<temp_type>', methods=['GET'])
def temp(temp_type):
    if(temp_type == 'hlt'):
        return Temp.hlt
    if(temp_type == 'mlt'):
        return Temp.mlt
    if(temp_type == 'bk'):
        return Temp.bk
    else:
        return 'Invalid request {temp_type} is not a temp type'
    
if __name__ == '__main__':
    app.run(debug=True, port=80, host='0.0.0.0')
    
def addition(num1, num2):
    return num1+num2

class Temp:
    def __init__(self):
        temps = read_sensor()
        self.hlt = temps[0][1]
        self.mlt = temps[1][1]
        self.bk  = temps[2][1]
        
        