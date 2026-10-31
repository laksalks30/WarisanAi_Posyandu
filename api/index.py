"""
WARISAN.AI - Vercel Serverless Function Entry Point
Menyediakan interface ASGI FastAPI untuk runtime serverless Vercel Python.
"""

import sys
import os

# Menambahkan root project ke sys.path agar modul 'backend' dapat di-import
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from backend.main import app
