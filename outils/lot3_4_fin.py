#!/usr/bin/env python3
"""Lots 3 et 4 : rubriques Résilience, Gouvernance et Obligations NIS 2 (24 modules JSON).

Ne réécrit pas un module dont le statut n'est plus « brouillon » (déjà relu).
Les modules NIS 2 portent une date de péremption : la loi de transposition était en cours
d'adoption en novembre 2026, il faut revérifier leur texte avant cette date.
"""
import json
from pathlib import Path

SAUV = {"nom": "Cybermalveillance.gouv.fr, les sauvegardes",
        "url": "https://www.cybermalveillance.gouv.fr/tous-nos-contenus/bonnes-pratiques/sauvegardes"}
RANCON = {"nom": "Cybermalveillance.gouv.fr, fiche réflexe Rançongiciels",
          "url": "https://www.cybermalveillance.gouv.fr/tous-nos-contenus/fiches-reflexes/rancongiciels-ransomwares"}
CRISE = {"nom": "ANSSI, organiser un exercice de gestion de crise cyber",
         "url": "https://cyber.gouv.fr/publications/organiser-un-exercice-de-gestion-de-crise-cyber"}
RGPD = {"nom": "CNIL, le RGPD : de quoi parle-t-on ?", "url": "https://www.cnil.fr/fr/rgpd-de-quoi-parle-t-on"}
DROITS = {"nom": "CNIL, les droits pour maîtriser vos données personnelles",
          "url": "https://www.cnil.fr/fr/les-droits-pour-maitriser-vos-donnees-personnelles"}
M10 = {"nom": "Cybermalveillance.gouv.fr, 10 mesures essentielles",
       "url": "https://www.cybermalveillance.gouv.fr/tous-nos-contenus/bonnes-pratiques/10-mesures-essentielles-assurer-securite-numerique"}
IA = {"nom": "CNIL, intelligence artificielle", "url": "https://www.cnil.fr/fr/intelligence-artificielle"}
NIS2 = {"nom": "ANSSI, la directive NIS 2", "url": "https://cyber.gouv.fr/la-directive-nis-2"}
ESPACE = {"nom": "ANSSI, MonEspaceNIS2", "url": "https://monespacenis2.cyber.gouv.fr/"}
PEREMPTION_NIS2 = "2027-05-20"


def ch(*paires):
    return [{"txt": t, "va": v} for t, v in paires]


M = {}

# ================================================================ RÉSILIENCE
# ---------------------------------------------------------------- Sauvegardes
M["res-sauv-1"] = dict(rub="Résilience", theme="Sauvegardes", titre="Et si ton ordinateur disparaissait ce soir ?", source=SAUV, prio=["benevoles", "direction"],
    reflexe="Mes documents importants existent en au moins deux endroits, dont un qui n'est pas branché en permanence. Une panne n'est alors qu'un mauvais moment.",
    etapes={
    "debut": {"msg": "Salut, c'est {{perso}} ! Imagine : ce soir, ton ordinateur tombe en panne pour de bon. Qu'est-ce que tu perds ?",
              "choix": ch(("Pas grand-chose, tout est sauvegardé", "rien"), ("Aïe… beaucoup de choses", "tout"))},
    "rien": {"msg": "Bravo ! Vérifions quand même que ta sauvegarde résisterait au pire.", "va": "pannes"},
    "tout": {"msg": "Tu n'es pas seul : c'est souvent après une panne qu'on pense aux sauvegardes. Faisons-le avant !", "va": "pannes"},
    "pannes": {"msg": "Un disque qui lâche, un ordinateur volé, un café renversé, un rançongiciel… Les causes sont nombreuses, et elles arrivent sans prévenir.", "va": "deux"},
    "deux": {"msg": "La règle de base : tes documents importants doivent exister en au moins deux endroits. Ton ordinateur, plus une sauvegarde.", "va": "debranche"},
    "debranche": {"msg": "Et une copie doit être débranchée ou hors ligne : un rançongiciel chiffre tout ce qui est branché, y compris le disque de sauvegarde.", "va": "fin"},
    "fin": {"msg": "Deux endroits, dont un débranché. Demain, la règle 3-2-1 en 2 minutes. 👋", "fin": True}})

M["res-sauv-2"] = dict(rub="Résilience", theme="Sauvegardes", titre="La règle 3-2-1", source=SAUV, prio=["direction", "finances"],
    reflexe="Règle 3-2-1 : 3 copies de mes données, sur 2 supports différents, dont 1 hors du bureau ou hors ligne. Et je teste la restauration de temps en temps.",
    etapes={
    "debut": {"msg": "Tu connais la règle 3-2-1 des sauvegardes ?",
              "choix": ch(("Oui", "oui"), ("Non, explique", "explique"))},
    "oui": {"msg": "Super, alors on vérifie ensemble !", "va": "trois"},
    "explique": {"msg": "C'est simple, promis. Trois chiffres.", "va": "trois"},
    "trois": {"msg": "3 copies de tes données : l'originale et deux sauvegardes.", "va": "deux"},
    "deux": {"msg": "2 supports différents : par exemple un disque externe et un service en ligne. Si l'un lâche, l'autre tient.", "va": "un"},
    "un": {"msg": "1 copie ailleurs : hors du bureau, ou hors ligne. En cas d'incendie, de vol ou de rançongiciel, elle reste intacte.", "va": "test"},
    "test": {"msg": "Et le secret que peu de gens connaissent : une sauvegarde qu'on n'a jamais essayé de restaurer n'est qu'un espoir. Teste de temps en temps.", "va": "fin"},
    "fin": {"msg": "3 copies, 2 supports, 1 ailleurs, et un test de temps en temps. Demande à {{org.contact}} comment c'est fait dans {{org.nom_court}}. 👋", "fin": True}})

