# Réflexes cyber : « 2 minutes par jour pour tes réflexes cyber »

Kit **libre et gratuit** de sensibilisation à la cybersécurité, pour les associations et les petites structures :

- **des modules de 2 minutes** en forme de conversation : un personnage, Lou, dialogue avec l'utilisateur, et la suite change selon ses réponses. Chaque module compte 6 à 10 messages et fait passer un seul réflexe ;
- **des pages d'entraînement au phishing** (« ⚠️ Tu t'es fait prendre… mais rien de grave »), pour des campagnes internes bienveillantes ;
- **une personnalisation par structure** (contacts, réseaux Wi-Fi, métiers, modules propres) qui reste privée ;
- **un site statique** dans un conteneur nginx : aucun compte, aucun cookie, aucune donnée collectée, et un journal sans adresse IP.

## Démarrer

```sh
python3 outils/construire.py --organisation exemple --verifier   # contrôle des modules
python3 outils/construire.py --organisation exemple              # → dist/exemple/ et dist/reflexes-exemple.sqlite
python3 -m http.server -d dist/exemple 8000                      # aperçu sur http://localhost:8000/
ORGANISATION=exemple docker compose up -d --build                # serveur sur le port 8080
```

VM clé en main (Debian 12 ou 13) : `sh deploiement/installer_vm.sh <url-du-dépôt> <organisation>`.

## Tester une campagne en local

```sh
python3 outils/construire.py --organisation exemple
python3 -m http.server -d dist/exemple 8000          # terminal 1 : le site
python3 outils/kit_campagne.py --organisation exemple --adresse http://localhost:8000   # terminal 2
```

`dist/kit-exemple/` contient alors (ce dossier n'est jamais publié sur le site) :
- `apercu.html`, une boîte de réception de test avec les 6 faux messages et leurs liens ;
- `*.eml`, de vrais mails à ouvrir dans Thunderbird ;
- `sms-colis.txt`, le texte du faux SMS ;
- `qr-qr-code.png`, le QR code, si `qrencode` est installé ;
- `verification.txt`, qui indique pour chaque lien l'adresse visée et la réponse du serveur.

L'outil échoue si un lien ne mène pas à une page « Tu t'es fait prendre ».

**Depuis un téléphone** (SMS, QR code), `localhost` désigne le téléphone lui-même, pas ton PC. Utilise l'adresse de ton PC sur le réseau local, par exemple `--adresse http://192.168.20.15:8000`, avec `python3 -m http.server -d dist/exemple 8000 --bind 0.0.0.0`.

## Organisation du dépôt

| Dossier | Contenu |
|---|---|
| `modules/<rubrique>/` | modules communs (JSON), relus avant publication (`statut` : brouillon → relu → publié) |
| `scenarios/` | pages d'entraînement au phishing, chacune liée à un module |
| `metiers.json` | les métiers proposés, et les modules prioritaires pour chacun |
| `organisations/exemple/` | personnalisation d'exemple (fictive) ; **les autres structures restent hors du dépôt** |
| `site/` | moteur de conversation et pages (HTML, CSS, JS sans dépendance) |
| `outils/construire.py` | contrôle des modules, personnalisation, construction du site et de la base SQLite |
| `docs/kit-relais/` | modèles de faux messages et accord à signer avant une campagne |
| `docs/personnaliser/` | questions à poser à l'administrateur système pour écrire les modules propres à la structure |
| `deploiement/` | configuration nginx durcie, installation sur une VM |

## Règles d'un module

Elles sont contrôlées automatiquement par `construire.py` :
- 6 à 10 messages et au plus 280 mots sur le parcours le plus long, soit environ 2 minutes ;
- une source https citée et un réflexe final en une phrase ;
- toutes les étapes atteignables, sans boucle ;
- des variables `{{org.…}}` toutes définies.

**Ton :** bienveillant, jamais culpabilisant. Une mauvaise réponse mène à une explication.

## Licences

- Textes, modules et images : **CC BY-SA 4.0** (https://creativecommons.org/licenses/by-sa/4.0/deed.fr).
- Code : **MIT** (voir `LICENCE`).

Les modules s'appuient sur les publications publiques de l'ANSSI, de Cybermalveillance.gouv.fr et du ReCyF, toujours citées en source.
