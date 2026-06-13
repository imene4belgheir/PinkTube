"""
Configuration file - All settings in one place
"""

# Flask App Configuration
UPLOAD_FOLDER = 'static/videos'
MAX_CONTENT_LENGTH = 500 * 1024 * 1024  # 500MB
VIDEO_INDEX_FILE = 'static/video_index.json'

# Video Resolution Settings
RESOLUTIONS = {
    '480p': {'width': 854, 'height': 480, 'bitrate': '1000k', 'bandwidth': 1000000},
    '720p': {'width': 1280, 'height': 720, 'bitrate': '2500k', 'bandwidth': 2500000},
    '1080p': {'width': 1920, 'height': 1080, 'bitrate': '5000k', 'bandwidth': 5000000},
    '4k': {'width': 3840, 'height': 2160, 'bitrate': '15000k', 'bandwidth': 15000000}
}

# Segmentation Settings
DEFAULT_SEGMENT_DURATION = 4  # seconds
DEFAULT_BUFFER_SIZE = 3  # number of segments to preload
DEFAULT_CACHE_EXPIRY = 3600  # seconds (1 hour)

# ABR (Adaptive Bitrate) Settings
ABR_CHECK_INTERVAL = 5  # seconds between bandwidth checks
MIN_BUFFER_FOR_SWITCH = 5.0  # minimum buffer before allowing quality switch
BANDWIDTH_SAMPLE_COUNT = 10  # number of samples for bandwidth calculation

# Allowed file extensions
ALLOWED_EXTENSIONS = {'mp4', 'avi', 'mov', 'mkv', 'webm'}

# Logging Configuration
LOG_LEVEL = 'INFO'
LOG_FORMAT = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'