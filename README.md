# TempShare

A simple, secure file and URL sharing platform built with Django.

🚀 **Live Demo**: [http://13.53.205.148](http://13.53.205.148)

## Features

- **File Sharing**: Upload and share files with auto-expiring links
- **URL Shortening**: Create short, shareable links for long URLs
- **Auto-Expiration**: All shared content automatically expires after a set duration
- **Clean UI**: Modern, responsive interface with Bootstrap styling
- **Background Cleanup**: Automated task to remove expired content

## Tech Stack

- **Backend**: Django (Python)
- **Frontend**: Bootstrap, CSS
- **Database**: SQLite (development) / PostgreSQL (production)
- **Deployment**: Configured for cloud deployment with Gunicorn

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/MudaSir-Latif/tempshare.git
   cd tempshare
   ```

2. Create a virtual environment and activate it:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Run migrations:
   ```bash
   python manage.py migrate
   ```

5. Start the development server:
   ```bash
   python manage.py runserver
   ```

6. Visit `http://127.0.0.1:8000` in your browser

## Usage

### Sharing Files
1. Navigate to the home page
2. Select a file to upload
3. Choose expiration time (optional)
4. Click "Share File"
5. Copy and share the generated link

### Sharing URLs
1. Navigate to the home page
2. Enter the URL you want to shorten
3. Choose expiration time (optional)
4. Click "Share URL"
5. Copy and share the generated short link

## Management Commands

Clean up expired content manually:
```bash
python manage.py cleanup_expired
```

## Project Structure

```
tempshare/
├── core/              # Core sharing functionality
│   ├── models.py      # FileShare and URLShare models
│   ├── views.py       # Upload and sharing views
│   └── management/    # Custom management commands
├── frontend/          # Frontend templates and views
│   ├── templates/     # HTML templates
│   └── views.py       # Frontend page views
├── static/            # Static CSS files
└── temshare_proj/     # Project settings
```

## Configuration

Key settings in `temshare_proj/settings.py`:
- `MEDIA_ROOT`: Location for uploaded files
- `ALLOWED_HOSTS`: Hosts allowed to serve the application
- Database configuration for production deployment

## Deployment

### Current Deployment
This application is currently deployed on **AWS EC2** with the following setup:
- **Server**: Ubuntu EC2 instance
- **Web Server**: Nginx (reverse proxy)
- **Application Server**: Gunicorn
- **Live URL**: [http://13.53.205.148](http://13.53.205.148)

### Deployment Architecture
```
Internet → Nginx (Port 80) → Gunicorn (WSGI) → Django Application
                     ↓
              Static Files (served by Nginx)
              Media Files (served by Nginx)
```

### Deployment Configuration
The project includes configuration files for deployment:
- `Procfile`: For Heroku/similar PaaS
- `requirements.txt`: Python dependencies
- Nginx configuration for reverse proxy setup
- Gunicorn WSGI server configuration

### Manual Deployment Steps (AWS EC2)
1. Launch an Ubuntu EC2 instance
2. Install Python, Nginx, and required dependencies
3. Clone the repository
4. Set up virtual environment and install requirements
5. Configure Gunicorn as a systemd service
6. Configure Nginx as reverse proxy
7. Set up static and media file serving
8. Configure security groups (port 80/443)

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is open source and available under the MIT License.

## Author

MudaSir-Latif

## Support

For issues and questions, please open an issue on GitHub.
