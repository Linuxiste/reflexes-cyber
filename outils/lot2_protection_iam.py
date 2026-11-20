#!/usr/bin/env python3
"""Lot 2, partie 1 (rubrique Protection, identités et accès) : 12 modules JSON dans modules/protection/.

Thèmes : mots de passe, double authentification, comptes partagés et départs, droits d'administrateur.
Gardé pour mémoire : une fois les modules relus et corrigés dans les JSON, ne plus relancer
ce script (il écraserait les corrections). Il refuse d'écraser un module déjà « relu ».
"""
import json
from pathlib import Path

GI = {"nom": "ANSSI, ReCyF en pratique : Gestion des identités (v1.0, septembre 2026)",
      "url": "https://messervices.cyber.gouv.fr/documents-guides/Fiche_Gestion-des-identites_Protection_VF.pdf"}
ADM = {"nom": "ANSSI, ReCyF en pratique : Administration (v1.0, septembre 2026)",
       "url": "https://messervices.cyber.gouv.fr/documents-guides/Fiche_Administration_Protection_VF.pdf"}
M10 = {"nom": "Cybermalveillance.gouv.fr, 10 mesures essentielles",
       "url": "https://www.cybermalveillance.gouv.fr/tous-nos-contenus/bonnes-pratiques/10-mesures-essentielles-assurer-securite-numerique"}


def ch(*paires):
    return [{"txt": t, "va": v} for t, v in paires]


M = {}

# ---------------------------------------------------------------- Mots de passe
M["pro-mdp-1"] = dict(theme="Mots de passe", titre="Le même mot de passe partout",
    source=M10, prio=["benevoles"],
    reflexe="Un mot de passe différent pour chaque compte important. Si un site se fait voler ses mots de passe, les autres comptes restent protégés.",
    etapes={
    "debut": {"msg": "Salut, c'est {{perso}} ! Question franche, entre nous : tu utilises le même mot de passe pour plusieurs comptes ?",
              "choix": ch(("Oui, c'est plus simple", "oui"), ("Non, jamais", "non"))},
    "oui": {"msg": "Merci pour ta franchise, tu es loin d'être le seul ! Voyons pourquoi c'est risqué.", "va": "fuite"},
    "non": {"msg": "Bravo ! Tu vas pouvoir expliquer pourquoi à tes collègues.", "va": "fuite"},
    "fuite": {"msg": "Chaque année, des sites se font voler leurs fichiers de mots de passe. Ce n'est pas ta faute : c'est le site qui est piraté.", "va": "essai"},
    "essai": {"msg": "Les escrocs essaient alors automatiquement ce mot de passe sur ta messagerie, ta banque, tes réseaux sociaux…", "va": "domino"},
    "domino": {"msg": "Avec un seul mot de passe partout, une fuite sur un petit site de jardinage peut ouvrir ta messagerie de travail. C'est l'effet domino.", "va": "solution"},
    "solution": {"msg": "La parade : un mot de passe différent pour chaque compte important. Demain, je te montre comment t'en souvenir sans effort.", "va": "fin"},
    "fin": {"msg": "Un compte, un mot de passe. Une fuite reste alors une petite fuite. À demain ! 👋", "fin": True}})

M["pro-mdp-2"] = dict(theme="Mots de passe", titre="La phrase de passe et le coffre-fort",
    source=M10, prio=["benevoles"],
    reflexe="Une phrase de passe de plusieurs mots est longue, donc solide, et facile à retenir. Un gestionnaire de mots de passe retient tous les autres pour moi.",
    etapes={
    "debut": {"msg": "Lequel de ces deux mots de passe est le plus solide, selon toi ? « P@ssw0rd! » ou « parapente-cerise-lundi-violon » ?",
              "choix": ch(("P@ssw0rd!", "court"), ("La phrase avec des mots", "long"))},
    "court": {"msg": "Il a l'air compliqué, mais il est très connu des pirates et bien trop court. Leurs logiciels le trouvent en quelques secondes.", "va": "longueur"},
    "long": {"msg": "Exact ! Et en plus, il est bien plus facile à retenir.", "va": "longueur"},
    "longueur": {"msg": "Le secret, c'est la longueur. Quatre ou cinq mots choisis au hasard, sans lien entre eux, font une phrase de passe très solide.", "va": "nombre"},
    "nombre": {"msg": "« Mais je ne vais pas retenir 30 phrases ! » Bonne nouvelle : tu n'as pas à le faire.",
               "choix": ch(("Ah bon ?", "coffre"), ("Je les note sur un carnet", "carnet"))},
    "carnet": {"msg": "Un carnet rangé chez toi vaut mieux qu'un seul mot de passe partout. Mais au bureau, un post-it sur l'écran, non !", "va": "coffre"},
    "coffre": {"msg": "Un gestionnaire de mots de passe est un coffre-fort qui les retient tous. Toi, tu ne retiens qu'une seule phrase de passe : celle du coffre.", "va": "fin"},
    "fin": {"msg": "Une phrase de passe pour le coffre, et le coffre retient le reste. Demande à {{org.contact}} lequel utiliser. 👋", "fin": True}})

