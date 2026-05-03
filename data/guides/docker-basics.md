# Docker Basics for Beginners

## What is Docker

Docker is a platform that lets you package an application and everything it needs — code, runtime, libraries, config — into a single unit called a **container**. Containers run the same way on every machine, which solves the classic "it works on my machine" problem.

Key terms:
- **Image** — a read-only template describing what the container will contain.
- **Container** — a running instance of an image.
- **Dockerfile** — a text file with instructions for building an image.
- **Registry** — a server that stores and serves images (Docker Hub is the default public registry).

## Installing Docker

**macOS and Windows:** Download Docker Desktop from [https://www.docker.com/products/docker-desktop](https://www.docker.com/products/docker-desktop). Docker Desktop includes Docker Engine, Docker CLI, and Docker Compose.

**Ubuntu Linux:**
```bash
sudo apt-get update
sudo apt-get install docker.io
sudo systemctl start docker
sudo systemctl enable docker
sudo usermod -aG docker $USER  # lets you run docker without sudo
```

Log out and back in after adding yourself to the `docker` group.

Verify the install:
```bash
docker --version
docker run hello-world
```

## Writing a Dockerfile

A Dockerfile is a list of instructions. Docker reads them top to bottom and builds a layer for each one.

```dockerfile
# Start from an official base image
FROM python:3.11-slim

# Set working directory inside the container
WORKDIR /app

# Copy dependency list first (improves layer caching)
COPY requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application
COPY . .

# Tell Docker which port the app will use
EXPOSE 8000

# Command to run when the container starts
CMD ["python", "app.py"]
```

Common base images:
- `python:3.11-slim` — Python 3.11, minimal Debian, ~45MB
- `node:18-slim` — Node.js 18, minimal Debian
- `nginx:alpine` — Nginx web server on Alpine Linux, ~5MB
- `ubuntu:22.04` — Full Ubuntu (use slim variants when possible)

## Building and Running

**Build an image:**
```bash
docker build -t my-app:latest .
```
- `-t my-app:latest` tags the image as `my-app` with the `latest` tag.
- `.` tells Docker to use the current directory as the build context.

**Run a container:**
```bash
docker run -p 8000:8000 my-app:latest
```
- `-p 8000:8000` maps port 8000 on your machine to port 8000 in the container.

**Run in the background (detached mode):**
```bash
docker run -d -p 8000:8000 --name my-running-app my-app:latest
```

**Stop and remove:**
```bash
docker stop my-running-app
docker rm my-running-app
```

## Common Docker Commands

| Command | What it does |
|---------|-------------|
| `docker ps` | List running containers |
| `docker ps -a` | List all containers (including stopped) |
| `docker images` | List local images |
| `docker logs <name>` | View container output |
| `docker exec -it <name> bash` | Open a shell inside a running container |
| `docker build -t <tag> .` | Build image from Dockerfile in current directory |
| `docker pull <image>` | Download an image from Docker Hub |
| `docker rmi <image>` | Remove a local image |
| `docker system prune` | Remove stopped containers and unused images |

## Docker Compose

Docker Compose lets you define and run multiple containers together using a `docker-compose.yml` file.

```yaml
version: "3.9"
services:
  web:
    build: .
    ports:
      - "8000:8000"
    environment:
      - DATABASE_URL=postgresql://db:5432/myapp
    depends_on:
      - db
  db:
    image: postgres:15
    environment:
      - POSTGRES_DB=myapp
      - POSTGRES_PASSWORD=secret
    volumes:
      - db-data:/var/lib/postgresql/data
volumes:
  db-data:
```

**Start all services:**
```bash
docker compose up
```

**Start in background:**
```bash
docker compose up -d
```

**Stop all services:**
```bash
docker compose down
```

## Common Beginner Mistakes

**Mistake: Copying everything including node_modules or __pycache__**
Fix: Add a `.dockerignore` file:
```
node_modules/
__pycache__/
.git/
.env
```

**Mistake: Running as root inside the container**
Fix: Add a non-root user to your Dockerfile:
```dockerfile
RUN useradd -m appuser
USER appuser
```

**Mistake: Putting ENV secrets in the Dockerfile**
Fix: Use environment variables at runtime:
```bash
docker run -e SECRET_KEY=... my-app
```
Or use a `.env` file with Docker Compose — never commit it to git.

**Mistake: Not tagging images**
Fix: Always use a specific tag. `latest` is a convention, not a guarantee of freshness.
