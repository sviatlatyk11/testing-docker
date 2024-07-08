from flask import Flask, request, jsonify
from flask_cors import CORS
from modules import Database, Email, Telegram

app = Flask(__name__)
CORS(app)


@app.route('/register', methods=['POST'])
def register():
    result, message, email = Database.add_to_database(request.get_json())

    if result.acknowledged:
        # Send notification via Telegram
        Telegram.send_message(message)
        Email.send_email(email)
        return jsonify({"message": "Registration successful"}), 200
    else:
        return jsonify({"error": "Failed to register"}), 500


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8088)

