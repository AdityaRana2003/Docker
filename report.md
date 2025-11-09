# LocalCloud: Containerized File Upload Service

## Abstract
This mini project demonstrates container-based virtualization using Docker. LocalCloud is a simple web application for file upload, packaged as a container and deployed using docker-compose. It highlights service composition, persistence, reverse proxying and resource constraints.

## Tools & Technologies
- Docker, Docker Compose
- Flask (Python)
- Gunicorn (WSGI)
- Nginx (reverse proxy)

## Design
- `web` service: Flask app served by Gunicorn
- `nginx` service: reverse proxy, exposes port 80
- persistent storage via `uploads_data` docker volume

## Implementation Steps
1. Build image: `docker-compose up --build`
2. Access UI at `http://localhost`
3. Upload files (allowed: txt, pdf, png, jpg, jpeg, gif, zip)
4. Monitor containers via `docker ps`, `docker logs`, `docker stats`

## Results
- Successful uploads persisted across container restarts.
- Nginx served as reverse proxy to web service.
- Demonstrated container lifecycle commands.

## Advantages
- Lightweight, fast startups
- Portable environment on localhost
- Clear demonstration of virtualization concepts for labs

## Limitations & Future Work
- Authentication missing (add JWT or sessions)
- Add cAdvisor/Prometheus + Grafana for monitoring metrics
- Introduce scaling (swarm/k8s) for orchestration demonstration