M["res-sauv-3"] = dict(rub="Résilience", theme="Sauvegardes", titre="Quiz : sauvegarde ou pas ?", source=SAUV, prio=[],
    reflexe="Un document synchronisé n'est pas toujours sauvegardé : s'il est effacé ou chiffré, la synchronisation peut propager le problème. Une vraie sauvegarde garde l'historique.",
    etapes={
    "debut": {"msg": "Quiz ! Tes fichiers sont dans un dossier synchronisé sur Internet. C'est une sauvegarde ?",
              "choix": ch(("Oui, ils sont en ligne", "q1non"), ("Pas forcément", "q1oui"))},
    "q1oui": {"msg": "Bien vu ! Si tu effaces un fichier, la synchronisation l'efface aussi partout.", "va": "q2"},
    "q1non": {"msg": "Pas forcément : si un fichier est effacé ou chiffré, la synchronisation recopie le problème partout. Une sauvegarde garde les anciennes versions.", "va": "q2"},
    "q2": {"msg": "Question 2 : ton disque de sauvegarde reste branché en permanence à l'ordinateur. Risqué ?",
           "choix": ch(("Oui, en cas de rançongiciel", "q2oui"), ("Non, c'est pratique", "q2non"))},
    "q2oui": {"msg": "Exactement !", "va": "q3"},
    "q2non": {"msg": "Pratique, mais un rançongiciel le chiffrerait avec le reste. On le débranche après la sauvegarde.", "va": "q3"},
    "q3": {"msg": "Dernière : quand as-tu vérifié pour la dernière fois que tu savais restaurer un fichier ?",
           "choix": ch(("Récemment", "fin"), ("Jamais…", "jamais"))},
    "jamais": {"msg": "Pas de souci, c'est le cas de beaucoup de monde ! Essaie cette semaine avec un fichier sans importance.", "va": "fin"},
    "fin": {"msg": "Synchroniser n'est pas sauvegarder, et une sauvegarde se teste. Bravo ! 👋", "fin": True}})

# ---------------------------------------------------------------- Rançongiciel
M["res-rancon-1"] = dict(rub="Résilience", theme="Rançongiciel", titre="Le message qui réclame une rançon", source=RANCON, prio=["direction"],
    reflexe="Rançongiciel : je débranche le réseau, je ne paie pas, je ne touche plus à rien, et je préviens tout de suite.",
    etapes={
    "debut": {"msg": "Un rançongiciel, tu sais ce que c'est ?",
              "choix": ch(("Oui, un virus qui bloque tout", "oui"), ("Pas vraiment", "non"))},
    "oui": {"msg": "Exactement. Voyons comment il entre, et comment réagir.", "va": "quoi"},
    "non": {"msg": "C'est un logiciel malveillant qui rend tes fichiers illisibles, puis réclame de l'argent pour les « rendre ».", "va": "quoi"},
    "quoi": {"msg": "Il entre souvent par une pièce jointe piégée, un lien, un mot de passe volé ou un logiciel pas à jour. Tout ce qu'on a vu dans les autres modules !", "va": "cible"},
    "cible": {"msg": "Les petites structures sont très visées : elles ont moins de protections, et elles ont besoin de leurs fichiers pour fonctionner.", "va": "payer"},
    "payer": {"msg": "Faut-il payer ? Non. Rien ne garantit que les fichiers seront rendus, et ça finance de nouvelles attaques.", "va": "parade"},
    "parade": {"msg": "La meilleure parade, c'est une sauvegarde débranchée : avec elle, une attaque devient un mauvais moment, pas une catastrophe.", "va": "fin"},
    "fin": {"msg": "Débrancher, ne pas payer, prévenir. Et avoir une sauvegarde débranchée. À demain ! 👋", "fin": True}})

M["res-rancon-2"] = dict(rub="Résilience", theme="Rançongiciel", titre="Mise en situation : lundi, 8 h 30", source=RANCON, prio=["accueil", "direction"],
    reflexe="Si je vois des fichiers renommés ou un message de rançon : je débranche le câble ou je coupe le Wi-Fi, je laisse l'ordinateur allumé, et j'appelle {{org.contact}}.",
    etapes={
    "debut": {"msg": "Lundi, 8 h 30. Un collègue t'appelle : « Mes fichiers ont tous une extension bizarre, et un message demande des bitcoins ! » Tu lui dis quoi ?",
              "choix": ch(("« Éteins tout ! »", "eteins"), ("« Débranche le réseau ! »", "reseau"))},
    "eteins": {"msg": "Le réflexe est compréhensible, mais éteindre peut effacer des traces utiles pour comprendre l'attaque. On isole plutôt du réseau.", "va": "isoler"},
    "reseau": {"msg": "Exactement ! Le câble réseau, ou le Wi-Fi coupé.", "va": "isoler"},
    "isoler": {"msg": "Isoler l'ordinateur empêche le rançongiciel de se propager aux autres postes et au serveur. Chaque minute compte.", "va": "toucher"},
    "toucher": {"msg": "Ensuite, on ne touche plus à rien : pas de « nettoyage » maison, pas de redémarrage, pas de réponse aux escrocs.", "va": "prevenir"},
    "prevenir": {"msg": "On prévient tout de suite {{org.contact}}, {{org.contact_detail}}. Et 17Cyber.gouv.fr guide pas à pas.", "va": "fin"},
    "fin": {"msg": "Isoler, ne plus toucher, prévenir. Ton collègue a eu le bon réflexe en t'appelant tout de suite ! 👋", "fin": True}})

