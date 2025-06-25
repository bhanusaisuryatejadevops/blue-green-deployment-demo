from flask import Flask
app = Flask(__name__)

@app.route('/')
def home():
    return "Hello from GREEN version!"  # change this to BLUE for blue deployment

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)