M["pro-mdp-3"] = dict(theme="Mots de passe", titre="Quiz éclair : les mots de passe",
    source=M10, prio=[],
    reflexe="Un mot de passe se garde pour soi : on ne le donne ni par mail, ni par téléphone, ni à un collègue. Personne de sérieux ne le demande.",
    etapes={
    "debut": {"msg": "Quiz éclair, 3 questions ! Ce qui rend un mot de passe solide avant tout, c'est…",
              "choix": ch(("Sa longueur", "q1oui"), ("Les caractères spéciaux", "q1non"))},
    "q1oui": {"msg": "Oui ! Plus c'est long, plus c'est solide.", "va": "q2"},
    "q1non": {"msg": "Ils aident un peu, mais c'est surtout la longueur qui compte. Une phrase de plusieurs mots bat un mot court plein de symboles.", "va": "q2"},
    "q2": {"msg": "Question 2 : avant de partir en congé, un collègue te donne son mot de passe pour que tu le dépannes. Bonne idée ?",
           "choix": ch(("Oui, ça rend service", "q2non"), ("Non, mieux vaut demander un accès", "q2oui"))},
    "q2non": {"msg": "C'est gentil, mais ensuite, impossible de savoir qui a fait quoi sur son compte. On demande plutôt un accès à {{org.contact}}.", "va": "q3"},
    "q2oui": {"msg": "Bien vu ! Chacun son compte, chacun ses actions.", "va": "q3"},
    "q3": {"msg": "Dernière : un mail du « support » te demande ton mot de passe pour une maintenance. Tu le donnes ?",
           "choix": ch(("Jamais", "fin"), ("Si c'est le support, oui", "jamais"))},
    "jamais": {"msg": "Aucun support sérieux ne demande ton mot de passe. Jamais, même pour une maintenance.", "va": "fin"},
    "fin": {"msg": "Long, unique, et gardé pour soi : ton mot de passe est en de bonnes mains. À demain ! 👋", "fin": True}})

# ---------------------------------------------------------------- Double authentification
M["pro-2fa-1"] = dict(theme="Double authentification", titre="La deuxième serrure",
    source=GI, prio=["direction", "finances", "accueil"],
    reflexe="J'active la double authentification sur ma messagerie et mes comptes importants. Même si mon mot de passe est volé, le compte reste fermé.",
    etapes={
    "debut": {"msg": "Imagine : un escroc a réussi à voler ton mot de passe de messagerie. Il peut entrer ?",
              "choix": ch(("Oui, forcément", "oui"), ("Ça dépend", "depend"))},
    "oui": {"msg": "Avec un mot de passe seul, oui. Sauf si ta porte a une deuxième serrure !", "va": "deux"},
    "depend": {"msg": "Exactement, ça dépend d'une chose : la deuxième serrure.", "va": "deux"},
    "deux": {"msg": "La double authentification, c'est demander deux preuves : ce que tu sais (ton mot de passe) et ce que tu possèdes (ton téléphone, par exemple).", "va": "effet"},
    "effet": {"msg": "L'escroc a ton mot de passe, mais pas ton téléphone dans sa poche. Résultat : la porte reste fermée.", "va": "ou"},
    "ou": {"msg": "C'est l'une des protections les plus efficaces contre le vol de mot de passe et l'hameçonnage. Commence par ta messagerie : elle donne accès à tout le reste.", "va": "fin"},
    "fin": {"msg": "Deux preuves valent mieux qu'une. Demain, je te montre comment ça se passe au quotidien. 👋", "fin": True}})

