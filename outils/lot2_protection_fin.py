#!/usr/bin/env python3
"""Lot 2, partie 2 (rubrique Protection) : 9 modules JSON dans modules/protection/.

Thèmes : mises à jour, poste et appareils, Wi-Fi et déplacements.
Ne réécrit pas un module dont le statut n'est plus « brouillon » (déjà relu).
"""
import json
from pathlib import Path

MAJ = {"nom": "Cybermalveillance.gouv.fr, les mises à jour",
       "url": "https://www.cybermalveillance.gouv.fr/tous-nos-contenus/bonnes-pratiques/mises-a-jour"}
DUR = {"nom": "ANSSI, ReCyF en pratique : Durcissement et sécurité des équipements (v1.0, septembre 2026)",
       "url": "https://messervices.cyber.gouv.fr/documents-guides/Fiche_Durcissement-securitee_VF.pdf"}
NOM = {"nom": "ANSSI, recommandations sur le nomadisme numérique",
       "url": "https://cyber.gouv.fr/publications/recommandations-sur-le-nomadisme-numerique"}


def ch(*paires):
    return [{"txt": t, "va": v} for t, v in paires]


M = {}

# ---------------------------------------------------------------- Mises à jour
M["pro-maj-1"] = dict(theme="Mises à jour", titre="« Rappelez-moi plus tard »", source=MAJ, prio=["benevoles"],
    reflexe="Je fais les mises à jour dès qu'elles sont proposées, sur l'ordinateur comme sur le téléphone. Elles bouchent des trous déjà connus des pirates.",
    etapes={
    "debut": {"msg": "Salut, c'est {{perso}} ! Ton ordinateur affiche « Mises à jour disponibles ». Tu cliques sur quoi, d'habitude ?",
              "choix": ch(("« Rappelez-moi plus tard »", "plus_tard"), ("« Installer maintenant »", "maintenant"))},
    "plus_tard": {"msg": "Tu n'es pas le seul ! Ça tombe toujours au mauvais moment. Mais regarde ce qu'il y a dedans…", "va": "trou"},
    "maintenant": {"msg": "Bravo ! Tu sais ce qu'elles contiennent ?",
                   "choix": ch(("Des nouveautés", "trou"), ("Des corrections de sécurité", "trou"))},
    "trou": {"msg": "Souvent, une mise à jour bouche une faille, un trou dans le logiciel. Et dès qu'elle est publiée, les pirates savent que le trou existe.", "va": "course"},
    "course": {"msg": "C'est une course : ils cherchent les ordinateurs qui n'ont pas encore fait la mise à jour. Chaque jour de retard laisse la porte ouverte.", "va": "astuce"},
    "astuce": {"msg": "L'astuce : lance les mises à jour avant de partir déjeuner ou le soir. Et active les mises à jour automatiques quand c'est possible.", "va": "fin"},
    "fin": {"msg": "Mise à jour proposée, mise à jour installée. Sur le téléphone aussi ! À demain ! 👋", "fin": True}})

M["pro-maj-2"] = dict(theme="Mises à jour", titre="Le vieil ordinateur du bureau", source=MAJ, prio=["direction", "benevoles"],
    reflexe="Un appareil qui ne reçoit plus de mises à jour de sécurité n'est plus protégé. Je le signale pour qu'il soit remplacé ou isolé.",
    etapes={
    "debut": {"msg": "Dans un coin du bureau, un vieil ordinateur sert encore à imprimer. Il affiche « Windows 7 ». Ça te pose un souci ?",
              "choix": ch(("Non, il marche très bien", "marche"), ("Oui, il est vieux", "vieux"))},
    "marche": {"msg": "Il marche, oui ! Mais son système ne reçoit plus aucune mise à jour de sécurité depuis des années.", "va": "fin_support"},
    "vieux": {"msg": "Ce n'est pas son âge le souci, c'est autre chose…", "va": "fin_support"},
    "fin_support": {"msg": "Quand un éditeur arrête les mises à jour, chaque nouvelle faille découverte reste ouverte pour toujours. C'est pareil pour Windows 10 depuis octobre 2025.", "va": "reseau"},
    "reseau": {"msg": "Et cet ordinateur est branché sur le même réseau que les autres : il peut servir de porte d'entrée vers tout le bureau.", "va": "geste"},
    "geste": {"msg": "Pas de panique, et pas de reproche : signale-le à {{org.contact}}. On peut le remplacer, le débrancher du réseau, ou lui installer un système encore suivi.", "va": "fin"},
    "fin": {"msg": "Un appareil sans mises à jour, je le signale. Même s'il « marche très bien ». À demain ! 👋", "fin": True}})

