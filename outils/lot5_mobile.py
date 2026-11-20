#!/usr/bin/env python3
"""Lot 5 : rubrique Protection, thème « Téléphone mobile » (3 modules JSON).

Source : CERT-FR (ANSSI), CERTFR-2025-DUR-001, « 10 bonnes pratiques pour l'utilisation
des téléphones mobiles » (3 avril 2025). Les 10 règles sont couvertes :
  module 1 : règles 1 (mises à jour, redémarrage), 4 (applications, autorisations), 5 (sans-fil) ;
  module 2 : règles 3 (appareils et Wi-Fi inconnus), 6 (perso / pro), 7 (éteindre), 8 (réunions) ;
  module 3 : règles 9 (SMS / chiffrement), 10 (hameçonnage, association d'appareil), 2 (durcissement).

Ne réécrit pas un module dont le statut n'est plus « brouillon » (déjà relu).
"""
import json
from pathlib import Path

CERTFR = {"nom": "CERT-FR (ANSSI), 10 bonnes pratiques pour l'utilisation des téléphones mobiles (CERTFR-2025-DUR-001)",
          "url": "https://cert.cyber.gouv.fr/dur/CERTFR-2025-DUR-001/"}


def ch(*paires):
    return [{"txt": t, "va": v} for t, v in paires]


M = {}

M["pro-mobile-1"] = dict(theme="Téléphone mobile", titre="Un bureau dans ta poche", prio=["direction", "accueil", "benevoles"],
    reflexe="Je mets à jour mon téléphone et ses applications dès que possible, je le redémarre de temps en temps, je supprime les applications inutiles et je coupe Bluetooth, Wi-Fi et localisation quand je ne m'en sers pas.",
    etapes={
    "debut": {"msg": "Salut, c'est {{perso}} ! Ton téléphone contient tes mails, tes photos, tes codes… C'est un vrai bureau dans ta poche. Il est bien rangé ?",
              "choix": ch(("Je crois, oui", "oui"), ("Euh… pas sûr", "pas-sur"))},
    "oui": {"msg": "Parfait, on vérifie ensemble en trois points.", "va": "maj"},
    "pas-sur": {"msg": "Pas de souci, c'est le cas de presque tout le monde. Trois gestes suffisent.", "va": "maj"},
    "maj": {"msg": "1. Les mises à jour : installe-les dès qu'elles arrivent, système et applications. Elles bouchent des failles déjà connues des pirates.",
            "va": "redemarrer"},
    "redemarrer": {"msg": "Petit bonus de l'ANSSI : redémarre ton téléphone régulièrement. Certains logiciels espions ne survivent pas à un redémarrage.",
                   "va": "applis"},
    "applis": {"msg": "2. Les applications : celles que tu n'utilises plus, supprime-les. Et pour les autres, une lampe de poche n'a pas besoin de tes contacts !",
               "choix": ch(("Je vais faire le tri", "sansfil"), ("Comment je vérifie ?", "verifier"))},
    "verifier": {"msg": "Dans les réglages, cherche « Autorisations » ou « Confidentialité » : tu vois quelle application accède à quoi, et tu peux retirer l'accès.",
                 "va": "sansfil"},
    "sansfil": {"msg": "3. Bluetooth, Wi-Fi, NFC, localisation : quand tu ne t'en sers pas, coupe-les. Ce sont autant de portes ouvertes en moins.",
                "va": "fin"},
    "fin": {"msg": "À jour, trié, portes fermées : ton bureau de poche est rangé. Demain, on parle chargeurs et réunions. 👋", "fin": True}})

