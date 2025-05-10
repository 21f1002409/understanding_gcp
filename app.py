from flask import Flask, request, render_template, redirect, jsonify
from supabase import create_client, Client
import sqlite3
import random
from dotenv import load_dotenv
import os

app = Flask(__name__)
DB_NAME = 'blogs.db'
BUCKET_NAME = "gcpbucket"

# Load environment variables from .env file
load_dotenv()

# Initialize Supabase client
url = os.getenv("SUPABASE_URL")  # Load Supabase URL from .env
key = os.getenv("SUPABASE_KEY")   # Load Supabase Key from .env
supabase: Client = create_client(url, key)

def upload_file(s_file, d_file_name):
    # Read the contents of the FileStorage object into a bytes object
    s_file.seek(0)  # Ensure the file pointer is at the beginning
    file_content = s_file.read()
    
    try:
        # Upload the file to Supabase storage
        response = supabase.storage.from_(BUCKET_NAME).upload(d_file_name, file_content)
        print(f"Upload response: {response}")  # Log the response for debugging
        
        # Get the public URL of the uploaded file
        public_url = supabase.storage.from_(BUCKET_NAME).get_public_url(d_file_name)
        print(f"Public URL: {public_url}")  # Log the public URL for debugging
        return public_url
    except Exception as e:
        # Log or handle the error
        print(f"Failed to upload file: {e}")
        raise

def generate_name_tag(name):
    number = random.randint(100000, 999999)
    return f"{name}_{number}"

# Initialize database and create table if not exists
def init_db():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS blogs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            image_url TEXT NOT NULL,
            content TEXT NOT NULL,
            author TEXT NOT NULL
        )
    ''')
    conn.commit()
    conn.close()

@app.route('/', methods=['GET'])
def get_blogs():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute('SELECT id, title, image_url, content, author FROM blogs')
    blogs = cursor.fetchall()
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

        conn = sqlite3.connect(DB_NAME)
        cursor = conn.cursor()
        cursor.execute('INSERT INTO blogs (title, image_url, content, author) VALUES (?, ?, ?, ?)', (title, image_url, content, author))
        conn.commit()
        conn.close()
        return redirect('/')
    return render_template('create_blogs.html')

if __name__ == '__main__':
    init_db()
    app.run(debug=True)