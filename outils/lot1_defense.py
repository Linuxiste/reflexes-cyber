#!/usr/bin/env python3
"""Lot 1 (rubrique Défense) : écrit les 15 modules JSON dans modules/defense/.

Gardé pour mémoire : une fois les modules relus et corrigés à la main dans les JSON,
ne plus relancer ce script (il écraserait les corrections).
"""
import json
from pathlib import Path

H = {"nom": "Cybermalveillance.gouv.fr, fiche réflexe Hameçonnage",
     "url": "https://www.cybermalveillance.gouv.fr/tous-nos-contenus/fiches-reflexes/hameconnage-phishing"}
C7 = {"nom": "Cybermalveillance.gouv.fr, 7 conseils pour éviter les cyberescroqueries",
      "url": "https://www.cybermalveillance.gouv.fr/tous-nos-contenus/actualites/7-conseils-pour-eviter-les-cyberescroqueries"}
M10 = {"nom": "Cybermalveillance.gouv.fr, 10 mesures essentielles",
       "url": "https://www.cybermalveillance.gouv.fr/tous-nos-contenus/bonnes-pratiques/10-mesures-essentielles-assurer-securite-numerique"}
S33 = {"nom": "33700, signalement des SMS et appels indésirables", "url": "https://www.33700.fr/"}
S17 = {"nom": "17Cyber, l'assistance officielle en cas de cyberattaque", "url": "https://www.17cyber.gouv.fr/"}


def ch(*paires):
    return [{"txt": t, "va": v} for t, v in paires]


M = {}

# ---------------------------------------------------------------- Mail d'hameçonnage
M["def-phishing-1"] = dict(theme="Mail d'hameçonnage", titre="Le lien qui se déguise", source=H,
    reflexe="Avant de cliquer, je laisse la souris sur le lien et je lis l'adresse qui s'affiche. Si elle ne correspond pas, je ne clique pas.",
    etapes={
    "debut": {"msg": "Salut, c'est {{perso}} ! Petite question : un mail te dit « Votre colis est bloqué, cliquez ici ». Tu fais quoi ?",
              "choix": ch(("Je clique, j'attends un colis", "clic"), ("Je regarde d'abord le lien", "bravo"))},
    "clic": {"msg": "C'est le piège le plus courant : les escrocs envoient ce mail à des milliers de gens. Forcément, certains attendent un colis !", "va": "astuce"},
    "bravo": {"msg": "Excellent réflexe ! Et tu sais comment voir où mène vraiment un lien ?",
              "choix": ch(("Oui, en survolant", "astuce"), ("Pas vraiment", "astuce"))},
    "astuce": {"msg": "Le texte d'un lien peut dire n'importe quoi. Laisse la souris dessus, sans cliquer : au bout d'une seconde, la vraie adresse s'affiche en bas de l'écran.", "va": "exemple"},
    "exemple": {"msg": "Le texte dit « La Poste », mais l'adresse affichée est 25fjus25g.fr/colis.html ? Ce n'est pas La Poste. Pas besoin d'être expert : il suffit de lire.", "va": "mobile"},
    "mobile": {"msg": "Sur un téléphone, appuie longtemps sur le lien sans relâcher : l'adresse apparaît aussi.", "va": "fin"},
    "fin": {"msg": "Une seconde de survol peut tout changer. À demain pour 2 minutes de plus ! 👋", "fin": True}})

