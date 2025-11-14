# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

A simple Flask web application that allows users to input numbers through a modern web interface and stores them in a SQLite database.

## Development Commands

### Setup
```bash
# Install dependencies
pip install -r requirements.txt
```

### Running the Application
```bash
# Run the Flask development server
python app.py
```

The application will be available at `http://localhost:5000`

## Architecture

### Application Structure
- `app.py` - Main Flask application with routes and database logic
- `templates/index.html` - Single-page frontend with modern CSS and JavaScript
- `numbers.db` - SQLite database (auto-created on first run)

### Database Schema
The application uses a single table `numbers`:
- `id` (INTEGER PRIMARY KEY) - Auto-incrementing unique identifier
- `value` (REAL) - The stored number
- `created_at` (TIMESTAMP) - Timestamp of when the number was stored

### Routes
- `GET /` - Displays the main page with input form and list of stored numbers
- `POST /add` - Accepts JSON with a number and stores it in the database
- `DELETE /delete/<id>` - Deletes a number by ID from the database

### Frontend
The interface uses vanilla JavaScript with fetch API for AJAX requests. The UI features a gradient purple theme with smooth animations and responsive design.
