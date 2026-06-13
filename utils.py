"""
Utility functions and Flask template filters
"""
from datetime import datetime

def format_duration(seconds):
    """Format seconds into readable duration"""
    if not seconds:
        return "0:00"
    hrs = int(seconds // 3600)
    mins = int((seconds % 3600) // 60)
    secs = int(seconds % 60)
    if hrs > 0:
        return f"{hrs}:{mins:02d}:{secs:02d}"
    return f"{mins}:{secs:02d}"

def format_date(iso_date):
    """Format ISO date into readable format"""
    if not iso_date:
        return ""
    try:
        dt = datetime.fromisoformat(iso_date)
        return dt.strftime("%b %d, %Y")
    except:
        return ""

def register_filters(app):
    """Register all template filters with Flask app"""
    app.template_filter('format_duration')(format_duration)
    app.template_filter('format_date')(format_date)