M["def-phishing-2"] = dict(theme="Mail d'hameçonnage", titre="Vrai ou faux ? L'adresse", source=H,
    reflexe="Le vrai nom du site est juste avant le premier « / » et juste avant « .fr » ou « .com ». Tout le reste peut être inventé.",
    etapes={
    "debut": {"msg": "On s'entraîne ! Tu survoles un lien « Votre banque » et tu lis : banque-terranova.fr.securite-client.com/connexion. C'est le site de ta banque ?",
              "choix": ch(("Oui, il y a son nom", "piege"), ("Non, c'est louche", "bravo"))},
    "piege": {"msg": "Bien tenté, mais non ! Le nom de la banque est au début pour te rassurer. Le vrai site, c'est ce qui est juste avant le premier « / ».", "va": "lecture"},
    "bravo": {"msg": "Bien vu ! Tu sais repérer où se cache le vrai nom du site ?",
              "choix": ch(("Juste avant le premier /", "lecture"), ("Au début de l'adresse", "lecture"))},
    "lecture": {"msg": "Ici, juste avant le premier « / », on lit securite-client.com. C'est ce site-là qui reçoit tes informations, pas ta banque.", "va": "deux"},
    "deux": {"msg": "Deuxième essai : terranova.fr/espace-client. Cette fois, le nom juste avant le premier « / » est terranova.fr.",
             "choix": ch(("Ça semble correct", "nuance"), ("Je me méfie quand même", "nuance"))},
    "nuance": {"msg": "C'est plausible. Mais le plus sûr reste de taper toi-même l'adresse de ta banque, ou d'utiliser son appli, plutôt que de suivre un lien reçu.", "va": "fin"},
    "fin": {"msg": "Retenu : le vrai nom est juste avant le premier « / ». Et pour un compte important, je passe par l'appli ou par mes favoris. 👋", "fin": True}})

M["def-phishing-3"] = dict(theme="Mail d'hameçonnage", titre="Quiz éclair : les signaux d'un faux mail", source=H,
    reflexe="Un faux mail cumule souvent : une urgence, une demande inhabituelle, une adresse d'expéditeur bizarre et un lien qui ne mène pas où il dit.",
    etapes={
    "debut": {"msg": "Quiz éclair, 3 questions ! Lequel de ces signaux doit t'alerter dans un mail ?",
              "choix": ch(("Une urgence (« sous 24 h »)", "q1"), ("Un logo officiel", "logo"))},
    "logo": {"msg": "Un logo se copie en deux secondes : il ne prouve rien. En revanche, l'urgence est un signal très fréquent.", "va": "q2"},
    "q1": {"msg": "Exact ! L'urgence sert à t'empêcher de réfléchir.", "va": "q2"},
    "q2": {"msg": "Question 2 : l'expéditeur s'appelle « Service Client », mais l'adresse est service.client.4521@gmail.com. Ça te paraît normal ?",
           "choix": ch(("Oui, c'est le service client", "q2non"), ("Non, une entreprise n'écrit pas depuis Gmail", "q2oui"))},
    "q2non": {"msg": "Le nom affiché se choisit librement. Regarde toujours l'adresse complète, entre les < >.", "va": "q3"},
    "q2oui": {"msg": "Bravo, c'est un très bon indice !", "va": "q3"},
    "q3": {"msg": "Dernière : un mail de ton fournisseur d'énergie te demande ton mot de passe « pour vérification ». Tu réponds ?",
           "choix": ch(("Non, jamais", "fin"), ("Si c'est vraiment lui, oui", "jamais"))},
    "jamais": {"msg": "Aucun service sérieux ne demande ton mot de passe par mail. Jamais.", "va": "fin"},
    "fin": {"msg": "Urgence, expéditeur bizarre, demande inhabituelle : un seul de ces signaux suffit pour ralentir. À demain ! 👋", "fin": True}})

# ---------------------------------------------------------------- L'urgence
M["def-urgence-1"] = dict(theme="L'urgence, levier n° 1", titre="Pourquoi ils sont toujours pressés", source=C7,
    reflexe="Quand un message me presse, je ralentis. L'urgence est l'outil préféré des escrocs.",
    etapes={
    "debut": {"msg": "Dis-moi : « Votre compte sera supprimé dans 2 heures ». Qu'est-ce que tu ressens en lisant ça ?",
              "choix": ch(("Un peu de stress", "stress"), ("Rien, je connais", "connais"))},
    "stress": {"msg": "C'est normal, et c'est exactement le but ! Sous le stress, on agit vite et on vérifie moins.", "va": "pourquoi"},
    "connais": {"msg": "Tant mieux ! Mais même les plus vigilants se font avoir un jour de fatigue. Voyons pourquoi ça marche.", "va": "pourquoi"},
    "pourquoi": {"msg": "Une arnaque a besoin que tu agisses avant de réfléchir. Alors elle invente un délai, une amende, une menace.", "va": "parapente"},
    "parapente": {"msg": "En parapente, on dit : « Quand tout s'accélère, on ralentit ses gestes. » C'est pareil ici.", "va": "geste"},
    "geste": {"msg": "Le bon geste : souffler, fermer le message, et vérifier par un autre chemin. L'appli officielle, le site tapé à la main, un appel.", "va": "fin"},
    "fin": {"msg": "Plus c'est urgent, plus je prends mon temps. À demain ! 👋", "fin": True}})

