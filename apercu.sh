#!/bin/sh
# Aperçu local du site, sans VM ni Docker : contrôle et construit les modules, puis lance un petit serveur web.
# Usage, depuis le dossier du dépôt :  ./apercu.sh [organisation] [port]
#   ./apercu.sh                     → http://localhost:8000/ (organisation « exemple »)
#   ./apercu.sh exemple 8000 reseau → aussi visible depuis un téléphone du même réseau
# Arrêt : Ctrl + C. Rien n'est installé ; le site construit est dans dist/<organisation>/.
set -eu
cd "$(dirname "$0")"
ORG="${1:-exemple}"
PORT="${2:-8000}"
LIER=127.0.0.1
[ "${3:-}" = "reseau" ] && LIER=0.0.0.0
python3 -I outils/construire.py --organisation "$ORG" | tail -2
echo
echo "Site : http://localhost:$PORT/"
echo "Pages d'entraînement : http://localhost:$PORT/entrainement/lien/ (et urgence, piece-jointe, colis, virement, qr-code)"
if [ "$LIER" = 0.0.0.0 ]; then
    IP=$(hostname -I 2>/dev/null | awk '{print $1}')
    echo "Depuis un téléphone du même réseau : http://$IP:$PORT/"
fi
echo "Arrêt : Ctrl + C"
echo
exec python3 -m http.server -d "dist/$ORG" -b "$LIER" "$PORT"
