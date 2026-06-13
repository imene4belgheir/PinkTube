"""
All Flask routes in one file using Blueprint
"""
from flask import Blueprint, render_template, request, jsonify
import os
from helpers import *
from config import *

routes = Blueprint('routes', __name__)

@routes.route('/')
def index():
    return render_template('index.html')

@routes.route('/library')
def library():
    data = read_json(VIDEO_INDEX_FILE) or {'videos': []}
    return render_template('library.html', videos=data.get('videos', []))

@routes.route('/player')
def player():
    video_id = request.args.get('video')
    if not video_id:
        return "No video specified", 400
    
    metadata_path = os.path.join(UPLOAD_FOLDER, video_id, 'metadata.json')
    if not os.path.exists(metadata_path):
        return f"Video not found: {video_id}", 404
    
    return render_template('player.html', video_id=video_id)

@routes.route('/api/video/<video_id>/metadata')
def api_metadata(video_id):
    metadata_path = os.path.join(UPLOAD_FOLDER, video_id, 'metadata.json')
    metadata = read_json(metadata_path)
    
    if not metadata:
        return jsonify({'error': 'Not found'}), 404
    
    return jsonify(metadata)

@routes.route('/api/video/<video_id>/segments/<resolution>/status')
def api_segment_status(video_id, resolution):
    metadata_path = os.path.join(UPLOAD_FOLDER, video_id, 'metadata.json')
    metadata = read_json(metadata_path)
    
    if not metadata:
        return jsonify({'error': 'Not found'}), 404
    
    video_folder = os.path.join(UPLOAD_FOLDER, video_id)
    status = get_segment_status(video_folder, resolution, metadata)
    
    return jsonify(status)

@routes.route('/upload', methods=['POST'])
def upload():
    if 'video' not in request.files:
        return jsonify({'error': 'No file'}), 400
    
    file = request.files['video']
    if file.filename == '':
        return jsonify({'error': 'No file selected'}), 400
    
    # Get custom parameters with logging
    segment_duration = int(request.form.get('segment_duration', DEFAULT_SEGMENT_DURATION))
    buffer_size = int(request.form.get('buffer_size', DEFAULT_BUFFER_SIZE))
    cache_expiry = int(request.form.get('cache_expiry', DEFAULT_CACHE_EXPIRY))
    
    print(f"=== UPLOAD PARAMETERS ===")
    print(f"Segment Duration: {segment_duration}")
    print(f"Buffer Size: {buffer_size}")
    print(f"Cache Expiry: {cache_expiry}")
    print(f"========================")
    
    result = process_upload(file, UPLOAD_FOLDER, VIDEO_INDEX_FILE, RESOLUTIONS,
                           segment_duration, buffer_size, cache_expiry)
    
    if result['success']:
        return jsonify(result)
    return jsonify(result), 500