M["pro-2fa-2"] = dict(theme="Double authentification", titre="La demande de validation surprise",
    source=GI, prio=["direction", "finances"],
    reflexe="Une demande de validation ou un code que je n'ai pas demandé ? Je refuse, je ne donne le code à personne, et je change mon mot de passe.",
    etapes={
    "debut": {"msg": "Tu regardes la télé, et ton téléphone affiche : « Tentative de connexion à votre messagerie. Valider ? » Tu n'as rien demandé. Tu fais quoi ?",
              "choix": ch(("Je valide pour que ça s'arrête", "valide"), ("Je refuse", "refuse"))},
    "valide": {"msg": "C'est ce qu'espère l'escroc ! Il connaît déjà ton mot de passe, et il ne lui manque que ta validation.", "va": "signe"},
    "refuse": {"msg": "Parfait ! Et tu sais ce que ça veut dire ?",
               "choix": ch(("Quelqu'un a mon mot de passe", "signe"), ("Un bug, sûrement", "signe"))},
    "signe": {"msg": "Une demande que tu n'as pas faite signifie souvent que quelqu'un connaît ton mot de passe. Ta deuxième serrure vient de le bloquer.", "va": "insiste"},
    "insiste": {"msg": "Parfois, les demandes arrivent en rafale pour te fatiguer, ou quelqu'un t'appelle pour te réclamer le code. Ne cède jamais.", "va": "geste"},
    "geste": {"msg": "Le bon geste : refuser, changer ton mot de passe, et prévenir {{org.contact}} si c'est un compte de travail.", "va": "fin"},
    "fin": {"msg": "Je ne valide que ce que je viens de demander moi-même. À demain ! 👋", "fin": True}})

M["pro-2fa-3"] = dict(theme="Double authentification", titre="Quiz : les deux preuves",
    source=GI, prio=[],
    reflexe="Les deux preuves sont : ce que je sais (mot de passe), ce que je possède (téléphone, clé) ou ce que je suis (empreinte). Deux de familles différentes.",
    etapes={
    "debut": {"msg": "Quiz ! Lequel de ces éléments est « quelque chose que tu possèdes » ?",
              "choix": ch(("Mon téléphone", "q1oui"), ("Mon code PIN", "q1non"))},
    "q1oui": {"msg": "Oui ! Le code PIN, lui, c'est quelque chose que tu sais.", "va": "q2"},
    "q1non": {"msg": "Le code PIN, c'est quelque chose que tu sais, comme un mot de passe. Ton téléphone, lui, tu le possèdes.", "va": "q2"},
    "q2": {"msg": "Question 2 : deux mots de passe à la suite, c'est une double authentification ?",
           "choix": ch(("Oui", "q2non"), ("Non", "q2oui"))},
    "q2oui": {"msg": "Bien vu ! Deux choses que tu sais, ça reste une seule famille de preuve.", "va": "q3"},
    "q2non": {"msg": "Pas vraiment : ce sont deux choses que tu sais. Il faut deux familles différentes, comme un mot de passe et ton téléphone.", "va": "q3"},
    "q3": {"msg": "Dernière : par quel compte commencer pour activer la double authentification ?",
           "choix": ch(("Ma messagerie", "fin"), ("Mon site de recettes", "recettes"))},
    "recettes": {"msg": "Commence plutôt par ta messagerie : c'est elle qui sert à réinitialiser tous tes autres mots de passe.", "va": "fin"},
    "fin": {"msg": "Deux preuves de familles différentes, en commençant par la messagerie. Bravo ! 👋", "fin": True}})

# ---------------------------------------------------------------- Comptes partagés et départs
M["pro-comptes-1"] = dict(theme="Comptes partagés et départs", titre="Le mot de passe de toute l'équipe",
    source=GI, prio=["benevoles", "educatif", "accueil"],
    reflexe="Un compte par personne. Quand un compte partagé est vraiment nécessaire, on note qui l'utilise et quand, et on change son mot de passe à chaque départ.",
    etapes={
    "debut": {"msg": "Dis-moi : chez {{org.nom_court}}, il y a une boîte mail ou un logiciel dont tout le monde connaît le même mot de passe ?",
              "choix": ch(("Oui, c'est pratique", "oui"), ("Non, chacun a son compte", "non"))},
    "oui": {"msg": "C'est très courant, et c'est souvent fait pour gagner du temps. Voyons ce que ça change.", "va": "qui"},
    "non": {"msg": "Super ! Voyons quand même pourquoi c'est important, pour pouvoir l'expliquer.", "va": "qui"},
    "qui": {"msg": "Avec un compte partagé, si un message bizarre part ou si un fichier disparaît, impossible de savoir qui l'a fait. Même pas pour se défendre.", "va": "depart"},
    "depart": {"msg": "Et quand quelqu'un quitte l'équipe, il garde le mot de passe en poche, souvent sans même y penser.", "va": "regle"},
    "regle": {"msg": "La règle de base : un compte par personne. Si un compte partagé est vraiment nécessaire, on note qui l'utilise et quand.", "va": "changer"},
    "changer": {"msg": "Et à chaque départ, on change son mot de passe. Ça prend deux minutes et ça ferme la porte.", "va": "fin"},
    "fin": {"msg": "Un compte par personne, ou un cahier pour le compte partagé. À demain ! 👋", "fin": True}})