M["res-rancon-3"] = dict(rub="Résilience", theme="Rançongiciel", titre="Quiz : face au rançongiciel", source=RANCON, prio=[],
    reflexe="Les portes d'entrée d'un rançongiciel sont connues : pièces jointes, liens, mots de passe volés, logiciels pas à jour. Chaque bon réflexe en ferme une.",
    etapes={
    "debut": {"msg": "Quiz ! Quelle est la meilleure protection contre la perte de données par rançongiciel ?",
              "choix": ch(("Une sauvegarde débranchée", "q1oui"), ("Payer vite", "q1non"))},
    "q1oui": {"msg": "Oui ! Avec elle, on restaure et on repart.", "va": "q2"},
    "q1non": {"msg": "Payer ne garantit rien. Une sauvegarde débranchée, elle, permet de tout récupérer.", "va": "q2"},
    "q2": {"msg": "Question 2 : laquelle de ces portes d'entrée est la plus fréquente ?",
           "choix": ch(("Un mail piégé", "q2oui"), ("Un écran trop lumineux", "q2non"))},
    "q2oui": {"msg": "Exact : l'hameçonnage reste l'une des premières portes d'entrée.", "va": "q3"},
    "q2non": {"msg": "Ha ha, non ! Le mail piégé reste l'une des premières portes d'entrée.", "va": "q3"},
    "q3": {"msg": "Dernière : tu as un doute sur un comportement bizarre de ton ordinateur. Tu attends de voir ?",
           "choix": ch(("Non, je préviens tout de suite", "fin"), ("Oui, ça passera", "attendre"))},
    "attendre": {"msg": "Mieux vaut une fausse alerte qu'une attaque découverte trop tard. Préviens {{org.contact}} sans hésiter.", "va": "fin"},
    "fin": {"msg": "Sauvegarde débranchée, mails vérifiés, alerte rapide : tu fermes les portes. Bravo ! 👋", "fin": True}})

# ---------------------------------------------------------------- Continuer sans informatique
M["res-continuer-1"] = dict(rub="Résilience", theme="Continuer sans informatique", titre="Le jour où plus rien ne marche", source=CRISE, prio=["direction", "accueil", "educatif", "soin"],
    reflexe="Je garde sur papier les quelques informations indispensables : les contacts clés, les numéros d'urgence et la façon de travailler sans ordinateur.",
    etapes={
    "debut": {"msg": "Imagine : plus d'ordinateurs, plus de messagerie, plus de logiciels pendant trois jours. Tu sais comment joindre tes collègues ?",
              "choix": ch(("Oui, j'ai leurs numéros", "oui"), ("Euh… ils sont dans ma messagerie", "non"))},
    "oui": {"msg": "Parfait ! Et les autres informations indispensables ?", "va": "liste"},
    "non": {"msg": "C'est le piège classique : toutes les informations sont… dans l'ordinateur en panne !", "va": "liste"},
    "liste": {"msg": "Une panne, une coupure ou une attaque peut tout arrêter d'un coup. Ce jour-là, le papier redevient le meilleur ami.", "va": "quoi"},
    "quoi": {"msg": "Une simple feuille suffit : les numéros de l'équipe et de la direction, de {{org.contact}}, des partenaires clés, et des urgences.", "va": "facon"},
    "facon": {"msg": "Et pour les tâches vitales, comme les plannings, les rendez-vous ou les traitements : comment faire sans ordinateur ? Ça se prévoit à l'avance, calmement.", "va": "fin"},
    "fin": {"msg": "Une feuille de contacts imprimée et rangée, c'est une heure de travail qui peut sauver des jours. À demain ! 👋", "fin": True}})

M["res-continuer-2"] = dict(rub="Résilience", theme="Continuer sans informatique", titre="Mise en situation : la messagerie est coupée", source=CRISE, prio=["direction"],
    reflexe="Pendant un incident, je communique par un autre moyen (téléphone, SMS) et je me méfie des messages qui profitent de la confusion.",
    etapes={
    "debut": {"msg": "Suite à une attaque, la messagerie de {{org.nom_court}} est coupée. Un SMS arrive : « Ici le support, cliquez ici pour réactiver votre compte ». Tu cliques ?",
              "choix": ch(("Oui, il faut bien réactiver", "clic"), ("Je vérifie d'abord", "verifie"))},
    "clic": {"msg": "C'est très bien imité, mais les escrocs adorent profiter des moments de confusion. Une crise est le moment idéal pour eux.", "va": "canal"},
    "verifie": {"msg": "Excellent ! Comment vérifierais-tu ?",
                "choix": ch(("J'appelle {{org.contact}}", "canal"), ("Je réponds au SMS", "repond"))},
    "repond": {"msg": "Répondre à l'expéditeur ne prouve rien. On appelle plutôt un numéro connu.", "va": "canal"},
    "canal": {"msg": "Pendant un incident, les consignes officielles arrivent par un canal prévu à l'avance : un appel, un SMS d'un numéro connu, une réunion.", "va": "calme"},
    "calme": {"msg": "Et on garde son calme : on note ce qu'on a vu, avec l'heure. C'est précieux pour ceux qui réparent.", "va": "fin"},
    "fin": {"msg": "En crise, je passe par les canaux connus, et je me méfie encore plus. À demain ! 👋", "fin": True}})

