from flask import Flask, request, render_template, redirect, jsonify
from supabase import create_client, Client
import random
from dotenv import load_dotenv
import os
import psycopg2
from psycopg2 import sql
import logging

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

app = Flask(__name__)
BUCKET_NAME = "gcpbucket"

# Load environment variables from .env file
load_dotenv()

# Initialize Supabase client for storage
SUPABASE_URL = os.getenv("SUPABASE_URL")  # Load Supabase URL from .env
SUPABASE_KEY = os.getenv("SUPABASE_KEY")   # Load Supabase Key from .env
supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

# Supabase PostgreSQL connection URL
DATABASE_URL = os.getenv("DATABASE_URL")  # Format: postgresql://postgres:[PASSWORD]@db.cyqhfqflmxgfljsyfclb.supabase.co:5432/postgres

def get_db_connection():
    """Create and return a connection to the Supabase PostgreSQL database"""
    try:
        logger.info("Connecting to Supabase PostgreSQL database")
        connection = psycopg2.connect(DATABASE_URL)
        logger.info("Database connection successful")
        return connection
    except Exception as e:
        logger.error(f"Database connection error: {e}")
        raise

def upload_file(s_file, d_file_name):
    # Read the contents of the FileStorage object into a bytes object
    s_file.seek(0)  # Ensure the file pointer is at the beginning
    file_content = s_file.read()
    
    try:
        # Upload the file to Supabase storage
        response = supabase.storage.from_(BUCKET_NAME).upload(d_file_name, file_content)
        logger.info(f"Upload response: {response}")
        
        # Get the public URL of the uploaded file
        public_url = supabase.storage.from_(BUCKET_NAME).get_public_url(d_file_name)
        logger.info(f"Public URL: {public_url}")
        return public_url
    except Exception as e:
        logger.error(f"Failed to upload file: {e}")
        raise

def generate_name_tag(name):
    number = random.randint(100000, 999999)
    return f"{name}_{number}"

# Initialize database and create table if not exists
def init_db():
    conn = get_db_connection()
    cursor = conn.cursor()
    
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS blogs (
            id SERIAL PRIMARY KEY,
            title TEXT NOT NULL,
            image_url TEXT NOT NULL,
            content TEXT NOT NULL,
            author TEXT NOT NULL
        )
    ''')
    
    conn.commit()
    cursor.close()
    conn.close()
    logger.info("Database initialized successfully")

@app.route('/', methods=['GET'])
def get_blogs():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT id, title, image_url, content, author FROM blogs')
    blogs = cursor.fetchall()
    cursor.close()
    conn.close()
    return render_template('blogs.html', blogs=blogs), 200

@app.route('/blogs', methods=['GET', 'POST'])
def create_blog():
    if request.method == 'POST':
        title = request.form.get('title')
        content = request.form.get('content')
        author = request.form.get('author')
        image = request.files.get('image')

        if not title or not content or not author or not image:
            return jsonify({'error': 'Missing required fields'}), 400

        image_url = upload_file(image, generate_name_tag(author))

        conn = get_db_connection()
        cursor = conn.cursor()
        
        cursor.execute(
            'INSERT INTO blogs (title, image_url, content, author) VALUES (%s, %s, %s, %s)',
            (title, image_url, content, author)
        )
            
        conn.commit()
        cursor.close()
        conn.close()
        return redirect('/')
    return render_template('create_blogs.html')

if __name__ == '__main__':
    try:
        init_db()
        logger.info("Starting Flask application")
        app.run(host='0.0.0.0', debug=True)
    except Exception as e:
        logger.error(f"Application error: {e}")