M["pro-comptes-2"] = dict(theme="Comptes partagés et départs", titre="Mise en situation : le départ de Sam",
    source=GI, prio=["rh", "direction", "benevoles"],
    reflexe="Quand quelqu'un part, ses comptes sont désactivés sans délai. Je préviens {{org.contact}} dès que je connais la date de départ.",
    etapes={
    "debut": {"msg": "Sam, qui gérait le planning, quitte l'équipe vendredi. Que faut-il prévoir côté informatique ?",
              "choix": ch(("Rien, il rendra son badge", "rien"), ("Fermer ses accès", "fermer"))},
    "rien": {"msg": "Le badge, oui ! Mais ses comptes informatiques continuent d'exister, eux. On les oublie facilement.", "va": "risque"},
    "fermer": {"msg": "Exactement. Tu penses à lesquels ?",
               "choix": ch(("Sa messagerie et ses logiciels", "risque"), ("Je ne sais pas trop", "risque"))},
    "risque": {"msg": "Messagerie, logiciels, partages de fichiers, groupes de discussion… Un compte oublié peut être utilisé des mois plus tard, par lui ou par quelqu'un d'autre.", "va": "desactiver"},
    "desactiver": {"msg": "La règle : désactiver ses comptes dès son départ. Désactiver plutôt que supprimer, pour garder ses documents et l'historique.", "va": "qui"},
    "qui": {"msg": "Le plus simple : prévenir {{org.contact}} dès que la date de départ est connue. Pareil pour une longue absence.", "va": "fin"},
    "fin": {"msg": "Un départ annoncé, des accès fermés. Sam partira l'esprit tranquille, et toi aussi. 👋", "fin": True}})

M["pro-comptes-3"] = dict(theme="Comptes partagés et départs", titre="Quiz : qui a fait quoi ?",
    source=GI, prio=["rh"],
    reflexe="Chaque action doit pouvoir être rattachée à une personne : un compte par personne, des comptes fermés aux départs, et une revue régulière des comptes.",
    etapes={
    "debut": {"msg": "Quiz ! Un collègue absent pour 6 mois : que devient son compte ?",
              "choix": ch(("On le laisse ouvert", "q1non"), ("On le désactive en attendant", "q1oui"))},
    "q1non": {"msg": "Un compte inutilisé pendant des mois est une porte que personne ne surveille. On le désactive, et on le réactive à son retour.", "va": "q2"},
    "q1oui": {"msg": "Oui, et on le réactive à son retour.", "va": "q2"},
    "q2": {"msg": "Question 2 : on trouve un compte au nom de quelqu'un qui est parti il y a un an. Normal ?",
           "choix": ch(("Non, il faut le fermer", "q2oui"), ("Ce n'est pas grave", "q2non"))},
    "q2oui": {"msg": "Bien vu ! C'est pour ça qu'on fait régulièrement le tour des comptes.", "va": "q3"},
    "q2non": {"msg": "C'est un oubli fréquent, mais risqué. D'où l'intérêt de faire régulièrement le tour des comptes.", "va": "q3"},
    "q3": {"msg": "Dernière : à quoi sert « un compte par personne » ?",
           "choix": ch(("À savoir qui a fait quoi", "fin"), ("À surveiller les gens", "surveiller"))},
    "surveiller": {"msg": "Non : ça sert surtout à protéger chacun. Si un problème arrive avec ton compte, on sait que ce n'est pas toi qui as utilisé celui d'un autre.", "va": "fin"},
    "fin": {"msg": "Un compte par personne, fermé au départ, et vérifié de temps en temps. Bravo ! 👋", "fin": True}})

