# fbmessenger-django
FBmessenger chatter on django on docker with Traefik as reverse proxy
The container will listen on port 8000 on internal network on Traefik network

The use of traefik, will help automatically bind the container to a DNS and HTTPS certificates with letsencrypt is done automatically

# Requirements
  - Docker
  - Docker-compose
  - Facebook Access Tokens
  - Traefik (not necessary if you have other reverse proxy)

# Installation guide
 - Clone repository
 - cd fbmessenger-django/codes/fb_kushalrover
 - Add the page tokens on the file views.py (parameter API_PAGE_FB)
 - cd fbmessenger-django
 - if you are using traefik, modify the docker-compose.yml file for HOST url of your DNS.
 - docker-compose up -d (to run container in detached mode)
 - docker logs -f <ID Container>  to check log
 - The container will listen on port 8000