M["def-urgence-2"] = dict(theme="L'urgence, levier n° 1", titre="Mise en situation : l'amende", source=C7,
    reflexe="Face à une urgence, je vérifie par un autre canal : l'appli officielle, le site que je tape moi-même, ou un appel à un numéro que je connais.",
    etapes={
    "debut": {"msg": "SMS reçu à 18 h : « Amende impayée, majoration de 135 € ce soir. Réglez ici : amendes-gouv-paiement.com ». Tu fais quoi ?",
              "choix": ch(("Je paie vite pour éviter la majoration", "paie"), ("Je vérifie ailleurs", "verifie"))},
    "paie": {"msg": "Aïe, c'est ce que veulent les escrocs ! Tu leur donnerais ta carte bancaire, et souvent bien plus que 35 €.", "va": "indices"},
    "verifie": {"msg": "Parfait ! Et où vérifierais-tu ?",
                "choix": ch(("Sur le site officiel, tapé moi-même", "indices"), ("En cliquant sur le lien pour voir", "lien"))},
    "lien": {"msg": "Le lien, c'est justement la porte d'entrée du piège. On vérifie toujours sans passer par lui.", "va": "indices"},
    "indices": {"msg": "Les indices : l'urgence (« ce soir »), un site qui n'est pas en .gouv.fr, et l'administration ne réclame pas d'amende par SMS avec un lien.", "va": "geste"},
    "geste": {"msg": "Tu peux transférer ce SMS au 33700 : c'est le numéro gratuit pour signaler les SMS frauduleux.", "va": "fin"},
    "fin": {"msg": "Une urgence ? Je vérifie par un autre chemin, jamais par le lien reçu. À demain ! 👋", "fin": True}})

M["def-urgence-3"] = dict(theme="L'urgence, levier n° 1", titre="Quiz : urgent ou arnaque ?", source=C7,
    reflexe="Un vrai interlocuteur accepte toujours que je prenne le temps de vérifier. Celui qui refuse que je raccroche est suspect.",
    etapes={
    "debut": {"msg": "Quiz rapide ! Un « technicien » t'appelle : « Votre ordinateur est infecté, laissez-moi en prendre le contrôle tout de suite. » Arnaque ?",
              "choix": ch(("Oui, arnaque", "q1oui"), ("Peut-être vrai", "q1non"))},
    "q1oui": {"msg": "Exact : aucun éditeur n'appelle spontanément pour réparer ton ordinateur.", "va": "q2"},
    "q1non": {"msg": "C'est l'arnaque au faux support technique. Personne n'appelle spontanément pour réparer ton ordinateur.", "va": "q2"},
    "q2": {"msg": "Question 2 : tu dis « Je vous rappelle dans 5 minutes », et ton interlocuteur insiste pour que tu restes en ligne. Mauvais signe ?",
           "choix": ch(("Oui", "q2oui"), ("Non, il veut aider", "q2non"))},
    "q2oui": {"msg": "Bien vu ! Une personne honnête te laisse vérifier.", "va": "q3"},
    "q2non": {"msg": "Une personne honnête te laisse toujours raccrocher et vérifier. L'insistance est un signal fort.", "va": "q3"},
    "q3": {"msg": "Et si tu as un doute au travail, tu préviens qui ?",
           "choix": ch(("{{org.contact}}", "fin"), ("Personne, je gère seul", "seul"))},
    "seul": {"msg": "Tu n'as pas à gérer seul : {{org.contact}} est là pour ça, {{org.contact_detail}}.", "va": "fin"},
    "fin": {"msg": "Le bon réflexe : je raccroche, je vérifie, et je n'hésite pas à demander. À demain ! 👋", "fin": True}})

