from flask import Flask, request, jsonify
from jarvismain import main  # Import your Jarvis function

app = Flask(__name__)

@app.route('/ask_jarvis', methods=['POST'])
def ask_jarvis():
    data = request.json
    user_input = data.get('user_input')
    
    if user_input:
        response = main(user_input)  # Call your processing function
        return jsonify({"response": response})
    
    return jsonify({"error": "No input provided"}), 400

if __name__ == '__main__':
    app.run(debug=True)