M["res-continuer-3"] = dict(rub="Résilience", theme="Continuer sans informatique", titre="Quiz : prêt pour la panne ?", source=CRISE, prio=[],
    reflexe="Être prêt, c'est simple : une liste de contacts imprimée, des sauvegardes testées et une idée claire de qui fait quoi si tout s'arrête.",
    etapes={
    "debut": {"msg": "Quiz ! Où ranger la liste des contacts d'urgence ?",
              "choix": ch(("Imprimée, dans un endroit connu", "q1oui"), ("Dans un fichier sur le serveur", "q1non"))},
    "q1oui": {"msg": "Oui ! Accessible même quand tout est en panne.", "va": "q2"},
    "q1non": {"msg": "Si le serveur est en panne, la liste aussi ! On la garde aussi imprimée.", "va": "q2"},
    "q2": {"msg": "Question 2 : pendant un incident, tu remarques quelque chose d'étrange. Tu fais quoi ?",
           "choix": ch(("Je le note avec l'heure", "q2oui"), ("Je n'y pense plus", "q2non"))},
    "q2oui": {"msg": "Parfait, c'est très utile pour l'enquête.", "va": "q3"},
    "q2non": {"msg": "Note-le avec l'heure : un détail peut aider à comprendre l'attaque.", "va": "q3"},
    "q3": {"msg": "Dernière : s'entraîner à une panne, c'est utile ?",
           "choix": ch(("Oui, comme un exercice d'évacuation", "fin"), ("Non, on verra le jour J", "jourj"))},
    "jourj": {"msg": "Comme pour un incendie, on réagit bien mieux quand on s'est entraîné une fois. Même 30 minutes autour d'une table.", "va": "fin"},
    "fin": {"msg": "Bravo, tu as terminé la rubrique Résilience ! 👋", "fin": True}})

# ================================================================ GOUVERNANCE
# ---------------------------------------------------------------- Données personnelles
M["gou-donnees-1"] = dict(rub="Gouvernance", theme="Données personnelles", titre="Une donnée personnelle, c'est quoi ?", source=RGPD, prio=["rh", "soin", "educatif", "accueil"],
    reflexe="Une donnée personnelle, c'est toute information qui permet de reconnaître une personne. Je n'en collecte et je n'en partage que le strict nécessaire.",
    etapes={
    "debut": {"msg": "Question : parmi ces informations, laquelle est une donnée personnelle ? Un nom, un numéro de téléphone, une photo…",
              "choix": ch(("Seulement le nom", "nom"), ("Les trois", "trois"))},
    "nom": {"msg": "Le nom, oui, mais pas seulement ! Le téléphone et la photo aussi.", "va": "definition"},
    "trois": {"msg": "Exactement, les trois !", "va": "definition"},
    "definition": {"msg": "Une donnée personnelle, c'est toute information qui permet de reconnaître quelqu'un, directement ou en croisant plusieurs informations.", "va": "sensible"},
    "sensible": {"msg": "Certaines sont encore plus sensibles : la santé, la situation sociale, l'origine, les opinions. Elles demandent une attention particulière.", "va": "moins"},
    "moins": {"msg": "La règle d'or du RGPD : ne collecter que ce qui est vraiment utile, et ne le montrer qu'à ceux qui en ont besoin pour leur travail.", "va": "fin"},
    "fin": {"msg": "Le strict nécessaire, aux seules personnes concernées. C'est du respect avant d'être une loi. 👋", "fin": True}})

M["gou-donnees-2"] = dict(rub="Gouvernance", theme="Données personnelles", titre="Mise en situation : le mail à tous les adhérents", source=RGPD, prio=["benevoles", "accueil"],
    reflexe="Pour écrire à un groupe de personnes extérieures, je mets les adresses en copie cachée (Cci), pour que chacun ne voie pas les adresses des autres.",
    etapes={
    "debut": {"msg": "Tu envoies l'invitation à l'assemblée générale aux 120 adhérents. Tu mets les adresses où ?",
              "choix": ch(("Dans « À », toutes ensemble", "a"), ("En copie cachée (Cci)", "cci"))},
    "a": {"msg": "C'est très courant ! Mais alors, chaque adhérent reçoit les 119 autres adresses.", "va": "probleme"},
    "cci": {"msg": "Parfait ! Tu sais pourquoi c'est mieux ?",
            "choix": ch(("Pour protéger les adresses", "probleme"), ("Pas vraiment", "probleme"))},
    "probleme": {"msg": "Une adresse mail est une donnée personnelle. Certains ne veulent pas que leur adhésion se sache, et une liste d'adresses visible intéresse les escrocs.", "va": "repondre"},
    "repondre": {"msg": "En plus, avec « Répondre à tous », une réponse part chez 120 personnes. En copie cachée, elle n'arrive qu'à toi.", "va": "astuce"},
    "astuce": {"msg": "L'astuce : mets ta propre adresse dans « À », et toutes les autres dans « Cci ».", "va": "fin"},
    "fin": {"msg": "Un mail à un groupe extérieur ? Les adresses en copie cachée. À demain ! 👋", "fin": True}})

M["gou-donnees-3"] = dict(rub="Gouvernance", theme="Données personnelles", titre="Quiz : les données des personnes", source=DROITS, prio=[],
    reflexe="Chacun a le droit de savoir quelles données on garde sur lui et de les faire corriger. Si quelqu'un le demande, je transmets vite à la bonne personne.",
    etapes={
    "debut": {"msg": "Quiz ! Une personne demande quelles informations {{org.nom_court}} garde sur elle. Elle a le droit ?",
              "choix": ch(("Oui", "q1oui"), ("Non", "q1non"))},
    "q1oui": {"msg": "Oui, c'est le droit d'accès du RGPD.", "va": "q2"},
    "q1non": {"msg": "Si, c'est le droit d'accès du RGPD. Elle peut aussi faire corriger les informations fausses.", "va": "q2"},
    "q2": {"msg": "Question 2 : tu reçois cette demande. Tu fais quoi ?",
           "choix": ch(("Je la transmets à la personne responsable", "q2oui"), ("Je la laisse de côté", "q2non"))},
    "q2oui": {"msg": "Parfait : il y a un délai pour répondre, en général un mois.", "va": "q3"},
    "q2non": {"msg": "Il faut répondre dans un délai d'un mois en général : transmets-la vite à la personne responsable.", "va": "q3"},
    "q3": {"msg": "Dernière : un tableau avec les coordonnées de toutes les personnes accompagnées traîne sur le bureau partagé de l'ordinateur. Normal ?",
           "choix": ch(("Non, il faut le ranger et le protéger", "fin"), ("Oui, c'est pratique", "pratique"))},
    "pratique": {"msg": "Pratique, mais visible par tous ceux qui utilisent ce poste. Range-le dans un dossier dont l'accès est limité.", "va": "fin"},
    "fin": {"msg": "Les données des personnes se protègent comme on protège les personnes. Bravo ! 👋", "fin": True}})