# ---------------------------------------------------------------- SMS, QR codes, appels
M["def-sms-1"] = dict(theme="SMS, QR codes et appels", titre="Le colis qui n'existe pas", source=S33,
    reflexe="Je ne suis jamais un lien reçu par SMS pour un colis, une amende ou un remboursement. Je vérifie dans l'appli officielle.",
    etapes={
    "debut": {"msg": "« Votre colis n'a pas pu être livré. Frais de réexpédition : 1,99 €. » Ça te dit quelque chose ?",
              "choix": ch(("Oui, je l'ai déjà reçu", "deja"), ("Non, jamais", "jamais"))},
    "deja": {"msg": "Tu n'es pas le seul : c'est l'un des SMS frauduleux les plus envoyés en France.", "va": "piege"},
    "jamais": {"msg": "Ça viendra sûrement ! C'est l'un des SMS frauduleux les plus envoyés en France.", "va": "piege"},
    "piege": {"msg": "Le piège, ce n'est pas 1,99 €. C'est ta carte bancaire : une fois saisie, elle peut servir à des achats bien plus gros.", "va": "verif"},
    "verif": {"msg": "Tu attends vraiment un colis ? Ouvre l'appli ou le site du transporteur toi-même, avec ton numéro de suivi.", "va": "signal"},
    "signal": {"msg": "Et transfère le SMS au 33700. C'est gratuit, et ça aide à bloquer ces numéros.", "va": "fin"},
    "fin": {"msg": "Un SMS avec un lien et un petit paiement ? Je vérifie ailleurs et je signale au 33700. À demain ! 👋", "fin": True}})

M["def-sms-2"] = dict(theme="SMS, QR codes et appels", titre="Le QR code collé sur l'horodateur", source=C7,
    reflexe="Un QR code est un lien caché. Avant de payer, je regarde l'adresse qui s'affiche après le scan, et je préfère l'appli officielle.",
    etapes={
    "debut": {"msg": "Tu te gares. Sur l'horodateur, un autocollant : « Payez plus vite, scannez-moi ». Tu scannes ?",
              "choix": ch(("Oui, c'est pratique", "scan"), ("Je me méfie", "mefie"))},
    "scan": {"msg": "C'est pratique… pour les escrocs aussi ! Il leur suffit de coller leur propre QR code par-dessus le vrai.", "va": "cache"},
    "mefie": {"msg": "Tu as raison ! Tu sais pourquoi ?",
              "choix": ch(("On ne voit pas où il mène", "cache"), ("Pas vraiment", "cache"))},
    "cache": {"msg": "Un QR code, c'est un lien qu'on ne peut pas lire à l'œil. On ne voit l'adresse qu'après l'avoir scanné.", "va": "geste"},
    "geste": {"msg": "Le réflexe : après le scan, ton téléphone affiche l'adresse avant de l'ouvrir. Lis-la. Un autocollant par-dessus l'affiche ? Méfiance.", "va": "mieux"},
    "mieux": {"msg": "Pour payer, le plus sûr reste l'appli officielle de la ville ou du parking, que tu installes toi-même.", "va": "fin"},
    "fin": {"msg": "Un QR code, c'est un lien caché : je lis l'adresse avant d'ouvrir. À demain ! 👋", "fin": True}})

