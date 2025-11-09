LocalCloud - Containerized File Upload Service (localhost)

Prerequisites:
- Docker & docker-compose installed
- 4GB free disk, internet to pull images

Run:
1. From project root:
   docker-compose up --build

2. Open browser to: http://localhost

Files uploaded are persisted in a Docker volume named 'LocalCloud_uploads_data' (inspect with 'docker volume ls' and 'docker volume inspect').

Stop:
  docker-compose down

To list logs:
  docker-compose logs -f

To see resource usage (on host):
  docker stats

To remove volumes:
  docker-compose down -v
