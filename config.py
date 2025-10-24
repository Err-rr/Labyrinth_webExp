import os

# Flask configuration
SECRET_KEY = 'lab1r1nth_s3cr3t_k3y_2024_v1'  # INTENTIONALLY WEAK - this will be leaked via backup
DEBUG = True
UPLOAD_FOLDER = 'uploads'
MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 16MB max upload

# JWT Configuration
JWT_SECRET_KEY = SECRET_KEY  # Same as Flask secret for simplicity
JWT_ALGORITHM = 'HS256'

# Database
DATABASE = 'labyrinth.db'

# Session configuration
SESSION_COOKIE_HTTPONLY = False  # INTENTIONAL VULNERABILITY
SESSION_COOKIE_SECURE = False
SESSION_COOKIE_SAMESITE = None

# CORS (intentionally permissive for CTF)
CORS_ORIGINS = '*'

# Developer notes (will be visible in backup):
# TODO: Change SECRET_KEY before production deployment
# TODO: Enable HTTPS and secure cookies
# TODO: Implement rate limiting on /api endpoints
# TODO: Add CSRF protection
# TODO: Remove /debug endpoint
# FIXME: SQLi in /search endpoint - use parameterized queries!