M["def-sms-3"] = dict(theme="SMS, QR codes et appels", titre="Le faux conseiller bancaire", source=C7,
    reflexe="Ma banque ne me demande jamais un code reçu par SMS ni de valider une opération au téléphone. Je raccroche et je rappelle le numéro de ma carte.",
    etapes={
    "debut": {"msg": "Le téléphone sonne. « Bonjour, service fraude de votre banque. Une opération suspecte est en cours. » La personne connaît ton nom. Tu la crois ?",
              "choix": ch(("Oui, elle connaît mon nom", "nom"), ("Je reste prudent", "prudent"))},
    "nom": {"msg": "Ton nom, et parfois ton adresse, se trouvent facilement après une fuite de données. Ça ne prouve rien.", "va": "code"},
    "prudent": {"msg": "Bon réflexe. Écoute la suite…", "va": "code"},
    "code": {"msg": "« Pour bloquer l'opération, donnez-moi le code que vous allez recevoir par SMS. »",
             "choix": ch(("Je le donne, c'est pour bloquer", "donne"), ("Je refuse", "refuse"))},
    "donne": {"msg": "C'est le piège ! Ce code sert à valider un paiement ou un nouvel appareil… au profit de l'escroc.", "va": "geste"},
    "refuse": {"msg": "Exactement : un code reçu par SMS ne se donne à personne, même pas à ta banque.", "va": "geste"},
    "geste": {"msg": "Le bon geste : raccrocher, puis appeler toi-même le numéro au dos de ta carte bancaire.", "va": "fin"},
    "fin": {"msg": "Un code SMS ne se donne jamais. Je raccroche et je rappelle le numéro que je connais. À demain ! 👋", "fin": True}})

# ---------------------------------------------------------------- Fraude au président ou au trésorier
M["def-president-1"] = dict(theme="Fraude au président ou au trésorier", titre="Le virement très discret", source=C7,
    reflexe="Une demande de virement urgente et confidentielle par mail ? Je rappelle la personne sur son numéro habituel avant de faire quoi que ce soit.",
    etapes={
    "debut": {"msg": "Mail de {{org.presidence}} : « Je suis en réunion, peux-tu faire un virement urgent à ce fournisseur ? C'est confidentiel, n'en parle à personne. » Tu fais quoi ?",
              "choix": ch(("Je fais le virement, c'est la direction", "vire"), ("Je trouve ça bizarre", "bizarre"))},
    "vire": {"msg": "C'est exactement ce que l'escroc espère ! Cette arnaque s'appelle la « fraude au président ».", "va": "indices"},
    "bizarre": {"msg": "Tu as raison ! Qu'est-ce qui cloche, selon toi ?",
                "choix": ch(("L'urgence", "indices"), ("Le secret", "indices"))},
    "indices": {"msg": "Les deux ! L'urgence t'empêche de réfléchir, et le secret t'empêche de demander conseil. Ce sont les deux signaux de cette arnaque.", "va": "adresse"},
    "adresse": {"msg": "Souvent, l'adresse de l'expéditeur ressemble à la vraie, à une lettre près. Et si sa messagerie a été piratée, elle peut même être la vraie.", "va": "geste"},
    "geste": {"msg": "Le bon geste : appeler la personne sur le numéro que tu connais déjà. Jamais celui donné dans le mail.", "va": "fin"},
    "fin": {"msg": "Urgent et secret, c'est le signal d'alarme. Je rappelle avant de virer. Personne ne te reprochera d'avoir vérifié. À demain ! 👋", "fin": True}})

M["def-president-2"] = dict(theme="Fraude au président ou au trésorier", titre="Le RIB qui change", source=C7,
    reflexe="Un fournisseur m'annonce un changement de RIB par mail ? Je vérifie par téléphone, avec un numéro que j'avais déjà.",
    etapes={
    "debut": {"msg": "Mail d'un fournisseur habituel : « Nous changeons de banque, voici notre nouveau RIB pour la prochaine facture. » Tu mets à jour ?",
              "choix": ch(("Oui, c'est un fournisseur connu", "oui"), ("Je vérifie d'abord", "verifie"))},
    "oui": {"msg": "C'est le piège du faux RIB : l'escroc se fait passer pour le fournisseur, et la prochaine facture part sur son compte.", "va": "comment"},
    "verifie": {"msg": "Très bon réflexe ! Tu vérifies comment ?",
                "choix": ch(("Je réponds au mail", "repond"), ("J'appelle le numéro que je connais", "comment"))},
    "repond": {"msg": "Si la messagerie du fournisseur est piratée, c'est l'escroc qui te répondra « oui, c'est bien nous » !", "va": "comment"},
    "comment": {"msg": "La seule vérification fiable : appeler le fournisseur sur un numéro que tu avais avant ce mail. Celui de tes anciennes factures, par exemple.", "va": "regle"},
    "regle": {"msg": "Avec {{org.tresorier}}, vous pouvez fixer une règle simple : aucun changement de RIB sans appel de vérification.", "va": "fin"},
    "fin": {"msg": "Nouveau RIB par mail ? J'appelle d'abord, avec un numéro que j'avais déjà. À demain ! 👋", "fin": True}})

