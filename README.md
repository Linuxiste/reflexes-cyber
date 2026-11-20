# Réflexes cyber : « 2 minutes par jour pour tes réflexes cyber »

Kit **libre et gratuit** de sensibilisation à la cybersécurité, pour les associations et les petites structures :

- **des modules de 2 minutes** en forme de conversation : un personnage, Lou, dialogue avec l'utilisateur, et la suite change selon ses réponses. Chaque module compte 6 à 10 messages et fait passer un seul réflexe ;
- **des pages d'entraînement au phishing** (« ⚠️ Tu t'es fait prendre… mais rien de grave »), pour des campagnes internes bienveillantes ;
- **une personnalisation par structure** (contacts, réseaux Wi-Fi, métiers, modules propres) qui reste privée ;
- **un site statique** dans un conteneur nginx : aucun compte, aucun cookie, aucune donnée collectée, et un journal sans adresse IP.

## Voir le site sur ton PC (sans VM ni Docker)

Il te faut seulement Python 3, déjà présent sur Debian. Rien n'est installé et rien ne tourne en arrière-plan.

```sh
cd reflexes-cyber        # le dossier du dépôt
./apercu.sh              # contrôle les modules, construit le site, puis lance le serveur
```

Ouvre ensuite **http://localhost:8000/** dans ton navigateur. Pour arrêter, fais **Ctrl + C** dans le terminal.

- Après une modification d'un module, arrête avec Ctrl + C et relance `./apercu.sh` : le site est reconstruit.
- Un autre port : `./apercu.sh exemple 8080`.
- Une autre structure : `./apercu.sh ma-structure`, avec son dossier `organisations/ma-structure/`.
- Pour le voir depuis un téléphone du même réseau : `./apercu.sh exemple 8000 reseau`. Le script affiche l'adresse à taper sur le téléphone.

Si un module ne respecte pas les règles, `./apercu.sh` s'arrête et indique lequel et pourquoi.

## Tester une campagne de phishing en local

Il faut **deux terminaux**, ouverts dans le dossier du dépôt.

**Terminal 1 : le site**, qui reste ouvert pendant tout le test.
```sh
./apercu.sh
```

**Terminal 2 : les faux messages et la vérification des liens.**
```sh
python3 outils/kit_campagne.py --organisation exemple --adresse http://localhost:8000
```

Le terminal 2 affiche une ligne par faux message, avec OK ou ÉCHEC. Ouvre ensuite le dossier `dist/kit-exemple/` :

| Fichier | À quoi il sert |
|---|---|
| `apercu.html` | Une boîte de réception de test. Ouvre-la dans le navigateur et clique sur chaque bouton : tu dois arriver sur « Tu t'es fait prendre… ». |
| `*.eml` | Les 4 faux mails. Double-clique dessus : ils s'ouvrent dans Thunderbird comme de vrais mails. |
| `sms-colis.txt` | Le texte du faux SMS. |
| `qr-qr-code.png` | Le QR code. Il n'apparaît que si `qrencode` est installé (`sudo apt install qrencode`). |
| `verification.txt` | Le résultat du contrôle : l'adresse visée par chaque lien et la réponse du serveur. |

**Pour le SMS et le QR code**, teste depuis un téléphone. Sur le téléphone, `localhost` désigne le téléphone lui-même :
```sh
./apercu.sh exemple 8000 reseau                                                      # terminal 1
python3 outils/kit_campagne.py --organisation exemple --adresse http://<IP-du-PC>:8000   # terminal 2
```

Le dossier `dist/kit-…` n'est jamais publié sur le site.

## Installer pour de vrai (serveur ou VM)

```sh
ORGANISATION=exemple docker compose up -d --build     # serveur nginx durci, sur le port 8080
sh deploiement/installer_vm.sh <url-du-dépôt> <organisation>   # VM Debian 12 ou 13 neuve, clé en main
```

## Version publique sur Linuxiste

La version publique est sur **https://linuxiste.fr/reflexes/**, avec des textes génériques (`organisations/linuxiste/`).

```sh
sh deploiement/deployer_linuxiste.sh            # construit, envoie une nouvelle version et bascule dessus
sh deploiement/deployer_linuxiste.sh --retour   # revient à la version précédente
```

Sur la VM, Apache sert `/var/www/reflexes-cyber/current` via `deploiement/apache-reflexes.conf`. Seule cette partie reçoit des en-têtes de sécurité stricts (CSP, nosniff, DENY). Le script garde les 5 dernières versions.

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

Tous les modules suivent les recommandations de l'ANSSI ([guides](https://messervices.cyber.gouv.fr/guides), [fiches pratiques ReCyF](https://messervices.cyber.gouv.fr/guides/fiches-pratiques-recyf)) et des services publics qui les relaient (Cybermalveillance.gouv.fr, CNIL, 17Cyber, 33700). La source exacte est toujours citée à la fin du module, et le site renvoie vers la documentation de l'ANSSI sur l'accueil, à la fin de chaque module et sur les pages d'entraînement.
