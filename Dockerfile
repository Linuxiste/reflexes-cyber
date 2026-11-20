# Étape 1 : contrôle des modules et construction du site pour une structure.
FROM python:3.12-alpine AS construction
ARG ORGANISATION=exemple
WORKDIR /src
COPY . .
RUN python3 -I outils/construire.py --organisation "$ORGANISATION"

# Étape 2 : serveur web minimal, sans droits root.
FROM nginxinc/nginx-unprivileged:1.27-alpine
ARG ORGANISATION=exemple
COPY deploiement/nginx.conf /etc/nginx/conf.d/default.conf
COPY --from=construction /src/dist/${ORGANISATION}/ /usr/share/nginx/html/
EXPOSE 8080
