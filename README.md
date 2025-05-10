# Flask Blog Application with Supabase Storage

This is a simple blog application built with Flask and Supabase for file storage. The application allows users to create blog posts with titles, content, author information, and image uploads.

## Features

- Create blog posts with titles, content, and author information
- Upload images for blog posts (stored in Supabase)
- View all blog posts on the home page
- SQLite database for storing blog post data

## Setup

1. Clone this repository
2. Install dependencies:
   ```
   pip install flask supabase python-dotenv
   ```
3. Create a `.env` file with your Supabase credentials:
   ```
   SUPABASE_URL=your_supabase_url
   SUPABASE_KEY=your_supabase_key
   ```
4. Run the application:
   ```
   python app.py
   ```

## Project Structure

- `app.py`: Main application file with routes and database setup
- `templates/`: HTML templates for the application
  - `blogs.html`: Template for displaying all blogs
  - `create_blogs.html`: Form template for creating new blogs
- `blogs.db`: SQLite database file 