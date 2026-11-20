#!/bin/sh
# Déploie Réflexes cyber sur https://linuxiste.fr/reflexes/ (VM Linuxiste, Apache).
# Usage, depuis le dossier du dépôt :  sh deploiement/deployer_linuxiste.sh
# - contrôle et construit la version « linuxiste » (textes génériques) ;
# - copie le site dans une nouvelle version, puis bascule « current » (retour arrière : sh deploiement/deployer_linuxiste.sh --retour) ;
# - garde les 5 dernières versions.
set -eu
cd "$(dirname "$0")/.."
VM="${VM:-vlib@192.168.60.20}"
RACINE=/var/www/reflexes-cyber
SSH="ssh -o BatchMode=yes -o ConnectTimeout=10"

if [ "${1:-}" = "--retour" ]; then
    $SSH "$VM" "cd $RACINE/releases && P=\$(ls -1 | sort | tail -2 | head -1) && sudo ln -sfn $RACINE/releases/\$P $RACINE/current.tmp && sudo mv -T $RACINE/current.tmp $RACINE/current && echo \"retour à la version \$P\""
    exit 0
fi

python3 -I outils/construire.py --organisation linuxiste | tail -2
VERSION=$(date +%Y%m%d-%H%M%S)
TMP=/tmp/reflexes-$VERSION
$SSH "$VM" "mkdir -p $TMP" && tar -C dist/linuxiste -cf - . | $SSH "$VM" "tar -C $TMP -xf -"
$SSH "$VM" "set -e
  sudo mkdir -p $RACINE/releases
  sudo mv $TMP $RACINE/releases/$VERSION
  sudo chown -R root:root $RACINE/releases/$VERSION
  sudo find $RACINE/releases/$VERSION -type d -exec chmod 755 {} +
  sudo find $RACINE/releases/$VERSION -type f -exec chmod 644 {} +
  sudo ln -sfn $RACINE/releases/$VERSION $RACINE/current.tmp
  sudo mv -T $RACINE/current.tmp $RACINE/current
  cd $RACINE/releases && ls -1 | sort | head -n -5 | xargs -r sudo rm -rf
  echo \"version active : \$(readlink $RACINE/current)\""
