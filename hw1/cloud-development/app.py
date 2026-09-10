from flask import Flask, jsonify, request
import datetime
import os

app = Flask(__name__)
messages = []

@app.route('/health', methods=['GET'])
def health():
    """Health check endpoint"""
    return jsonify({
        "status": "healthy",
        "timestamp": datetime.datetime.now().isoformat(),
        "service": "CMPE789-HW1"
    }), 200

@app.route('/message', methods=['POST'])
def post_message():
    """Store a message"""
    data = request.get_json()
    if not data or 'text' not in data:
        return jsonify({"error": "Missing 'text' field"}), 400

    msg = {
        "id": len(messages),
        "text": data['text'],
        "timestamp": datetime.datetime.now().isoformat()
    }
    messages.append(msg)
    return jsonify(msg), 201

@app.route('/message', methods=['GET'])
def get_messages():
    """Retrieve all messages"""
    return jsonify({"messages": messages, "count": len(messages)}), 200

@app.route('/message/<int:msg_id>', methods=['GET'])
def get_message(msg_id):
    """Retrieve specific message"""
    if msg_id < 0 or msg_id >= len(messages):
        return jsonify({"error": "Message not found"}), 404
    return jsonify(messages[msg_id]), 200

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=False)