# ---------------------------------------------------------------- Partage de fichiers
M["gou-partage-1"] = dict(rub="Gouvernance", theme="Partage de fichiers", titre="Le document de travail sur mon cloud perso", source=M10, prio=["benevoles", "direction"],
    reflexe="Les documents de {{org.nom_court}} restent sur les outils fournis par {{org.nom_court}}, pas sur mon cloud ou ma messagerie personnels.",
    etapes={
    "debut": {"msg": "Pour finir un dossier chez toi, tu l'envoies sur ta boîte mail personnelle ou ton cloud perso. Ça te paraît…",
              "choix": ch(("Pratique, je le fais souvent", "souvent"), ("Risqué", "risque"))},
    "souvent": {"msg": "C'est très courant, et c'est fait pour bien faire ! Mais voyons ce que ça change.", "va": "pourquoi"},
    "risque": {"msg": "Tu as raison. Tu sais pourquoi ?",
               "choix": ch(("On perd le contrôle du document", "pourquoi"), ("Pas vraiment", "pourquoi"))},
    "pourquoi": {"msg": "Sur ton compte personnel, le document échappe aux protections de {{org.nom_court}} : sauvegardes, droits d'accès, fermeture des comptes au départ.", "va": "perso"},
    "perso": {"msg": "Et si ton compte personnel est piraté un jour, les documents de travail partent avec.", "va": "solution"},
    "solution": {"msg": "La solution : demande à {{org.contact}} comment travailler à distance avec les outils de {{org.nom_court}}. Il y a souvent une solution simple.", "va": "fin"},
    "fin": {"msg": "Les documents de travail restent sur les outils de travail. À demain ! 👋", "fin": True}})

M["gou-partage-2"] = dict(rub="Gouvernance", theme="Partage de fichiers", titre="« Toute personne disposant du lien »", source=M10, prio=["accueil", "rh"],
    reflexe="Quand je partage un document, je choisis des personnes précises plutôt que « toute personne disposant du lien », et je mets une date de fin si je peux.",
    etapes={
    "debut": {"msg": "Tu partages un dossier avec un partenaire. L'outil propose : « Toute personne disposant du lien peut voir ». Tu choisis ça ?",
              "choix": ch(("Oui, c'est le plus simple", "simple"), ("Je préfère choisir les personnes", "personnes"))},
    "simple": {"msg": "C'est le plus simple, oui. Mais le lien peut être transféré, oublié dans un mail, ou publié par erreur. Et n'importe qui peut ouvrir le dossier.", "va": "mieux"},
    "personnes": {"msg": "Excellent réflexe !", "va": "mieux"},
    "mieux": {"msg": "Le mieux : partager avec les adresses précises des personnes concernées. Seules elles pourront ouvrir le dossier.", "va": "date"},
    "date": {"msg": "Encore mieux : mettre une date de fin au partage, ou le retirer quand le projet est terminé.", "va": "menage"},
    "menage": {"msg": "Et de temps en temps, un petit ménage dans tes partages : on est souvent surpris de ce qui est encore ouvert !", "va": "fin"},
    "fin": {"msg": "Des personnes précises, une date de fin, et un peu de ménage. À demain ! 👋", "fin": True}})

M["gou-partage-3"] = dict(rub="Gouvernance", theme="Partage de fichiers", titre="Quiz : partager sans fuiter", source=M10, prio=[],
    reflexe="Avant d'envoyer un document, je vérifie le destinataire, ce que contient le document, et le bon outil pour l'envoyer.",
    etapes={
    "debut": {"msg": "Quiz ! Avant d'envoyer un document sensible par mail, tu vérifies quoi en premier ?",
              "choix": ch(("L'adresse du destinataire", "q1oui"), ("La couleur du document", "q1non"))},
    "q1oui": {"msg": "Oui ! La saisie automatique propose parfois la mauvaise personne.", "va": "q2"},
    "q1non": {"msg": "Ha ha ! L'adresse du destinataire d'abord : la saisie automatique propose parfois un homonyme.", "va": "q2"},
    "q2": {"msg": "Question 2 : tu envoies un mail au mauvais destinataire avec des données personnelles. Tu fais quoi ?",
           "choix": ch(("Je préviens {{org.contact}}", "q2oui"), ("Je ne dis rien", "q2non"))},
    "q2oui": {"msg": "Bravo : une fuite de données doit parfois être déclarée, et vite.", "va": "q3"},
    "q2non": {"msg": "Une erreur, ça arrive. Mais il faut prévenir vite : certaines fuites doivent être déclarées sous 72 heures.", "va": "q3"},
    "q3": {"msg": "Dernière : un gros fichier à envoyer à un partenaire. Tu utilises…",
           "choix": ch(("L'outil fourni par {{org.nom_court}}", "fin"), ("Le premier site gratuit trouvé", "gratuit"))},
    "gratuit": {"msg": "Un site inconnu peut garder une copie de ton fichier. Demande l'outil prévu à {{org.contact}}.", "va": "fin"},
    "fin": {"msg": "Le bon destinataire, le bon outil, et une alerte rapide en cas d'erreur. Bravo ! 👋", "fin": True}})

