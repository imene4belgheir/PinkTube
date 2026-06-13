
from flask import Flask, jsonify
import os
import logging
from config import *
from utils import register_filters
from routes import routes

# Setup logging
logging.basicConfig(level=LOG_LEVEL, format=LOG_FORMAT)

# Create Flask app
app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = MAX_CONTENT_LENGTH

# Register template filters
register_filters(app)

# Register routes blueprint
app.register_blueprint(routes)

# Error handlers
@app.errorhandler(404)
def not_found(e):
    return jsonify({'error': 'Not found'}), 404

@app.errorhandler(500)
def error(e):
    return jsonify({'error': 'Server error'}), 500

# Main entry point
if __name__ == '__main__':
    os.makedirs(UPLOAD_FOLDER, exist_ok=True)
    app.run(debug=True, host='0.0.0.0', port=5000, threaded=True)