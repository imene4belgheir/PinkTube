# 🎬 PinkTube - Video Streaming Platform

A beautiful custom video streaming platform built with Flask featuring adaptive bitrate streaming, segment-based playback, and automatic quality switching.

## ✨ Features

- 📤 **Video Upload** - Upload videos with custom segment duration, buffer size, and cache settings
- 🎥 **Multi-Quality Streaming** - Automatic generation of 480p, 720p, 1080p, and 4K variants
- ⚡ **Adaptive Bitrate (ABR)** - Automatic quality switching based on bandwidth + manual control
- 📼 **Segment Management** - View and manage segments with thumbnails and progress tracking
- 🎨 **Beautiful UI** - Modern pink-themed responsive design inspired by YouTube
- 📱 **Fully Responsive** - Works perfectly on desktop, tablet, and mobile devices
- 🔄 **Smooth Quality Switching** - Maintains video position when changing quality
- 📊 **Buffer Status Display** - Visual progress bars showing preloaded segments

## 🚀 Quick Start

### Prerequisites

Before you start, make sure you have:
- **Python 3.7 or higher** - [Download here](https://www.python.org/)
- **FFmpeg** - Required for video processing
  - **Windows**: Download from [ffmpeg.org](https://ffmpeg.org/download.html)
  - **Mac**: `brew install ffmpeg`
  - **Linux**: `sudo apt-get install ffmpeg`
- **Git** - [Download here](https://git-scm.com/)
- **pip** - Usually comes with Python

### Installation (5 Steps)

**Step 1: Clone the repository**
```bash
git clone https://github.com/yourusername/pinktube.git
cd pinktube
```

**Step 2: Create virtual environment**
```bash
python -m venv venv
```

**Step 3: Activate virtual environment**
- **Windows**: `venv\Scripts\activate`
- **Mac/Linux**: `source venv/bin/activate`

**Step 4: Install dependencies**
```bash
pip install -r requirements.txt
```

**Step 5: Run the application**
```bash
python app.py
```

Open your browser to: **http://localhost:5000** 🎉

## 📁 Project Structure

```
pinktube/
├── app.py              # Main Flask app entry point
├── routes.py           # All Flask routes (Blueprint)
├── helpers.py          # Business logic & video processing
├── config.py           # Configuration settings
├── utils.py            # Template filters & utilities
├── requirements.txt    # Python dependencies
├── static/
│   ├── style.css       # All styling (pink theme)
│   ├── pinktube2.png   # App logo
│   └── videos/         # Uploaded videos (auto-created)
└── templates/
    ├── index.html      # Upload page
    ├── library.html    # Video library/playlist
    └── player.html     # Video player with ABR
```

## 🎯 How to Use

### 1. Upload a Video

1. Go to the **Upload** page (home)
2. Click to select a video file (MP4, AVI, MOV, MKV, WebM)
3. Set custom options:
   - **Segment Duration**: How long each segment is (2-10 seconds)
   - **Buffer Size**: How many segments to preload (1-10)
   - **Cache Expiry**: How long segments stay in cache (5 min - 24 hours)
4. Click **Upload & Process**
5. Wait for 480p to process (instant playback!)
6. Other qualities process in background

### 2. Watch Videos

1. Go to **Library** to see all your videos
2. Click any video thumbnail to play
3. Video player opens with:
   - Current quality displayed
   - Settings ⚙️ button to change quality
   - Segment list on the right with thumbnails
   - Buffer status bar below segments

### 3. Switch Quality

- Click **⚙️ Settings** button → Select quality
- Video stays at same position (timestamp alignment)
- Segment list updates automatically
- Missing segments show as "Segment X"

## ⚙️ Configuration

Edit `config.py` to customize:

```python
# Video processing
DEFAULT_SEGMENT_DURATION = 4      # seconds per segment
DEFAULT_BUFFER_SIZE = 3           # segments to preload
DEFAULT_CACHE_EXPIRY = 3600       # cache duration in seconds

# Resolutions to generate
RESOLUTIONS = {
    '480p': {'width': 854, 'height': 480, 'bitrate': '2500k'},
    '720p': {'width': 1280, 'height': 720, 'bitrate': '5000k'},
    '1080p': {'width': 1920, 'height': 1080, 'bitrate': '8000k'},
    '4k': {'width': 3840, 'height': 2160, 'bitrate': '15000k'}
}

# Server
UPLOAD_FOLDER = 'static/videos'
MAX_FILE_SIZE = 500 * 1024 * 1024  # 500MB
```

## 🎓 Key Technologies

| Technology | Purpose |
|-----------|---------|
| **Flask** | Web framework & routing |
| **FFmpeg** | Video segmentation & encoding |
| **Python** | Backend logic |
| **HTML5** | Video player structure |
| **CSS3** | Beautiful pink styling |
| **JavaScript** | Player controls & ABR logic |
| **JSON** | Metadata & playlist format |

## 🎬 How It Works (Behind the Scenes)

### Upload Process

1. **480p First** - Generated immediately (30-60 sec) → Instant playback
2. **Background Processing** - Other qualities (720p, 1080p, 4K) process in parallel
3. **Segmentation** - Each quality is split into small MP4 segments
4. **Metadata** - JSON file tracks all segments, durations, and locations

### Playback Process

1. **Load Metadata** - Get segment info from JSON
2. **Start Segment 1** - Begin playback immediately
3. **Preload Ahead** - Load next 3 segments in advance
4. **Sequential Play** - Auto-play next segment when current ends
5. **Quality Switching** - If user changes quality, find matching position and continue
6. **ABR** - Monitor bandwidth and auto-switch if needed

### Adaptive Bitrate (ABR)

- ✅ **Manual**: Click settings to pick quality
- ✅ **Automatic**: Monitors download speed
  - Fast network → 1080p or 4K
  - Slow network → 480p or 720p
  - Adapts in real-time based on buffering

## 🔧 API Reference

The backend provides these API endpoints:

```
GET  /                           # Upload page
GET  /library                    # Video library
GET  /player?video=<id>          # Video player
POST /upload                     # Upload video
GET  /api/video/<id>/metadata    # Get video info
GET  /api/video/<id>/segments/<res>/status  # Check segments
```

## 🎨 Customization

### Change Colors

Edit `static/style.css`:
```css
/* Main pink color */
background: #ff69b4;     /* Hot pink */

/* Dark pink */
background: #ff1493;     /* Deep pink */

/* Light pink */
background: #ffb6d9;     /* Light pink */
```

### Change Logo

1. Create your own 150px wide image
2. Save as `static/pinktube2.png`
3. Refresh browser

### Adjust Defaults

Edit `config.py` for:
- Default segment duration
- Default buffer size
- Resolutions to generate
- Upload file size limit

## ⚠️ Troubleshooting

### "ffmpeg not found"
- **Windows**: Make sure FFmpeg is in your System PATH
  - Download from https://ffmpeg.org
  - Add to Environment Variables
- **Mac**: Run `brew install ffmpeg`
- **Linux**: Run `sudo apt-get install ffmpeg`

### "Video doesn't appear in library"
- Check that `static/videos/` folder exists
- Upload a new video
- Refresh the page

### "Segments not scrolling"
- Clear browser cache: `Ctrl + Shift + Delete`
- Hard refresh: `Ctrl + F5`
- Check browser console for errors (F12)

### "Quality button doesn't work"
- Make sure all qualities have finished processing
- Check that metadata.json exists in video folder
- Try a different quality

### "Video is black/stuttering"
- Increase buffer size in upload settings
- Reduce segment duration
- Check internet connection speed

## 📊 Example Workflow

```
1. Visit http://localhost:5000
   ↓
2. Upload video (MyVideo.mp4)
   ↓
3. Set: Duration=4s, Buffer=3, Expiry=1h
   ↓
4. Click "Upload & Process"
   ↓
5. Wait 1 minute (480p processing)
   ↓
6. Auto-redirected to player
   ↓
7. Watch video (480p playing immediately)
   ↓
8. Other qualities finish in background
   ↓
9. Click ⚙️ Settings to switch quality
   ↓
10. Video continues from same position
```

## 🚀 Performance Tips

- **Segment Duration**: 4 seconds = good balance
- **Buffer Size**: 3 segments = smooth playback
- **Cache Expiry**: 1 hour = good for testing
- **Resolutions**: Generate up to source quality only (no upscaling)

## 🌟 Features Explained

### Metadata JSON
Each video has a `metadata.json` file containing:
- All segment filenames
- Segment durations
- Bitrate info for each quality
- Processing status

This is the "playlist" - replaces traditional HLS .m3u8 files!

### Segment List
Right sidebar showing:
- Thumbnail for each segment
- Progress bar within segment
- Missing segments (if deleted)
- Current segment highlighted

Click any segment to jump to it!

### Buffer Status
Under segment list shows:
- How many segments are preloaded
- Progress bar (X of Y segments)
- Smooth playback indicator

## 📄 License

This project is open source under the MIT License. See LICENSE file for details.

## 🤝 Contributing

Have ideas? Found a bug?

1. Fork the repository
2. Create a feature branch: `git checkout -b feature/awesome-feature`
3. Make your changes
4. Commit: `git commit -m "Add awesome feature"`
5. Push: `git push origin feature/awesome-feature`
6. Create a Pull Request

## 🙏 Acknowledgments

- **Flask** - Web framework
- **FFmpeg** - Video processing
- **YouTube** - UI inspiration
- **You** - For using PinkTube!

## 📧 Support

Have questions or found a bug?
- Open an Issue on GitHub
- Check existing Issues for solutions
- Read the code comments

## 🎉 What's Next?

Future features to add:
- [ ] User authentication & accounts
- [ ] Video analytics & watch history
- [ ] Comments & likes
- [ ] Video thumbnails/covers
- [ ] Search functionality
- [ ] Database instead of JSON
- [ ] Live streaming support
- [ ] DRM protection


**Made with 💖 and Pink** ✨

Happy streaming! 🎬
