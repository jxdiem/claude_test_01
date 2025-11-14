# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

A comprehensive Flask web application for farm management with multiple modules including:
- Number storage (original feature)
- Farm management system (terreni, trattori, attrezzi, animali, colture, personale, magazzino, manutenzioni, finanze)
- SQLite database with persistent storage
- Dockerized deployment ready for production
- CI/CD pipeline with security scanning

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
- `templates/` - HTML templates for different modules
  - `menu.html` - Main menu page
  - `index.html` - Original numbers storage page
  - `farm.html` - Farm management dashboard
- `farm_management.db` - SQLite database (auto-created on first run)
- `Dockerfile` - Multi-stage Docker build configuration
- `docker-compose.yml` - Local development with Docker
- `render.yaml` - Render.com deployment configuration
- `.github/workflows/ci-cd.yml` - CI/CD pipeline with security scanning

### Database Schema
The application uses multiple tables for comprehensive farm management:
- **numbers** - Original number storage feature
- **terreni** - Land/field management
- **trattori** - Tractor and machinery tracking
- **attrezzi** - Equipment and tools inventory
- **animali** - Livestock management
- **colture** - Crop management
- **personale** - Staff/employee records
- **magazzino** - Warehouse inventory (seeds, fertilizers, etc.)
- **manutenzioni** - Maintenance records
- **finanze** - Financial transactions (expenses and revenues)

### Main Routes
- `GET /` - Main menu page
- `GET /health` - Health check endpoint (for monitoring)
- `GET /numbers` - Numbers storage page
- `GET /farm` - Farm management dashboard
- `POST /add` - Add a number
- `DELETE /delete/<id>` - Delete a number
- Multiple API routes for farm management (`/api/terreni`, `/api/trattori`, etc.)

### Frontend
The interface uses vanilla JavaScript with fetch API for AJAX requests. The UI features a gradient purple theme with smooth animations and responsive design.

## Docker Deployment

### Build and Run with Docker

```bash
# Build the Docker image
docker build -t farm-management-app .

# Run with volume persistence
docker run -d \
  -p 5000:5000 \
  -v farm_data:/data \
  --name farm-app \
  farm-management-app
```

### Run with Docker Compose

```bash
# Start the application
docker-compose up -d

# View logs
docker-compose logs -f

# Stop the application
docker-compose down
```

The application will be available at `http://localhost:5000`

## Deploy to Render.com

### Prerequisites
- GitHub account
- Render.com account (free tier available)

### Deployment Steps

1. **Push to GitHub**
   ```bash
   git add .
   git commit -m "Ready for deployment"
   git push origin main
   ```

2. **Connect to Render.com**
   - Go to [render.com](https://render.com)
   - Click "New +" → "Blueprint"
   - Connect your GitHub repository
   - Render will automatically detect `render.yaml`

3. **Configure (if needed)**
   - The `render.yaml` file includes all necessary configuration
   - A persistent disk is automatically created for SQLite database
   - Environment variables are pre-configured

4. **Deploy**
   - Click "Apply" to deploy
   - Render will build the Docker image and deploy
   - Your app will be live at `https://your-app-name.onrender.com`

### Important Notes
- **Free Tier Limitations**: The app will sleep after 15 minutes of inactivity (cold start ~30 seconds)
- **Database Persistence**: Uses a 1GB persistent disk (included in free tier)
- **Auto-Deploy**: Pushing to `main` branch triggers automatic deployment
- **Health Checks**: Render monitors the `/health` endpoint

## CI/CD Pipeline

### GitHub Actions Workflow

The repository includes a comprehensive CI/CD pipeline that runs on every push and pull request:

#### 1. Code Quality & Security Linting
- **Flake8**: Python code linting
- **Bandit**: Security vulnerability scanning for Python code
- **Safety**: Dependency vulnerability checking

#### 2. Docker Build & Container Scanning
- **Docker Build**: Multi-stage optimized build
- **Trivy**: Container vulnerability scanning
- **GitHub Container Registry**: Automatic image publishing

#### 3. CodeQL Analysis
- GitHub's native security scanning
- Identifies security vulnerabilities in code

### Viewing Security Reports
- Go to your repository → Security tab → Code scanning alerts
- Review Trivy and CodeQL findings
- Download Bandit reports from Actions artifacts

## Security Features

### Container Security
- **Non-root user**: App runs as `appuser` (UID 1000)
- **Multi-stage build**: Minimal attack surface
- **No unnecessary packages**: Only runtime dependencies included
- **Volume permissions**: Proper ownership for persistent data

### Application Security
- **Health checks**: Monitor application status
- **Error handling**: Proper exception handling in routes
- **Input validation**: Number validation in routes

### Continuous Security
- **Automated scanning**: Every commit is scanned for vulnerabilities
- **Dependency tracking**: Safety checks for known vulnerabilities
- **Container scanning**: Trivy scans for OS and library vulnerabilities

## Environment Variables

- `DATA_DIR` - Directory for database storage (default: `.`, production: `/data`)
- `FLASK_ENV` - Flask environment (development/production)
- `PORT` - Port to run the application (default: 5000)

## Troubleshooting

### Local Development
```bash
# Check if app is running
curl http://localhost:5000/health

# View Docker logs
docker logs farm-app

# Access container shell
docker exec -it farm-app /bin/bash
```

### Render.com
- Check logs in Render dashboard
- Verify persistent disk is mounted
- Ensure environment variables are set
- Check health check endpoint is responding