M["def-president-3"] = dict(theme="Fraude au président ou au trésorier", titre="Quiz : les bons réflexes avant un virement", source=C7,
    reflexe="Pour tout virement inhabituel : je ralentis, je vérifie par un autre canal, et j'en parle à quelqu'un. Le secret est un signal d'alarme.",
    etapes={
    "debut": {"msg": "Quiz ! Une demande de virement arrive par mail, avec la signature de {{org.presidence}}. La signature prouve que c'est lui ?",
              "choix": ch(("Oui", "q1non"), ("Non", "q1oui"))},
    "q1non": {"msg": "Une signature se copie en un clin d'œil. Elle ne prouve rien.", "va": "q2"},
    "q1oui": {"msg": "Exact : une signature se copie facilement.", "va": "q2"},
    "q2": {"msg": "Question 2 : on te demande de ne parler de ce virement à personne. C'est…",
           "choix": ch(("Normal si c'est confidentiel", "q2non"), ("Un signal d'alarme", "q2oui"))},
    "q2non": {"msg": "C'est le signal n° 1 de la fraude au président. Le secret sert à t'isoler.", "va": "q3"},
    "q2oui": {"msg": "Bravo ! Le secret sert à t'isoler.", "va": "q3"},
    "q3": {"msg": "Dernière : tu as un doute, mais tu as peur de déranger. Tu fais quoi ?",
           "choix": ch(("J'appelle quand même pour vérifier", "fin"), ("Je fais le virement pour ne pas déranger", "deranger"))},
    "deranger": {"msg": "Mieux vaut un appel de 30 secondes qu'un virement perdu. Un dirigeant préfère toujours qu'on vérifie.", "va": "fin"},
    "fin": {"msg": "Ralentir, vérifier par un autre canal, en parler : les 3 réflexes avant un virement inhabituel. À demain ! 👋", "fin": True}})

# ---------------------------------------------------------------- Signaler
M["def-signaler-1"] = dict(theme="Signaler", titre="J'ai cliqué… et maintenant ?", source=S17,
    reflexe="J'ai cliqué ou j'ai un doute ? Je préviens tout de suite. Plus on signale tôt, plus c'est facile à réparer, et on ne sera pas puni.",
    etapes={
    "debut": {"msg": "Imagine : tu viens de cliquer sur un lien, et tu réalises que c'était sûrement un piège. Tu ressens quoi ?",
              "choix": ch(("De la honte", "honte"), ("De la panique", "panique"))},
    "honte": {"msg": "C'est très humain, mais il n'y a aucune honte à avoir. Ces pièges sont faits par des professionnels, et tout le monde peut se faire avoir.", "va": "important"},
    "panique": {"msg": "Respire : la plupart du temps, ça se rattrape très bien, surtout si on agit vite.", "va": "important"},
    "important": {"msg": "Le plus important n'est pas d'avoir cliqué. C'est ce que tu fais dans les minutes qui suivent.", "va": "qui"},
    "qui": {"msg": "Préviens tout de suite {{org.contact}}, {{org.contact_detail}}. Dis simplement ce qui s'est passé.", "va": "mdp"},
    "mdp": {"msg": "Si tu as saisi un mot de passe, change-le au plus vite, depuis un autre appareil si possible.", "va": "fin"},
    "fin": {"msg": "Cliquer, ça arrive. Le vrai réflexe, c'est prévenir vite. Merci à ceux qui signalent : ils protègent tout le monde. 👋", "fin": True}})