M["pro-maj-3"] = dict(theme="Mises à jour", titre="Quiz : vraie ou fausse mise à jour ?", source=MAJ, prio=[],
    reflexe="Les vraies mises à jour passent par les réglages de l'appareil ou par l'application elle-même, jamais par une fenêtre surgie d'un site web.",
    etapes={
    "debut": {"msg": "Quiz ! Sur un site, une fenêtre surgit : « Votre lecteur vidéo est obsolète, mettez-le à jour ici ». Tu cliques ?",
              "choix": ch(("Oui, c'est une mise à jour", "q1non"), ("Non, c'est louche", "q1oui"))},
    "q1non": {"msg": "C'est un piège classique : une fausse mise à jour qui installe un logiciel malveillant.", "va": "q2"},
    "q1oui": {"msg": "Bien vu ! Une vraie mise à jour ne vient pas d'un site au hasard.", "va": "q2"},
    "q2": {"msg": "Question 2 : où trouve-t-on les vraies mises à jour ?",
           "choix": ch(("Dans les réglages de l'appareil", "q2oui"), ("Dans un mail qui me l'annonce", "q2non"))},
    "q2oui": {"msg": "Exact : dans les réglages, ou dans le menu de l'application.", "va": "q3"},
    "q2non": {"msg": "Un mail avec un lien « mettez à jour ici » est souvent un piège. Les vraies passent par les réglages ou par l'application.", "va": "q3"},
    "q3": {"msg": "Dernière : les applications du téléphone aussi ont besoin de mises à jour ?",
           "choix": ch(("Oui", "fin"), ("Non, seulement l'ordinateur", "tel"))},
    "tel": {"msg": "Le téléphone aussi ! Il contient tes mails, tes codes et ta banque. Active les mises à jour automatiques dans le magasin d'applications.", "va": "fin"},
    "fin": {"msg": "Les vraies mises à jour passent par les réglages. Bravo ! 👋", "fin": True}})

# ---------------------------------------------------------------- Poste et appareils
M["pro-poste-1"] = dict(theme="Poste et appareils", titre="Le café et l'écran ouvert", source=DUR, prio=["accueil", "soin", "educatif"],
    reflexe="Quand je quitte mon poste, même deux minutes, je verrouille l'écran : touches Windows + L, ou Ctrl + Cmd + Q sur Mac.",
    etapes={
    "debut": {"msg": "Tu pars chercher un café. Ton ordinateur reste allumé, ta messagerie ouverte. Ça ne craint rien, si ?",
              "choix": ch(("Non, c'est deux minutes", "deux"), ("Je verrouille toujours", "verrouille"))},
    "deux": {"msg": "Deux minutes, c'est assez pour lire un dossier, envoyer un mail en ton nom ou brancher une clé. Pas besoin d'être un pirate : un visiteur curieux suffit.", "va": "public"},
    "verrouille": {"msg": "Excellent réflexe ! Tu connais le raccourci le plus rapide ?",
                   "choix": ch(("Oui", "raccourci"), ("Pas vraiment", "raccourci"))},
    "public": {"msg": "C'est encore plus vrai à l'accueil, ou quand des jeunes, des patients ou des visiteurs passent près de ton bureau.", "va": "raccourci"},
    "raccourci": {"msg": "Le raccourci magique : touche Windows + L. Sur Mac : Ctrl + Cmd + Q. Une seconde, et l'écran est verrouillé.", "va": "auto"},
    "auto": {"msg": "En plus, demande à {{org.contact}} que l'écran se verrouille tout seul après quelques minutes. C'est un filet de sécurité en cas d'oubli.", "va": "fin"},
    "fin": {"msg": "Je me lève, je verrouille. Windows + L devient un réflexe. À demain ! 👋", "fin": True}})

