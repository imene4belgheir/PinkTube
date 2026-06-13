"""
All business logic in one file
Separated from Flask routes
"""
import os
import uuid
import subprocess
import json
import threading
import logging
from werkzeug.utils import secure_filename
from datetime import datetime

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# ==================== FILE OPERATIONS ====================

def read_json(filepath):
    """Read JSON file safely"""
    try:
        if os.path.exists(filepath):
            with open(filepath, 'r') as f:
                return json.load(f)
    except Exception as e:
        logger.error(f"Error reading {filepath}: {e}")
    return None

def write_json(filepath, data):
    """Write JSON file safely"""
    try:
        os.makedirs(os.path.dirname(filepath), exist_ok=True)
        with open(filepath, 'w') as f:
            json.dump(data, f, indent=2)
        return True
    except Exception as e:
        logger.error(f"Error writing {filepath}: {e}")
        return False

def segment_exists(video_folder, resolution, segment_name):
    """Check if segment file exists"""
    path = os.path.join(video_folder, resolution, segment_name)
    return os.path.exists(path)

# ==================== VIDEO HELPERS ====================

def get_video_info(video_path):
    """Get video resolution and duration"""
    try:
        # Get resolution
        cmd = ['ffprobe', '-v', 'error', '-select_streams', 'v:0',
               '-show_entries', 'stream=width,height', '-of', 'json', video_path]
        result = subprocess.run(cmd, capture_output=True, text=True)
        data = json.loads(result.stdout)
        width = int(data['streams'][0]['width'])
        height = int(data['streams'][0]['height'])
        
        # Get duration
        cmd = ['ffprobe', '-v', 'error', '-show_entries', 'format=duration',
               '-of', 'json', video_path]
        result = subprocess.run(cmd, capture_output=True, text=True)
        data = json.loads(result.stdout)
        duration = float(data['format']['duration'])
        
        return width, height, duration
    except Exception as e:
        logger.error(f"Error getting video info: {e}")
        raise

def get_segment_duration(segment_path):
    """Get duration of a segment"""
    try:
        cmd = ['ffprobe', '-v', 'error', '-show_entries', 'format=duration',
               '-of', 'json', segment_path]
        result = subprocess.run(cmd, capture_output=True, text=True)
        data = json.loads(result.stdout)
        return float(data['format']['duration'])
    except:
        return 4.0  # Default