# ---------------------------------------------------------------- IA générative
M["gou-ia-1"] = dict(rub="Gouvernance", theme="IA générative", titre="Ce que je colle dans l'IA", source=IA, prio=["tous"],
    reflexe="Je ne colle jamais de données personnelles ou confidentielles dans une IA en ligne. Ce que j'y écris peut être conservé et réutilisé.",
    etapes={
    "debut": {"msg": "Tu dois rédiger un compte rendu sur une personne accompagnée. Une IA en ligne pourrait t'aider. Tu colles tes notes telles quelles ?",
              "choix": ch(("Oui, ça me fera gagner du temps", "oui"), ("J'hésite", "hesite"))},
    "oui": {"msg": "Gagner du temps, c'est légitime ! Mais regarde où partent ces notes.", "va": "ou"},
    "hesite": {"msg": "Tu as raison d'hésiter. Voilà pourquoi.", "va": "ou"},
    "ou": {"msg": "Ce que tu écris dans une IA en ligne part sur les serveurs d'une entreprise. Il peut être conservé, relu, ou servir à entraîner l'outil.", "va": "sensible"},
    "sensible": {"msg": "Le nom d'une personne, sa santé, sa situation : ce sont des données personnelles, parfois sensibles. Elles n'ont rien à faire là.", "va": "comment"},
    "comment": {"msg": "Tu peux utiliser l'IA pour la forme : un modèle de compte rendu, une reformulation, sans aucun nom ni détail qui permette de reconnaître quelqu'un.", "va": "outil"},
    "outil": {"msg": "Et demande à {{org.contact}} quels outils d'IA sont autorisés dans {{org.nom_court}}.", "va": "fin"},
    "fin": {"msg": "L'IA pour la forme, jamais pour les données des personnes. À demain ! 👋", "fin": True}})

M["gou-ia-2"] = dict(rub="Gouvernance", theme="IA générative", titre="L'IA qui se trompe avec aplomb", source=IA, prio=["direction", "finances", "soin"],
    reflexe="Une IA peut inventer des faits avec assurance. Je relis et je vérifie tout ce qu'elle produit avant de m'en servir : c'est moi qui signe.",
    etapes={
    "debut": {"msg": "Une IA te répond avec assurance : « La loi impose ceci depuis 2019, article 12 ». Tu recopies dans ton courrier ?",
              "choix": ch(("Oui, elle a l'air sûre d'elle", "sure"), ("Je vérifie d'abord", "verifie"))},
    "sure": {"msg": "C'est le piège : une IA peut inventer un article de loi, une date ou un chiffre, et le dire avec une parfaite assurance.", "va": "pourquoi"},
    "verifie": {"msg": "Excellent réflexe !", "va": "pourquoi"},
    "pourquoi": {"msg": "Une IA générative produit un texte plausible, pas forcément un texte vrai. Elle ne « sait » pas quand elle se trompe.", "va": "signer"},
    "signer": {"msg": "Le courrier part pourtant avec ton nom ou celui de {{org.nom_court}}. C'est toi qui en es responsable, pas l'outil.", "va": "geste"},
    "geste": {"msg": "Le bon usage : l'IA propose, toi tu vérifies. Les chiffres, les dates, les références et les noms se contrôlent à la source.", "va": "fin"},
    "fin": {"msg": "L'IA est un assistant, pas une source. Je vérifie avant de signer. À demain ! 👋", "fin": True}})

M["gou-ia-3"] = dict(rub="Gouvernance", theme="IA générative", titre="Quiz : l'IA et moi", source=IA, prio=[],
    reflexe="Pas de données personnelles ni confidentielles dans une IA en ligne, une vérification de tout ce qu'elle produit, et seulement les outils autorisés.",
    etapes={
    "debut": {"msg": "Quiz ! Tu peux demander à une IA de reformuler un mail…",
              "choix": ch(("Sans noms ni détails personnels", "q1oui"), ("Avec toutes les infos, c'est plus précis", "q1non"))},
    "q1oui": {"msg": "Parfait : sans données personnelles, aucun souci.", "va": "q2"},
    "q1non": {"msg": "Plus précis, mais tes informations partent chez l'éditeur de l'IA. On retire les noms et les détails d'abord.", "va": "q2"},
    "q2": {"msg": "Question 2 : un message vocal de ta directrice te demande un virement urgent. Ça pourrait être une IA qui imite sa voix ?",
           "choix": ch(("Oui, c'est possible", "q2oui"), ("Non, impossible", "q2non"))},
    "q2oui": {"msg": "Oui : imiter une voix est devenu facile. D'où le réflexe de rappeler sur un numéro connu.", "va": "q3"},
    "q2non": {"msg": "C'est devenu facile, hélas. Une demande inhabituelle se vérifie en rappelant sur un numéro connu, même si la voix est familière.", "va": "q3"},
    "q3": {"msg": "Dernière : qui décide des outils d'IA utilisables au travail ?",
           "choix": ch(("{{org.nom_court}}, avec {{org.contact}}", "fin"), ("Chacun choisit le sien", "chacun"))},
    "chacun": {"msg": "Chacun son outil, c'est chacun ses risques. On utilise ceux que {{org.nom_court}} a choisis et vérifiés.", "va": "fin"},
    "fin": {"msg": "Bravo, tu as terminé la rubrique Gouvernance ! 👋", "fin": True}})

