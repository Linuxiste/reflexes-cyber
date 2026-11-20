#!/bin/sh
# Installe « Réflexes cyber » sur une VM Debian 12 ou 13 neuve (1 vCPU, 1 Go de RAM, 10 Go de disque suffisent).
# Usage, en root sur la VM :  sh installer_vm.sh <url-du-dépôt-git> [organisation]
# L'organisation privée (ex. fondation-cognacq-jay) se copie à part dans organisations/ AVANT de lancer la construction.
set -eu
DEPOT="${1:?usage : sh installer_vm.sh <url-du-depot-git> [organisation]}"
ORG="${2:-exemple}"
apt-get update -q
apt-get install -y -q ca-certificates curl git docker.io docker-compose unattended-upgrades
systemctl enable --now docker
[ -d /opt/reflexes-cyber ] || git clone "$DEPOT" /opt/reflexes-cyber
cd /opt/reflexes-cyber
if [ ! -f "organisations/$ORG/config.json" ]; then
    echo "organisations/$ORG/config.json introuvable : copie d'abord le dossier privé de la structure." >&2
    exit 1
fi
ORGANISATION="$ORG" docker-compose up -d --build
echo "Site disponible sur http://$(hostname -I | awk '{print $1}'):8080/"
echo "Visites par page (bilan anonyme) : docker logs reflexes-cyber 2>/dev/null | awk '{print \$3}' | sort | uniq -c | sort -rn"
