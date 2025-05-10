# Flask Blog Application with Supabase Storage and PostgreSQL

This is a simple blog application built with Flask, Supabase for file storage, and PostgreSQL for database storage. The application allows users to create blog posts with titles, content, author information, and image uploads.

## Features

- Create blog posts with titles, content, and author information
- Upload images for blog posts (stored in Supabase Storage)
- View all blog posts on the home page
- PostgreSQL database for storing blog post data

## Setup

1. Clone this repository
2. Install dependencies:
   ```
   pip install -r requirements.txt
   ```
3. Create a `.env` file with your credentials (see `.env.example` for template):
   ```
   # Supabase credentials for storage
   SUPABASE_URL=your_supabase_url
   SUPABASE_KEY=your_supabase_key
   
   # PostgreSQL database connection parameters
   DB_USER=your_db_user
   DB_PASSWORD=your_db_password
   DB_HOST=your_db_host
   DB_PORT=5432
   DB_NAME=your_db_name
   
   # Bucket name for file storage
   BUCKET_NAME=gcpbucket
   ```
4. Run the application:
   ```
   python app.py
   ```

## Database Setup

The application will automatically create the necessary tables in your PostgreSQL database when it starts. Make sure your PostgreSQL user has the necessary permissions to create tables.

## Project Structure

- `app.py`: Main application file with routes and database setup
- `templates/`: HTML templates for the application
  - `blogs.html`: Template for displaying all blogs
  - `create_blogs.html`: Form template for creating new blogs
- `.env.example`: Template for environment variables
- `requirements.txt`: List of Python dependencies 