# Nginx Basics

## What is Nginx

Nginx (pronounced "engine-x") is a high-performance, open-source web server and reverse proxy. It's designed to handle high traffic with low memory usage. Nginx can serve static files, proxy requests to application servers, load balance traffic, and provide other web services.

Nginx is commonly used as:
- A web server to serve static files and web applications
- A reverse proxy to forward requests to backend application servers
- A load balancer to distribute traffic across multiple servers
- An API gateway for microservices

## Installing Nginx

On Ubuntu/Debian:
```bash
sudo apt-get update
sudo apt-get install nginx
```

On macOS with Homebrew:
```bash
brew install nginx
```

After installation, start Nginx:
```bash
sudo systemctl start nginx
sudo systemctl enable nginx  # Start on boot
```

## Basic Configuration

Nginx configuration is stored in `/etc/nginx/nginx.conf` (on Linux) or `/usr/local/etc/nginx/nginx.conf` (on macOS).

The configuration file consists of directives organized in blocks:

```nginx
# Main context
user www-data;
worker_processes auto;
pid /var/run/nginx.pid;

events {
    worker_connections 768;
}

http {
    # HTTP block
    sendfile on;
    tcp_nopush on;
    tcp_nodelay on;
    keepalive_timeout 65;
    types_hash_max_size 2048;

    include /etc/nginx/mime.types;
    default_type application/octet-stream;

    access_log /var/log/nginx/access.log;
    error_log /var/log/nginx/error.log;

    gzip on;

    include /etc/nginx/conf.d/*.conf;
    include /etc/nginx/sites-enabled/*;
}
```

## Server Blocks (Virtual Hosts)

Server blocks define how Nginx handles requests for specific domains or IP addresses:

```nginx
server {
    listen 80;
    server_name example.com www.example.com;

    root /var/www/example.com;
    index index.html index.htm;

    location / {
        try_files $uri $uri/ =404;
    }
}
```

## Reverse Proxy Configuration

Use Nginx to forward requests to an application server running on localhost:

```nginx
upstream app_backend {
    server 127.0.0.1:8000;
    server 127.0.0.1:8001;
}

server {
    listen 80;
    server_name app.example.com;

    location / {
        proxy_pass http://app_backend;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
```

## Common Location Patterns

```nginx
# Exact match
location = /path {
    # Only matches /path
}

# Prefix match (case-insensitive)
location /api {
    # Matches /api, /api/, /api/users, etc.
}

# Regular expression match
location ~ \.(jpg|jpeg|png|gif)$ {
    # Matches image files
}

# Case-insensitive regex
location ~* \.php$ {
    # Matches .php files (case-insensitive)
}
```

## Static File Caching

Tell browsers to cache static files:

```nginx
server {
    listen 80;
    server_name example.com;

    location ~* \.(jpg|jpeg|png|gif|ico|css|js)$ {
        expires 30d;
        add_header Cache-Control "public, immutable";
    }

    location / {
        expires -1;
        add_header Cache-Control "no-cache, no-store, must-revalidate";
    }
}
```

## HTTPS with SSL/TLS

To enable HTTPS, use SSL certificates (e.g., from Let's Encrypt):

```nginx
server {
    listen 443 ssl http2;
    server_name example.com;

    ssl_certificate /etc/letsencrypt/live/example.com/fullchain.pem;
    ssl_certificate_key /etc/letsencrypt/live/example.com/privkey.pem;

    ssl_protocols TLSv1.2 TLSv1.3;
    ssl_ciphers HIGH:!aNULL:!MD5;

    location / {
        proxy_pass http://app_backend;
    }
}

# Redirect HTTP to HTTPS
server {
    listen 80;
    server_name example.com;
    return 301 https://$server_name$request_uri;
}
```

## Testing Configuration

Before reloading, test your configuration for errors:

```bash
sudo nginx -t
```

Then reload the configuration without restarting:

```bash
sudo systemctl reload nginx
```

## Useful Commands

```bash
# Check if Nginx is running
sudo systemctl status nginx

# Stop Nginx
sudo systemctl stop nginx

# Start Nginx
sudo systemctl start nginx

# Reload configuration
sudo systemctl reload nginx

# View logs
sudo tail -f /var/log/nginx/access.log
sudo tail -f /var/log/nginx/error.log
```