M["def-signaler-2"] = dict(theme="Signaler", titre="Mise en situation : l'ordinateur bizarre", source=S17,
    reflexe="Un comportement anormal sur mon poste (fichiers bizarres, message de rançon) : je débranche le réseau, je ne touche plus à rien, et je préviens.",
    etapes={
    "debut": {"msg": "Lundi matin, tes fichiers ont des noms étranges, et un message réclame de l'argent pour les « libérer ». Premier réflexe ?",
              "choix": ch(("J'éteins et je rallume", "eteins"), ("Je débranche le réseau", "debranche"))},
    "eteins": {"msg": "Mauvaise idée : éteindre peut effacer des traces utiles. Mieux vaut débrancher le câble réseau ou couper le Wi-Fi.", "va": "pourquoi"},
    "debranche": {"msg": "Parfait ! Tu sais pourquoi ?",
                  "choix": ch(("Pour que ça ne se propage pas", "pourquoi"), ("Pas vraiment", "pourquoi"))},
    "pourquoi": {"msg": "Un rançongiciel cherche à se propager aux autres ordinateurs et au serveur. Le couper du réseau limite les dégâts.", "va": "payer"},
    "payer": {"msg": "Et surtout, on ne paie pas : rien ne garantit que les fichiers seront rendus.", "va": "prevenir"},
    "prevenir": {"msg": "Ensuite, préviens {{org.contact}} tout de suite. En dehors du travail, le site 17Cyber.gouv.fr te guide pas à pas.", "va": "fin"},
    "fin": {"msg": "Débrancher, ne rien toucher, prévenir. Trois gestes simples qui sauvent beaucoup. À demain ! 👋", "fin": True}})

M["def-signaler-3"] = dict(theme="Signaler", titre="Quiz : à qui je signale ?", source=M10,
    reflexe="Au travail, je signale à {{org.contact}}. Un SMS frauduleux : au 33700. Un mail frauduleux : sur signal-spam.fr. Une attaque : 17Cyber.",
    etapes={
    "debut": {"msg": "Dernier quiz de la série Défense ! Un mail douteux arrive sur ta boîte de travail. Tu fais quoi ?",
              "choix": ch(("Je le supprime en silence", "q1non"), ("Je le signale", "q1oui"))},
    "q1non": {"msg": "Le supprimer te protège toi. Le signaler protège aussi tes collègues, qui l'ont peut-être reçu.", "va": "q2"},
    "q1oui": {"msg": "Super : tes collègues l'ont peut-être reçu aussi !", "va": "q2"},
    "q2": {"msg": "Question 2 : un SMS frauduleux sur ton téléphone. Tu le transfères à quel numéro ?",
           "choix": ch(("Le 33700", "q2oui"), ("Le 17", "q2non"))},
    "q2oui": {"msg": "Bravo, le 33700, gratuit.", "va": "q3"},
    "q2non": {"msg": "Le 17, c'est la police pour une urgence. Pour un SMS frauduleux, c'est le 33700.", "va": "q3"},
    "q3": {"msg": "Et pour un mail frauduleux sur ta boîte personnelle ?",
           "choix": ch(("signal-spam.fr", "fin"), ("Je réponds à l'escroc", "repond"))},
    "repond": {"msg": "Surtout pas : répondre lui confirme que ton adresse est active. On signale sur signal-spam.fr.", "va": "fin"},
    "fin": {"msg": "Signaler, c'est protéger tout le monde. Bravo, tu as fini la série Défense ! 👋", "fin": True}})


def main():
    d = Path(__file__).resolve().parent.parent / "modules" / "defense"
    d.mkdir(parents=True, exist_ok=True)
    for i, (mid, m) in enumerate(M.items()):
        doc = {"id": mid, "rubrique": "Défense", "theme": m["theme"], "titre": m["titre"],
               "reflexe": m["reflexe"], "source": m["source"], "statut": "brouillon", "etapes": m["etapes"]}
        (d / f"{mid}.json").write_text(json.dumps(doc, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
    print(f"{len(M)} modules écrits dans {d}")


if __name__ == "__main__":
    main()