M["pro-poste-2"] = dict(theme="Poste et appareils", titre="La clé USB trouvée sur le parking", source=DUR, prio=["accueil"],
    reflexe="Je ne branche jamais une clé USB trouvée ou inconnue. Je la remets à {{org.contact}}, sans la tester « juste pour voir ».",
    etapes={
    "debut": {"msg": "Sur le parking, tu trouves une clé USB marquée « Salaires 2026 ». Tu fais quoi ?",
              "choix": ch(("Je la branche pour trouver le propriétaire", "branche"), ("Je ne la branche pas", "branche_pas"))},
    "branche": {"msg": "C'est gentil de vouloir la rendre ! Mais c'est exactement le piège : l'étiquette est faite pour te donner envie de la brancher.", "va": "piege"},
    "branche_pas": {"msg": "Parfait ! Et tu sais pourquoi c'est risqué ?",
                    "choix": ch(("Elle peut contenir un virus", "piege"), ("Pas vraiment", "piege"))},
    "piege": {"msg": "Une clé piégée peut installer un logiciel malveillant dès qu'on la branche. Certaines se font même passer pour un clavier et tapent des commandes toutes seules.", "va": "tous"},
    "tous": {"msg": "C'est valable aussi pour une clé offerte dans un salon, ou un câble de recharge inconnu.", "va": "geste"},
    "geste": {"msg": "Le bon geste : la remettre à {{org.contact}}, sans la tester. Et pour échanger des fichiers, préfère un partage fourni par {{org.nom_court}}.", "va": "fin"},
    "fin": {"msg": "Clé inconnue, je ne branche pas. Même si l'étiquette donne très envie ! À demain ! 👋", "fin": True}})

M["pro-poste-3"] = dict(theme="Poste et appareils", titre="Quiz : mon poste, ma forteresse", source=DUR, prio=[],
    reflexe="Écran verrouillé quand je pars, aucune clé inconnue, et un appareil perdu ou volé signalé tout de suite.",
    etapes={
    "debut": {"msg": "Quiz ! Le raccourci pour verrouiller l'écran sous Windows, c'est…",
              "choix": ch(("Windows + L", "q1oui"), ("Ctrl + Alt + C", "q1non"))},
    "q1oui": {"msg": "Bravo ! L comme « Lock », verrouiller en anglais.", "va": "q2"},
    "q1non": {"msg": "C'est Windows + L. L comme « Lock », verrouiller en anglais.", "va": "q2"},
    "q2": {"msg": "Question 2 : ton téléphone professionnel disparaît dans le train. Tu préviens quand ?",
           "choix": ch(("Tout de suite", "q2oui"), ("Après l'avoir cherché une semaine", "q2non"))},
    "q2oui": {"msg": "Oui : on peut alors le bloquer ou l'effacer à distance.", "va": "q3"},
    "q2non": {"msg": "Préviens tout de suite {{org.contact}} : on peut le bloquer ou l'effacer à distance avant que quelqu'un s'en serve.", "va": "q3"},
    "q3": {"msg": "Dernière : un collègue te prête une clé USB qu'il utilise chez lui. Tu la branches ?",
           "choix": ch(("Je préfère un partage de fichiers", "fin"), ("Oui, c'est un collègue", "collegue"))},
    "collegue": {"msg": "Il est de bonne foi, mais son ordinateur personnel peut être infecté sans qu'il le sache. Un partage de fichiers est plus sûr.", "va": "fin"},
    "fin": {"msg": "Écran verrouillé, clés inconnues écartées, perte signalée vite. Bravo ! 👋", "fin": True}})

# ---------------------------------------------------------------- Wi-Fi et déplacements
M["pro-wifi-1"] = dict(theme="Wi-Fi et déplacements", titre="Le Wi-Fi gratuit de la gare", source=NOM, prio=["direction", "soin"],
    reflexe="Sur un Wi-Fi public, j'évite les comptes sensibles. Je préfère le partage de connexion de mon téléphone, ou le VPN fourni par {{org.nom_court}}.",
    etapes={
    "debut": {"msg": "Tu attends ton train. Un réseau « Gare_WiFi_Gratuit » est disponible. Tu t'y connectes pour finir un dossier de travail ?",
              "choix": ch(("Oui, c'est gratuit", "oui"), ("J'hésite", "hesite"))},
    "oui": {"msg": "C'est tentant ! Mais n'importe qui peut créer un réseau qui s'appelle « Gare_WiFi_Gratuit », avec son propre ordinateur.", "va": "faux"},
    "hesite": {"msg": "Tu as raison d'hésiter. Voilà pourquoi.", "va": "faux"},
    "faux": {"msg": "Sur un faux réseau, ou sur un vrai réseau mal protégé, quelqu'un peut observer ce qui passe, ou te présenter une fausse page de connexion.", "va": "alternative"},
    "alternative": {"msg": "La solution la plus simple : le partage de connexion de ton téléphone. C'est ton propre réseau, protégé par ton mot de passe.", "va": "vpn"},
    "vpn": {"msg": "Si {{org.nom_court}} fournit un VPN, active-le : il crée un tunnel chiffré jusqu'au bureau, même sur un Wi-Fi douteux.", "va": "fin"},
    "fin": {"msg": "Wi-Fi public : pas de compte sensible. Partage de connexion ou VPN. Bon voyage ! 👋", "fin": True}})