# ================================================================ OBLIGATIONS NIS 2
M["nis2-intro-1"] = dict(rub="Obligations NIS 2", theme="NIS2 en 2 minutes", titre="La cybersécurité vient d'évoluer en France", source=NIS2, prio=["direction"],
    reflexe="NIS2 fait de la cybersécurité une obligation pour des milliers d'organisations en France, et ses exigences touchent aussi leurs partenaires et fournisseurs.",
    etapes={
    "debut": {"msg": "Tu savais que la cybersécurité vient de beaucoup évoluer en France ?",
              "choix": ch(("Non, raconte !", "raconte"), ("Oui, NIS2 !", "nis2"))},
    "raconte": {"msg": "Alors voici l'essentiel en 2 minutes !", "va": "quoi"},
    "nis2": {"msg": "Bravo, tu suis l'actualité ! Petit rappel quand même…", "va": "quoi"},
    "quoi": {"msg": "NIS2 est une directive européenne sur la cybersécurité. En France, la loi qui l'applique, dite loi « Résilience », a été adoptée par l'Assemblée nationale en novembre 2026.", "va": "qui"},
    "qui": {"msg": "Avant, quelques centaines d'organisations étaient concernées. Avec NIS2, on passe à plus de 15 000 : entreprises, hôpitaux, collectivités…", "va": "obligations"},
    "obligations": {"msg": "Elles devront gérer leurs risques cyber, déclarer leurs incidents graves, et leurs dirigeants devront se former.", "va": "petits"},
    "petits": {"msg": "Ta structure n'est pas concernée directement ? Tes partenaires, tes clients ou tes financeurs peuvent l'être, et ils te poseront des questions.", "va": "fin"},
    "fin": {"msg": "La cybersécurité devient une obligation, pas une option. Et tous les modules que tu as faits t'y préparent déjà ! 👋", "fin": True}})

M["nis2-intro-2"] = dict(rub="Obligations NIS 2", theme="NIS2 en 2 minutes", titre="Pourquoi la direction doit se former", source=NIS2, prio=["direction"],
    reflexe="Avec NIS2, la cybersécurité est une responsabilité de la direction : elle doit valider les mesures, les suivre, et se former.",
    etapes={
    "debut": {"msg": "Selon toi, avec NIS2, la cybersécurité, c'est l'affaire de qui ?",
              "choix": ch(("Du service informatique", "info"), ("De la direction aussi", "direction"))},
    "info": {"msg": "Le service informatique fait beaucoup ! Mais NIS2 change la donne.", "va": "dirigeants"},
    "direction": {"msg": "Exactement, et c'est la grande nouveauté !", "va": "dirigeants"},
    "dirigeants": {"msg": "NIS2 demande aux organes de direction de valider les mesures de cybersécurité, d'en suivre la mise en œuvre, et de se former.", "va": "pourquoi"},
    "pourquoi": {"msg": "Pourquoi ? Parce que les décisions qui comptent sont souvent budgétaires ou organisationnelles : sauvegardes, remplacements, formations.", "va": "salaries"},
    "salaries": {"msg": "La directive encourage aussi la formation régulière de tout le personnel. Ces 2 minutes par jour en font partie !", "va": "fin"},
    "fin": {"msg": "La cybersécurité se décide en haut et se vit partout. À demain ! 👋", "fin": True}})

M["nis2-intro-3"] = dict(rub="Obligations NIS 2", theme="NIS2 en 2 minutes", titre="Quiz : NIS2", source=ESPACE, prio=["direction"],
    reflexe="Pour savoir si ma structure est concernée par NIS2, l'ANSSI propose un test en ligne sur MonEspaceNIS2.",
    etapes={
    "debut": {"msg": "Quiz ! NIS2, c'est…",
              "choix": ch(("Une directive européenne sur la cybersécurité", "q1oui"), ("Un nouveau logiciel", "q1non"))},
    "q1oui": {"msg": "Exact !", "va": "q2"},
    "q1non": {"msg": "C'est une directive européenne sur la cybersécurité, appliquée en France par une loi.", "va": "q2"},
    "q2": {"msg": "Question 2 : combien d'organisations sont concernées en France, environ ?",
           "choix": ch(("Plus de 15 000", "q2oui"), ("Une centaine", "q2non"))},
    "q2oui": {"msg": "Oui, contre quelques centaines avant.", "va": "q3"},
    "q2non": {"msg": "C'était à peu près le cas avant. Avec NIS2, on passe à plus de 15 000.", "va": "q3"},
    "q3": {"msg": "Dernière : comment savoir si ta structure est concernée ?",
           "choix": ch(("Le test de l'ANSSI sur MonEspaceNIS2", "fin"), ("Attendre un courrier", "courrier"))},
    "courrier": {"msg": "Mieux vaut ne pas attendre : l'ANSSI propose un test en ligne sur MonEspaceNIS2.", "va": "fin"},
    "fin": {"msg": "Le test MonEspaceNIS2 prend quelques minutes. Parles-en à ta direction ! 👋", "fin": True}})