# ---------------------------------------------------------------- Droits d'administrateur
M["pro-admin-1"] = dict(theme="Droits d'administrateur", titre="Les clés de tout le bâtiment",
    source=ADM, prio=["direction", "benevoles"],
    reflexe="Au quotidien (mails, Internet, bureautique), j'utilise un compte simple. Le compte administrateur sert seulement à installer ou régler l'ordinateur.",
    etapes={
    "debut": {"msg": "Petite image : tu préfères te promener avec la clé de ton bureau, ou avec le trousseau qui ouvre tout le bâtiment ?",
              "choix": ch(("La clé de mon bureau", "bureau"), ("Le trousseau, c'est pratique", "trousseau"))},
    "bureau": {"msg": "Sage ! Si tu la perds, seul ton bureau est exposé.", "va": "admin"},
    "trousseau": {"msg": "Pratique, oui… jusqu'au jour où tu le perds. Là, c'est tout le bâtiment qui est ouvert.", "va": "admin"},
    "admin": {"msg": "Sur un ordinateur, c'est pareil. Un compte administrateur peut tout installer, tout modifier, tout effacer : c'est le trousseau.", "va": "piege"},
    "piege": {"msg": "Si tu lis tes mails avec ce compte et que tu ouvres une pièce jointe piégée, le logiciel malveillant hérite de tout ce pouvoir.", "va": "regle"},
    "regle": {"msg": "La règle : un compte simple pour le quotidien (mails, Internet, documents), et le compte administrateur seulement pour installer ou régler la machine.", "va": "fin"},
    "fin": {"msg": "Le trousseau reste au coffre, je sors avec la clé de mon bureau. À demain ! 👋", "fin": True}})

M["pro-admin-2"] = dict(theme="Droits d'administrateur", titre="Mise en situation : « Il me faut les droits admin »",
    source=ADM, prio=["direction"],
    reflexe="Besoin d'installer un logiciel ? Je demande à {{org.contact}} plutôt que de réclamer des droits administrateur permanents.",
    etapes={
    "debut": {"msg": "Tu as besoin d'installer un petit logiciel pour ton travail, mais l'ordinateur refuse. Tu fais quoi ?",
              "choix": ch(("Je demande les droits admin pour toujours", "toujours"), ("Je demande l'installation", "demande"))},
    "toujours": {"msg": "C'est tentant pour ne plus être bloqué ! Mais ces droits resteraient ouverts tout le temps, y compris pour un logiciel malveillant.", "va": "moindre"},
    "demande": {"msg": "Bon réflexe ! Et tu sais pourquoi c'est mieux ainsi ?",
                "choix": ch(("Pour limiter les risques", "moindre"), ("Pas vraiment", "moindre"))},
    "moindre": {"msg": "C'est le principe du « moindre privilège » : chacun a juste les droits nécessaires à son travail, pas plus.", "va": "pas"},
    "pas": {"msg": "Ce n'est pas un manque de confiance en toi. C'est pour qu'une erreur ou un piège ait le moins de conséquences possible.", "va": "geste"},
    "geste": {"msg": "Le bon geste : demander l'installation à {{org.contact}}, qui vérifie aussi que le logiciel est sûr. Et c'est souvent rapide !", "va": "fin"},
    "fin": {"msg": "Juste les droits nécessaires, et une demande quand il en faut plus. À demain ! 👋", "fin": True}})

M["pro-admin-3"] = dict(theme="Droits d'administrateur", titre="Quiz : le bon compte au bon moment",
    source=ADM, prio=[],
    reflexe="Compte simple pour les mails, Internet et les documents ; compte administrateur seulement pour administrer. Et jamais l'inverse.",
    etapes={
    "debut": {"msg": "Quiz ! Pour lire tes mails, tu utilises quel compte ?",
              "choix": ch(("Mon compte simple", "q1oui"), ("Le compte administrateur", "q1non"))},
    "q1oui": {"msg": "Parfait : c'est le compte du quotidien.", "va": "q2"},
    "q1non": {"msg": "Les mails sont la porte d'entrée n° 1 des pièges : on les lit avec un compte simple, aux droits limités.", "va": "q2"},
    "q2": {"msg": "Question 2 : pour installer une imprimante, tu as besoin de…",
           "choix": ch(("Droits administrateur", "q2oui"), ("Rien de spécial", "q2non"))},
    "q2oui": {"msg": "Oui, c'est le moment de l'utiliser, puis de revenir à ton compte simple.", "va": "q3"},
    "q2non": {"msg": "Installer un pilote modifie l'ordinateur : il faut des droits administrateur. On s'en sert, puis on revient au compte simple.", "va": "q3"},
    "q3": {"msg": "Dernière : sur ton ordinateur personnel, tu as souvent un seul compte, administrateur. Que faire ?",
           "choix": ch(("Créer un compte simple pour tous les jours", "fin"), ("Rien, c'est chez moi", "maison"))},
    "maison": {"msg": "Chez toi aussi, un compte simple pour tous les jours limite beaucoup les dégâts d'un piège. Ça se crée en deux minutes.", "va": "fin"},
    "fin": {"msg": "Le bon compte au bon moment : la série « identités et accès » est terminée. Bravo ! 👋", "fin": True}})


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