M["pro-mobile-2"] = dict(theme="Téléphone mobile", titre="Le chargeur trouvé sur la table", prio=["direction", "finances", "accueil"],
    reflexe="Je ne branche mon téléphone que sur mon chargeur ou une prise électrique, j'évite les Wi-Fi publics, je sépare le perso du pro, je l'éteins quand je le confie et je le laisse dehors pour les réunions sensibles.",
    etapes={
    "debut": {"msg": "Ta batterie est à 5 %. Sur la table de la salle d'attente, un câble USB est déjà branché. Tu fais quoi ?",
              "choix": ch(("Je branche, c'est pratique", "branche"), ("J'hésite…", "hesite"))},
    "branche": {"msg": "Tentant ! Mais un câble ou un port USB inconnu peut faire plus que charger : il peut aussi échanger des données avec ton téléphone.",
                "va": "regle"},
    "hesite": {"msg": "Bonne intuition : un câble ou un port USB inconnu peut faire plus que charger, il peut échanger des données.", "va": "regle"},
    "regle": {"msg": "La règle de l'ANSSI : ne jamais brancher ton téléphone sur un appareil inconnu (chargeur, clé, ordinateur), ni sur un Wi-Fi public. Ton propre chargeur sur une prise électrique, c'est parfait.",
              "va": "separer"},
    "separer": {"msg": "Autre bon réflexe : séparer le perso et le pro. Les jeux et applis perso d'un côté, les données de {{org.nom_court}} de l'autre.",
                "va": "eteindre"},
    "eteindre": {"msg": "Et quand tu dois te séparer de ton téléphone (contrôle, réparation, vestiaire), éteins-le complètement.",
                 "va": "reunion"},
    "reunion": {"msg": "Dernier point, pour les réunions sensibles : laisse les téléphones dehors. Le mode avion n'empêche pas un logiciel espion d'écouter.",
                "choix": ch(("Même le mode avion ?", "avion"), ("D'accord, c'est noté", "fin"))},
    "avion": {"msg": "Oui : le mode avion coupe le réseau, pas le micro. Un espion peut enregistrer et tout envoyer plus tard.", "va": "fin"},
    "fin": {"msg": "Ton chargeur, ta prise, ta séparation perso/pro, et pas de téléphone en réunion sensible. Demain : les messages. 👋", "fin": True}})

M["pro-mobile-3"] = dict(theme="Téléphone mobile", titre="« Relie ton compte à ce nouvel appareil »", prio=["direction", "rh", "soin"],
    reflexe="Les informations sensibles ne passent pas par SMS mais par une messagerie chiffrée de bout en bout. Je n'accepte jamais une demande de relier un nouvel appareil à mon compte sans l'avoir faite moi-même.",
    etapes={
    "debut": {"msg": "Tu dois envoyer les coordonnées bancaires d'un bénévole à un collègue. Tu utilises quoi ?",
              "choix": ch(("Un SMS, c'est rapide", "sms"), ("Une messagerie chiffrée", "chiffree"))},
    "sms": {"msg": "Rapide, oui, mais un SMS n'est pas chiffré de bout en bout : il peut être lu en chemin.", "va": "conseil"},
    "chiffree": {"msg": "Bien vu ! Le chiffrement de bout en bout garantit que seul ton destinataire peut lire le message.", "va": "conseil"},
    "conseil": {"msg": "Pour tout ce qui est sensible, l'ANSSI recommande une messagerie chiffrée de bout en bout plutôt que le SMS. Demande à {{org.contact}} laquelle utiliser dans {{org.nom_court}}.",
                "va": "piege"},
    "piege": {"msg": "Maintenant, un piège répandu : tu reçois « Scanne ce QR code pour vérifier ton compte » ou « Donne-moi le code que tu viens de recevoir ».",
              "choix": ch(("Je le fais, ça a l'air officiel", "piege-oui"), ("Je me méfie", "piege-non"))},
    "piege-oui": {"msg": "Ce message est très bien imité ! Mais souvent, ce code ou ce QR code relie le téléphone de l'escroc à ton compte : il lit alors tous tes messages.",
                  "va": "verifier"},
    "piege-non": {"msg": "Exactement : ce code ou ce QR code sert souvent à relier le téléphone de l'escroc à ton compte.", "va": "verifier"},
    "verifier": {"msg": "En cas de doute, vérifie l'origine par un autre moyen, et regarde dans les réglages la liste des « appareils connectés » à ton compte.",
                 "va": "alerte"},
    "alerte": {"msg": "Et si Apple, Google ou ta messagerie t'alerte d'une attaque ciblée, préviens tout de suite {{org.contact}}. Pour les personnes très exposées, l'ANSSI conseille d'activer le mode de protection renforcée du téléphone.",
               "va": "fin"},
    "fin": {"msg": "Sensible = messagerie chiffrée, et jamais de code ou de QR code pour un appareil que tu n'as pas ajouté toi-même. 👋", "fin": True}})


def main():
    d = Path(__file__).resolve().parent.parent / "modules" / "protection"
    for mid, m in M.items():
        f = d / f"{mid}.json"
        if f.exists() and json.loads(f.read_text(encoding="utf-8")).get("statut") != "brouillon":
            print(f"  conservé (déjà relu) : {f.name}")
            continue
        doc = {"id": mid, "rubrique": "Protection", "theme": m["theme"], "titre": m["titre"], "reflexe": m["reflexe"],
               "source": CERTFR, "metiers": ["tous"], "prioritaire_pour": m["prio"], "statut": "brouillon",
               "etapes": m["etapes"]}
        f.write_text(json.dumps(doc, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
    print(f"{len(M)} modules traités")


if __name__ == "__main__":
    main()