M["nis2-incident-1"] = dict(rub="Obligations NIS 2", theme="Incident : les premières heures", titre="L'horloge de l'incident", source=NIS2, prio=["direction"],
    reflexe="Pour les structures concernées par NIS2, un incident grave se signale vite à l'ANSSI : une alerte sous 24 heures. D'où l'importance de prévenir tout de suite en interne.",
    etapes={
    "debut": {"msg": "Un incident grave touche une organisation concernée par NIS2. À ton avis, elle a combien de temps pour donner une première alerte à l'ANSSI ?",
              "choix": ch(("Une semaine", "semaine"), ("24 heures", "h24"))},
    "semaine": {"msg": "C'est beaucoup plus court que ça !", "va": "delais"},
    "h24": {"msg": "Exactement, 24 heures !", "va": "delais"},
    "delais": {"msg": "NIS2 prévoit une alerte précoce sous 24 heures, une notification plus complète sous 72 heures, puis un rapport final dans le mois.", "va": "toi"},
    "toi": {"msg": "Et l'horloge démarre quand l'organisation a connaissance de l'incident. Si personne ne prévient en interne, on perd des heures précieuses.", "va": "role"},
    "role": {"msg": "C'est là que tu comptes : le moindre doute signalé tôt à {{org.contact}} permet à ta structure de réagir à temps.", "va": "fin"},
    "fin": {"msg": "24 heures, ça va vite. Ton signalement rapide fait partie de la réponse. À demain ! 👋", "fin": True}})

M["nis2-incident-2"] = dict(rub="Obligations NIS 2", theme="Incident : les premières heures", titre="Mise en situation : vendredi, 17 h 45", source=NIS2, prio=["direction", "accueil"],
    reflexe="Un incident n'attend pas lundi : je préviens tout de suite, même un vendredi soir, avec ce que j'ai vu et l'heure.",
    etapes={
    "debut": {"msg": "Vendredi, 17 h 45. Tu vois des connexions bizarres à ta messagerie depuis l'étranger. Tu pars en week-end dans 15 minutes. Tu fais quoi ?",
              "choix": ch(("Je préviens tout de suite", "tout_suite"), ("J'en parlerai lundi", "lundi"))},
    "lundi": {"msg": "Le week-end, c'est justement le moment préféré des attaquants : il y a moins de monde pour réagir. Lundi, ce serait 60 heures de perdues.", "va": "quoi"},
    "tout_suite": {"msg": "Parfait ! Et tu dis quoi ?",
                   "choix": ch(("Ce que j'ai vu, avec l'heure", "quoi"), ("Juste « ça ne marche pas »", "quoi"))},
    "quoi": {"msg": "Le plus utile : ce que tu as vu, à quelle heure, sur quel compte ou quel appareil. Une capture d'écran aide aussi.", "va": "qui"},
    "qui": {"msg": "Préviens {{org.contact}}, {{org.contact_detail}}. S'il n'y a personne, suis la procédure d'urgence prévue, ou 17Cyber.gouv.fr.", "va": "mdp"},
    "mdp": {"msg": "Et si c'est ton compte, change ton mot de passe tout de suite depuis un autre appareil.", "va": "fin"},
    "fin": {"msg": "Un doute un vendredi soir mérite 5 minutes avant de partir. Bon week-end, l'esprit tranquille ! 👋", "fin": True}})

M["nis2-incident-3"] = dict(rub="Obligations NIS 2", theme="Incident : les premières heures", titre="Quiz final : les premières heures", source=NIS2, prio=[],
    reflexe="Signaler vite, décrire ce que j'ai vu, ne rien effacer et ne pas payer : c'est la meilleure aide que je puisse apporter pendant un incident.",
    etapes={
    "debut": {"msg": "Dernier quiz de toute la série ! Pendant un incident, effacer les mails suspects pour « nettoyer », c'est…",
              "choix": ch(("Une mauvaise idée", "q1oui"), ("Une bonne idée", "q1non"))},
    "q1oui": {"msg": "Oui : ce sont des indices pour l'enquête.", "va": "q2"},
    "q1non": {"msg": "Ce sont des indices précieux pour comprendre l'attaque. On les garde, et on les montre à {{org.contact}}.", "va": "q2"},
    "q2": {"msg": "Question 2 : qui doit être prévenu en premier ?",
           "choix": ch(("{{org.contact}}", "q2oui"), ("Mes amis sur les réseaux sociaux", "q2non"))},
    "q2oui": {"msg": "Exact.", "va": "q3"},
    "q2non": {"msg": "Surtout pas sur les réseaux sociaux ! On prévient {{org.contact}}, qui organise la suite.", "va": "q3"},
    "q3": {"msg": "Dernière question : signaler une erreur qu'on a faite soi-même, c'est…",
           "choix": ch(("Courageux et utile", "fin"), ("Risqué pour moi", "risque"))},
    "risque": {"msg": "Au contraire : signaler vite est le meilleur service à rendre. Une erreur cachée coûte bien plus cher qu'une erreur signalée.", "va": "fin"},
    "fin": {"msg": "Bravo, tu as terminé les 60 modules de base ! Tes réflexes cyber sont en place. Merci, et à bientôt pour les actualités ! 🪂", "fin": True}})


def main():
    racine = Path(__file__).resolve().parent.parent / "modules"
    dossiers = {"Résilience": "resilience", "Gouvernance": "gouvernance", "Obligations NIS 2": "nis2"}
    for mid, m in M.items():
        d = racine / dossiers[m["rub"]]
        d.mkdir(parents=True, exist_ok=True)
        f = d / f"{mid}.json"
        if f.exists() and json.loads(f.read_text(encoding="utf-8")).get("statut") != "brouillon":
            print(f"  conservé (déjà relu) : {f.name}")
            continue
        prio = [p for p in m["prio"] if p != "tous"]
        doc = {"id": mid, "rubrique": m["rub"], "theme": m["theme"], "titre": m["titre"], "reflexe": m["reflexe"],
               "source": m["source"], "metiers": ["tous"], "prioritaire_pour": prio, "statut": "brouillon"}
        if m["rub"] == "Obligations NIS 2":
            doc["perime_le"] = PEREMPTION_NIS2
        doc["etapes"] = m["etapes"]
        f.write_text(json.dumps(doc, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
    print(f"{len(M)} modules traités")


if __name__ == "__main__":
    main()
