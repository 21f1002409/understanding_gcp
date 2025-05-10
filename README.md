# Flask Blog Application with Supabase Storage and PostgreSQL

This is a simple blog application built with Flask, using Supabase for both file storage and PostgreSQL database services. The application allows users to create blog posts with titles, content, author information, and image uploads.

## Features

- Create blog posts with titles, content, and author information
- Upload images for blog posts (stored in Supabase Storage)
- View all blog posts on the home page
- Supabase PostgreSQL database for storing blog post data

## Setup

1. Clone this repository
2. Install dependencies:
   ```
   pip install -r requirements.txt
   ```
3. Create a `.env` file with your Supabase credentials (see `.env.example` for template):
   ```
   # Supabase credentials for storage
   SUPABASE_URL=your_supabase_url
   SUPABASE_KEY=your_supabase_key
   
   # Supabase PostgreSQL connection URL
   DATABASE_URL=postgresql://postgres:[YOUR-PASSWORD]@db.cyqhfqflmxgfljsyfclb.supabase.co:5432/postgres
   
   # Bucket name for file storage
   BUCKET_NAME=gcpbucket
   ```
4. Run the application:
   ```
   python app.py
   ```

## Database Configuration

The application uses Supabase's PostgreSQL service. You'll need to:

1. Create a Supabase project at [https://supabase.com](https://supabase.com)
2. Get your PostgreSQL connection URL from the Supabase dashboard
3. Create a bucket for file storage in the Supabase storage section
4. Add the connection URL and other credentials to your `.env` file

The application will automatically create the necessary tables in your Supabase PostgreSQL database when it starts.

## Project Structure

- `app.py`: Main application file with routes and database setup
- `templates/`: HTML templates for the application
  - `blogs.html`: Template for displaying all blogs
  - `create_blogs.html`: Form template for creating new blogs
- `.env.example`: Template for environment variables
- `requirements.txt`: List of Python dependencies 