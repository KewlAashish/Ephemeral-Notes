from flask import Flask, request, jsonify, render_template
import redis
import os

app = Flask(__name__)

# Connect to Redis
db = redis.Redis(host=os.getenv('REDIS_HOST', 'localhost'), port=6379, decode_responses=True)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/add_note', methods=['POST'])
def add_note():
    data = request.json
    note_id = data.get('id')
    note_text = data.get('text')
    expiry = int(data.get('expiry', 60))  # Default expiry: 60 seconds
    
    db.setex(note_id, expiry, note_text)
    return jsonify({'message': 'Note added', 'id': note_id, 'expiry': expiry})

@app.route('/get_note/<note_id>', methods=['GET'])
def get_note(note_id):
    note = db.get(note_id)
    if note:
        return jsonify({'id': note_id, 'text': note})
    else:
        return jsonify({'message': 'Note expired or not found'}), 404

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
