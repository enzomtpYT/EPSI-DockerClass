# Flask Docker Application

A production-ready Flask REST API with PostgreSQL database, containerized with Docker and served using Gunicorn WSGI server.

## 📋 Table of Contents

- [Features](#features)
- [Tech Stack](#tech-stack)
- [Project Structure](#project-structure)
- [Prerequisites](#prerequisites)
- [Quick Start](#quick-start)
- [Configuration](#configuration)
- [API Endpoints](#api-endpoints)
- [Development](#development)
- [Production Deployment](#production-deployment)
- [Docker Commands](#docker-commands)
- [Troubleshooting](#troubleshooting)

## ✨ Features

- **RESTful API** with Flask blueprints
- **PostgreSQL** database with Peewee ORM
- **Production WSGI server** using Gunicorn with 4 workers
- **Multi-stage Docker build** for optimized image size
- **Health check endpoints** for monitoring
- **Hot-reload development** environment
- **Database connection pooling** with proper lifecycle management
- **HTML frontend** for viewing items

## 🛠 Tech Stack

- **Python 3.9**
- **Flask 3.1.2** - Web framework
- **Gunicorn 23.0.0** - Production WSGI server
- **Peewee 3.18.2** - ORM for database operations
- **PostgreSQL 18** - Database
- **Docker & Docker Compose** - Containerization

## 📁 Project Structure

```
.
├── docker-compose.yml          # Production Docker Compose configuration
├── docker-compose-dev.yml      # Development Docker Compose configuration
├── Dockerfile                  # Production multi-stage Dockerfile
├── Dockerfile-dev              # Development Dockerfile with hot-reload
├── makefile                    # Convenience commands
├── requirements.txt            # Python dependencies
├── .env.example                # Environment variables template
└── src/
    ├── index.py                # Main Flask application
    ├── wsgi.py                 # WSGI entry point for Gunicorn
    ├── lib/
    │   └── postdb.py           # Database configuration and initialization
    ├── models/
    │   └── item.py             # Item model definition
    ├── routes/
    │   ├── __init__.py         # Blueprint exports
    │   └── api/
    │       ├── health.py       # Health check endpoint
    │       └── items.py        # Items CRUD endpoints
    └── templates/
        └── items_list.html     # HTML template for item listing
```

## 📦 Prerequisites

- **Docker** (version 20.10+)
- **Docker Compose** (version 2.0+)
- Make (optional, for using makefile commands)

## 🚀 Quick Start

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd Docker
   ```

2. **Create environment file**
   ```bash
   cp .env.example .env
   ```

3. **Start the application (Production)**
   ```bash
   make start
   # or
   docker compose up --build -d
   ```

4. **Access the application**
   - Web UI: http://localhost:5000
   - Health check: http://localhost:5000/api/v1/health
   - API: http://localhost:5000/api/v1/items

## ⚙️ Configuration

### Environment Variables

Create a `.env` file based on `.env.example`:

```bash
# Flask Configuration
FLASK_ENV=production
FLASK_DEBUG=0

# PostgreSQL Configuration
POSTGRES_USER=auser
POSTGRES_PASSWORD=password
POSTGRES_DB=appdb

# Database URL (uses above variables)
DATABASE_URL=postgresql://${POSTGRES_USER}:${POSTGRES_PASSWORD}@db:5432/${POSTGRES_DB}
```

### Gunicorn Configuration

The production setup uses Gunicorn with the following settings (configured in `Dockerfile`):
- **Workers**: 4 parallel worker processes
- **Timeout**: 120 seconds per request
- **Bind**: 0.0.0.0:5000
- **Logging**: Access and error logs to stdout/stderr

## 🌐 API Endpoints

### Health Check
```http
GET /api/v1/health
```
**Response:**
```json
{
  "status": "ok"
}
```

### List All Items
```http
GET /api/v1/items
```
**Response:**
```json
{
  "status": "ok",
  "data": [
    {
      "id": 1,
      "name": "Sample Item",
      "description": "This is a sample item."
    }
  ]
}
```

### Create Item
```http
POST /api/v1/items
Content-Type: application/json

{
  "name": "New Item",
  "description": "Item description"
}
```
**Response:**
```json
{
  "status": "ok",
  "message": "Item created"
}
```

### HTML View
```http
GET /
```
Returns an HTML page listing all items with styling.

## 🔧 Development

### Start Development Environment

Development mode includes:
- Live code reload (changes reflect immediately)
- Volume mounting (no rebuild needed)
- Debug mode enabled
- Exposed PostgreSQL port (5432)

```bash
make start-dev
# or
docker compose -f docker-compose-dev.yml up --build -d
```

### View Logs

```bash
# All services
docker compose logs -f

# Specific service
docker compose logs -f web
docker compose logs -f db
```

### Access Database

```bash
# PostgreSQL CLI
docker exec -it docker-db-1 psql -U auser -d appdb

# List tables
\dt

# Query items
SELECT * FROM items;
```

### Run Python Shell

```bash
docker exec -it docker-web-1 python
```

## 🚀 Production Deployment

The production setup uses:
- **Multi-stage Docker build** for smaller images
- **Gunicorn WSGI server** with multiple workers
- **Optimized Python bytecode compilation**
- **Health checks** for container orchestration
- **Automatic restarts** on failure

### Build and Deploy

```bash
make start
# or
docker compose up --build -d
```

### Check Service Health

```bash
docker compose ps
```

### Stop Services

```bash
docker compose down
```

### Stop and Remove Volumes

```bash
docker compose down -v
```

## 🐳 Docker Commands

### Makefile Commands

```bash
make start          # Start production environment
make start-dev      # Start development environment
```

### Manual Docker Compose Commands

```bash
# Build and start services
docker compose up --build -d

# View running containers
docker compose ps

# Stop services
docker compose stop

# Start existing containers
docker compose start

# Remove containers (keeps volumes)
docker compose down

# Remove containers and volumes
docker compose down -v

# View logs
docker compose logs -f

# Rebuild specific service
docker compose build web

# Execute command in container
docker compose exec web bash
```

## 🔍 Troubleshooting

### Database Connection Issues

**Problem**: `Database connection failed`

**Solution**:
1. Check if database is healthy: `docker compose ps`
2. Verify environment variables in `.env`
3. Check database logs: `docker compose logs db`

### Port Already in Use

**Problem**: `port is already allocated`

**Solution**:
1. Stop conflicting services using port 5000 or 5432
2. Or modify ports in `docker-compose.yml`

### Container Won't Start

**Problem**: Container exits immediately

**Solution**:
1. Check logs: `docker compose logs web`
2. Verify Dockerfile syntax
3. Ensure all dependencies are in `requirements.txt`

### Connection Pool Issues

**Problem**: `Connection already opened` errors

**Solution**: The application now properly manages connections per request. If you still see this:
1. Ensure you're using the latest version of the code
2. Check that `db.is_closed()` checks are in place
3. Restart services: `docker compose restart web`

### Module Not Found Errors

**Problem**: `ModuleNotFoundError` in Gunicorn

**Solution**:
1. Verify `wsgi.py` has proper path setup
2. Rebuild containers: `docker compose up --build -d`
3. Check import paths are correct

## 📝 Notes

- The development environment mounts your local code, so changes reflect immediately without rebuild
- The production environment compiles Python bytecode for better performance
- Database data persists in Docker volumes even when containers are removed
- Health checks ensure services are ready before dependent services start

## 🔒 Security: Non-root runtime user

For improved security the production image runs the application as a dedicated non-root user by default. The `Dockerfile` creates an `appuser` account (UID/GID 1000 by default) and switches to that user before starting Gunicorn. This reduces the blast radius if a process is compromised and avoids running services as root inside containers.

Customizing UID/GID

If you need the container files to match a host user (for bind mounts or CI systems), you can build the image with custom UID/GID:

```bash
docker build \
  --build-arg APP_UID=$(id -u) \
  --build-arg APP_GID=$(id -g) \
  -t td_docker:latest .
```

Or set build args in `docker-compose.yml`:

```yaml
services:
  web:
    build:
      context: .
      dockerfile: Dockerfile
      args:
        APP_UID: 1000
        APP_GID: 1000
```

Notes:
- The default user created is `appuser` with UID/GID 1000. You can change the username by passing `APP_USER` at build time if required.
- The runtime user has no login shell by default (`/bin/false`) — change this only for debug images.