M["pro-wifi-2"] = dict(theme="Wi-Fi et déplacements", titre="Mise en situation : le train et le voisin", source=NOM, prio=["direction", "soin", "rh"],
    reflexe="En déplacement, je garde mon matériel avec moi, je protège mon écran des regards, et je ne parle pas de sujets confidentiels au téléphone en public.",
    etapes={
    "debut": {"msg": "Dans le train, tu ouvres un dossier sur une personne accompagnée. Ton voisin a une vue parfaite sur ton écran. Tu continues ?",
              "choix": ch(("Il ne regarde pas", "regarde_pas"), ("Je change de place ou je ferme", "ferme"))},
    "regarde_pas": {"msg": "Peut-être ! Mais un regard suffit pour lire un nom, et une photo de ton écran se prend discrètement.", "va": "filtre"},
    "ferme": {"msg": "Très bon réflexe ! Les informations sur les personnes méritent cette discrétion.", "va": "filtre"},
    "filtre": {"msg": "Un filtre de confidentialité sur l'écran aide beaucoup : vu de côté, l'écran paraît noir. Demande-le à {{org.contact}}.", "va": "appel"},
    "appel": {"msg": "Le téléphone aussi : un appel sur un dossier sensible, dans un wagon, tout le monde l'entend.", "va": "pause"},
    "pause": {"msg": "Et si tu vas au wagon-bar, ton ordinateur vient avec toi, ou reste verrouillé et rangé. Il ne garde pas ta place tout seul !", "va": "fin"},
    "fin": {"msg": "En déplacement : écran discret, conversations discrètes, matériel sous la main. À demain ! 👋", "fin": True}})

M["pro-wifi-3"] = dict(theme="Wi-Fi et déplacements", titre="Quiz : en déplacement", source=NOM, prio=[],
    reflexe="Le partage de connexion de mon téléphone est plus sûr qu'un Wi-Fi public. Et un appareil perdu ou volé, je le signale tout de suite.",
    etapes={
    "debut": {"msg": "Quiz ! Le réseau le plus sûr pour travailler en déplacement, c'est…",
              "choix": ch(("Le partage de connexion de mon téléphone", "q1oui"), ("Le Wi-Fi de l'hôtel", "q1non"))},
    "q1oui": {"msg": "Exact : c'est ton propre réseau.", "va": "q2"},
    "q1non": {"msg": "Le Wi-Fi de l'hôtel est partagé avec tous les clients. Ton propre partage de connexion est plus sûr.", "va": "q2"},
    "q2": {"msg": "Question 2 : sur un Wi-Fi public, tu peux consulter…",
           "choix": ch(("Des infos et la météo", "q2oui"), ("Mon compte bancaire", "q2non"))},
    "q2oui": {"msg": "Oui, rien de sensible, aucun souci.", "va": "q3"},
    "q2non": {"msg": "Mieux vaut attendre d'être sur ton propre réseau pour la banque, ou passer par le réseau mobile.", "va": "q3"},
    "q3": {"msg": "Dernière : ton ordinateur de travail est volé dans ta voiture. Premier réflexe ?",
           "choix": ch(("Prévenir {{org.contact}} tout de suite", "fin"), ("Attendre la plainte", "attendre"))},
    "attendre": {"msg": "La plainte est importante, mais préviens d'abord {{org.contact}} : il faut fermer les accès avant qu'ils servent.", "va": "fin"},
    "fin": {"msg": "Bravo, tu as terminé la rubrique Protection ! 👋", "fin": True}})


def main():
    d = Path(__file__).resolve().parent.parent / "modules" / "protection"
    d.mkdir(parents=True, exist_ok=True)
    for mid, m in M.items():
        f = d / f"{mid}.json"
        if f.exists() and json.loads(f.read_text(encoding="utf-8")).get("statut") != "brouillon":
            print(f"  conservé (déjà relu) : {f.name}")
            continue
        doc = {"id": mid, "rubrique": "Protection", "theme": m["theme"], "titre": m["titre"], "reflexe": m["reflexe"],
               "source": m["source"], "metiers": ["tous"], "prioritaire_pour": m["prio"], "statut": "brouillon",
               "etapes": m["etapes"]}
        f.write_text(json.dumps(doc, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
    print(f"{len(M)} modules traités dans {d}")


if __name__ == "__main__":
    main()