def make_thumbnail(video_path, output_path):
    """Generate thumbnail from video"""
    try:
        cmd = ['ffmpeg', '-i', video_path, '-ss', '2', '-vframes', '1',
               '-vf', 'scale=320:180', '-y', output_path]
        subprocess.run(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        return True
    except:
        return False

# ==================== SEGMENTATION ====================

def segment_video(input_video, output_folder, resolution_name, width, height, bitrate):
    """Segment video into MP4 files with default 4s duration"""
    return segment_video_custom(input_video, output_folder, resolution_name, width, height, bitrate, 4)

def segment_video_custom(input_video, output_folder, resolution_name, width, height, bitrate, segment_duration):
    """Segment video into MP4 files with custom duration"""
    try:
        res_folder = os.path.join(output_folder, resolution_name)
        os.makedirs(res_folder, exist_ok=True)
        
        segment_pattern = os.path.join(res_folder, 'segment_%03d.mp4')
        
        cmd = [
            'ffmpeg', '-i', input_video,
            '-vf', f'scale={width}:{height}',
            '-c:v', 'libx264', '-preset', 'veryfast', '-crf', '23',
            '-b:v', bitrate, '-c:a', 'aac', '-b:a', '128k',
            '-f', 'segment', '-segment_time', str(segment_duration),
            '-reset_timestamps', '1', '-threads', '0',
            '-y',  # Overwrite output files
            segment_pattern
        ]
        
        logger.info(f"Segmenting with duration: {segment_duration}s")
        subprocess.run(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, check=True)
        
        # Get segment info
        segments = sorted([f for f in os.listdir(res_folder) if f.endswith('.mp4')])
        segment_list = []
        
        for idx, seg in enumerate(segments):
            seg_path = os.path.join(res_folder, seg)
            duration = get_segment_duration(seg_path)
            
            # Generate segment thumbnail
            thumb_path = os.path.join(output_folder, 'thumbnails', seg.replace('.mp4', '.jpg'))
            os.makedirs(os.path.dirname(thumb_path), exist_ok=True)
            
            thumb_cmd = ['ffmpeg', '-i', seg_path, '-ss', '0.5', '-vframes', '1',
                        '-vf', 'scale=160:90', '-y', thumb_path]
            subprocess.run(thumb_cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            
            segment_list.append({
                'index': idx,
                'filename': seg,
                'duration': duration,
                'url': f'/static/videos/{os.path.basename(output_folder)}/{resolution_name}/{seg}',
                'thumbnail': f'/static/videos/{os.path.basename(output_folder)}/thumbnails/{seg.replace(".mp4", ".jpg")}'
            })
        
        logger.info(f"Segmented {len(segments)} segments for {resolution_name}")
        return segment_list
    except Exception as e:
        logger.error(f"Segmentation error: {e}")
        raise

# ==================== UPLOAD WORKFLOW ====================

def process_upload(file, upload_folder, video_index_file, resolutions, segment_duration, buffer_size, cache_expiry):
    """Main upload workflow"""
    try:
        # Setup
        filename = secure_filename(file.filename)
        name_only = os.path.splitext(filename)[0]
        video_id = f"{name_only}-{str(uuid.uuid4())[:8]}"
        video_folder = os.path.join(upload_folder, video_id)
        os.makedirs(video_folder, exist_ok=True)
        
        # Save video
        temp_path = os.path.join(video_folder, filename)
        file.save(temp_path)
        
        # Get info
        width, height, duration = get_video_info(temp_path)
        
        # Make thumbnail
        thumb_path = os.path.join(video_folder, 'thumbnail.jpg')
        make_thumbnail(temp_path, thumb_path)
        
        # Process 480p first with custom segment duration
        segments_480p = segment_video_custom(temp_path, video_folder, '480p', 
                                      resolutions['480p']['width'],
                                      resolutions['480p']['height'],
                                      resolutions['480p']['bitrate'],
                                      segment_duration)
        
        # Create metadata
        metadata = {
            'id': video_id,
            'filename': filename,
            'duration': duration,
            'source_resolution': f"{width}x{height}",
            'upload_date': datetime.now().isoformat(),
            'segment_duration': segment_duration,
            'buffer_size': buffer_size,
            'cache_expiry': cache_expiry,
            'resolutions': {
                '480p': {
                    'width': 854, 'height': 480,
                    'bitrate': '1000k', 'bandwidth': 1000000,
                    'status': 'completed',
                    'segments': segments_480p
                },
                '720p': {'status': 'processing'},
                '1080p': {'status': 'processing'},
                '4k': {'status': 'processing'}
            }
        }
        
        # Save metadata
        metadata_path = os.path.join(video_folder, 'metadata.json')
        write_json(metadata_path, metadata)
        
        # Update index
        index = read_json(video_index_file) or {'videos': []}
        index['videos'].insert(0, {
            'id': video_id,
            'title': name_only,
            'thumbnail': f'/static/videos/{video_id}/thumbnail.jpg',
            'duration': duration,
            'upload_date': metadata['upload_date']
        })
        write_json(video_index_file, index)
        
        # Start background processing
        start_background(temp_path, video_folder, video_id, resolutions, metadata, segment_duration)
        
        return {'success': True, 'video_id': video_id}
    except Exception as e:
        logger.error(f"Upload error: {e}")
        return {'success': False, 'error': str(e)}

# ==================== BACKGROUND PROCESSING ====================

def start_background(video_path, video_folder, video_id, resolutions, metadata, segment_duration):
    """Process remaining resolutions in background"""
    def background_task():
        for res_name in ['720p', '1080p', '4k']:
            try:
                segments = segment_video_custom(video_path, video_folder, res_name,
                                        resolutions[res_name]['width'],
                                        resolutions[res_name]['height'],
                                        resolutions[res_name]['bitrate'],
                                        segment_duration)
                
                metadata['resolutions'][res_name] = {
                    'width': resolutions[res_name]['width'],
                    'height': resolutions[res_name]['height'],
                    'bitrate': resolutions[res_name]['bitrate'],
                    'bandwidth': int(resolutions[res_name]['bitrate'].replace('k', '000')),
                    'status': 'completed',
                    'segments': segments
                }
                
                write_json(os.path.join(video_folder, 'metadata.json'), metadata)
                logger.info(f"Completed {res_name} for {video_id}")
            except Exception as e:
                logger.error(f"Background error {res_name}: {e}")
                metadata['resolutions'][res_name] = {'status': 'failed', 'error': str(e)}
        
        # Cleanup
        try:
            os.remove(video_path)
        except:
            pass
    
    thread = threading.Thread(target=background_task)
    thread.daemon = True
    thread.start()

# ==================== MISSING SEGMENTS ====================

def get_segment_status(video_folder, resolution, metadata):
    """Check which segments are missing"""
    try:
        res_data = metadata.get('resolutions', {}).get(resolution, {})
        if res_data.get('status') != 'completed':
            return {'status': 'not_ready', 'available': 0, 'missing': []}
        
        segments = res_data.get('segments', [])
        missing = []
        
        for seg in segments:
            if not segment_exists(video_folder, resolution, seg['filename']):
                missing.append(seg['filename'])
        
        return {
            'status': 'partial' if missing else 'complete',
            'total': len(segments),
            'available': len(segments) - len(missing),
            'missing': missing
        }
    except Exception as e:
        logger.error(f"Error checking segments: {e}")
        return {'status': 'error', 'error': str(e)}