#!/usr/bin/env python3
"""Construit le site « Réflexes cyber » pour une structure, après contrôle de chaque module.

    python3 outils/construire.py --organisation exemple          # → dist/exemple/
    python3 outils/construire.py --organisation exemple --verifier  # contrôle seulement

Sources :
- modules/<rubrique>/*.json : modules communs (publics) ;
- scenarios/*.json : pages d'entraînement au phishing (« Tu t'es fait prendre… ») ;
- organisations/<nom>/config.json : personnalisation (nom, contacts, réseaux Wi-Fi…) ;
- organisations/<nom>/modules/*.json : modules propres à la structure (PRIVÉS, jamais dans le dépôt public).

Dans les textes, {{org.cle}} est remplacé par la valeur de config.json (clé « org »),
{{perso}} par le nom du personnage. Une variable inconnue bloque la construction.

Règles d'un module (refus sinon) : id = nom du fichier ; titre, reflexe, rubrique, theme,
source {nom, url https} ; étape « debut » ; chaque « va » mène à une étape existante ;
toutes les étapes sont atteignables ; aucun parcours ne boucle ; chaque parcours compte
au plus 10 messages du personnage, et le plus long au moins 6 ; 280 mots au plus sur
le parcours le plus long (environ 2 minutes de lecture et de réponses).
"""
from __future__ import annotations

import argparse
import html
import json
import re
import shutil
import sqlite3
import sys
from pathlib import Path

RACINE = Path(__file__).resolve().parent.parent
MAX_MESSAGES, MIN_MESSAGES, MAX_MOTS = 10, 6, 280
VARIABLE = re.compile(r"\{\{\s*([a-z_.]+)\s*\}\}")


class Refus(Exception):
    pass


def remplacer(texte: str, valeurs: dict, ou: str) -> str:
    def un(m):
        cle = m.group(1)
        if cle not in valeurs:
            raise Refus(f"{ou} : variable inconnue {{{{{cle}}}}} (à définir dans config.json)")
        return str(valeurs[cle])
    return VARIABLE.sub(un, texte)


def substituer(objet, valeurs: dict, ou: str):
    if isinstance(objet, str):
        return remplacer(objet, valeurs, ou)
    if isinstance(objet, list):
        return [substituer(x, valeurs, ou) for x in objet]
    if isinstance(objet, dict):
        return {k: substituer(v, valeurs, ou) for k, v in objet.items()}
    return objet


def parcours(etapes: dict, cle: str, chemin: tuple) -> list[tuple]:
    if cle in chemin:
        raise Refus(f"boucle : {' → '.join(chemin + (cle,))}")
    e = etapes[cle]
    chemin = chemin + (cle,)
    if e.get("fin"):
        return [chemin]
    suites = [c["va"] for c in e["choix"]] if e.get("choix") else [e["va"]]
    return [p for s in suites for p in parcours(etapes, s, chemin)]


def mots(texte: str) -> int:
    return len(re.findall(r"\w+", texte))


def controler(m: dict, fichier: Path, metiers_connus: set) -> dict:
    ou = str(fichier.relative_to(RACINE))
    for champ in ("metiers", "prioritaire_pour"):
        inconnus = set(m.get(champ, [])) - metiers_connus
        if inconnus:
            raise Refus(f"{ou} : métier(s) inconnu(s) dans « {champ} » : {', '.join(sorted(inconnus))} (voir metiers.json)")
    for champ in ("id", "titre", "reflexe", "rubrique", "theme", "source", "etapes"):
        if not m.get(champ):
            raise Refus(f"{ou} : champ « {champ} » manquant")
    if m["id"] != fichier.stem:
        raise Refus(f"{ou} : l'id « {m['id']} » doit être le nom du fichier")
    if not str(m["source"].get("url", "")).startswith("https://") or not m["source"].get("nom"):
        raise Refus(f"{ou} : source incomplète (nom et url https)")
    etapes = m["etapes"]
    if "debut" not in etapes:
        raise Refus(f"{ou} : étape « debut » manquante")
    for cle, e in etapes.items():
        if not e.get("msg"):
            raise Refus(f"{ou} : étape « {cle} » sans message")
        suites = [c.get("va") for c in e.get("choix", [])] if e.get("choix") else ([] if e.get("fin") else [e.get("va")])
        if not e.get("fin") and not suites:
            raise Refus(f"{ou} : étape « {cle} » sans suite (va, choix ou fin)")
        for s in suites:
            if s not in etapes:
                raise Refus(f"{ou} : étape « {cle} » mène à « {s} », qui n'existe pas")
        for c in e.get("choix", []):
            if not c.get("txt"):
                raise Refus(f"{ou} : un choix de l'étape « {cle} » n'a pas de texte")
    try:
        chemins = parcours(etapes, "debut", ())
    except Refus as e:
        raise Refus(f"{ou} : {e}") from None
    vues = {c for p in chemins for c in p}
    if set(etapes) - vues:
        raise Refus(f"{ou} : étapes jamais atteintes : {', '.join(sorted(set(etapes) - vues))}")
    longueurs = [len(p) for p in chemins]
    if max(longueurs) > MAX_MESSAGES:
        raise Refus(f"{ou} : un parcours compte {max(longueurs)} messages (maximum {MAX_MESSAGES})")
    if max(longueurs) < MIN_MESSAGES:
        raise Refus(f"{ou} : le parcours le plus long ne compte que {max(longueurs)} messages (minimum {MIN_MESSAGES})")
    def total(p):
        n = 0
        for i, cle in enumerate(p):
            n += mots(etapes[cle]["msg"])
            if etapes[cle].get("choix") and i + 1 < len(p):
                n += max(mots(c["txt"]) for c in etapes[cle]["choix"])
        return n
    plus_long = max(total(p) for p in chemins)
    if plus_long > MAX_MOTS:
        raise Refus(f"{ou} : {plus_long} mots sur le parcours le plus long (maximum {MAX_MOTS})")
    return {"messages_max": max(longueurs), "mots_max": plus_long, "parcours": len(chemins)}


GABARIT = """<!doctype html>
<html lang="fr">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <meta name="robots" content="noindex">
  <title>Entraînement · {nom}</title>
  <link rel="stylesheet" href="../../assets/style.css">
</head>
<body>
  <main class="page">
    <div class="panneau" role="alert">
      <p class="gros">⚠️ Tu t'es fait prendre…</p>
      <p><strong>Mais rien de grave :</strong> c'était un petit entraînement organisé par {org_nom}.
      Aucune donnée n'a été enregistrée, et personne ne sait que c'est toi.</p>
    </div>
    <h1>{titre}</h1>
    <p>{accroche}</p>
    <section class="conseils" aria-label="Les bons réflexes">
      <h2>Les bons réflexes</h2>
      <ul>
{conseils}
      </ul>
      <p class="source">Ces réflexes suivent les recommandations de l'ANSSI : <a href="https://messervices.cyber.gouv.fr/guides" rel="noopener" target="_blank">ses guides</a> et <a href="https://messervices.cyber.gouv.fr/guides/fiches-pratiques-recyf" rel="noopener" target="_blank">les fiches pratiques ReCyF</a>.</p>
    </section>
    <div class="actions">
      <a class="bouton plein" href="../../module.html?m={module}">Le module de 2 minutes sur ce piège</a>
      <a class="bouton" href="../../">Tous les modules</a>
    </div>
    <footer>{pied}</footer>
  </main>
</body>
</html>
"""


def ecrire_base(org, config, metiers, modules, scenarios) -> Path:
    """Base SQLite (index) : métiers, modules, rattachements, sources, pages d'entraînement.

    Les JSON restent la source (relus dans git) ; la base est régénérée à chaque construction.
    Elle sert à l'agent de création (thèmes déjà couverts, sources, péremption) et aux bilans.
    """
    f = RACINE / "dist" / f"reflexes-{org}.sqlite"
    f.unlink(missing_ok=True)
    cx = sqlite3.connect(f)
    cx.executescript("""
    CREATE TABLE metier (id TEXT PRIMARY KEY, nom TEXT NOT NULL, description TEXT);
    CREATE TABLE module (id TEXT PRIMARY KEY, rubrique TEXT NOT NULL, theme TEXT NOT NULL, titre TEXT NOT NULL,
                         reflexe TEXT NOT NULL, source_nom TEXT NOT NULL, source_url TEXT NOT NULL,
                         statut TEXT NOT NULL DEFAULT 'brouillon', format TEXT NOT NULL DEFAULT 'base',
                         organisation TEXT, perime_le TEXT, messages_max INTEGER, mots_max INTEGER, fichier TEXT);
    CREATE TABLE module_metier (module TEXT REFERENCES module(id), metier TEXT REFERENCES metier(id),
                                prioritaire INTEGER NOT NULL DEFAULT 0, PRIMARY KEY (module, metier));
    CREATE TABLE scenario (slug TEXT PRIMARY KEY, titre TEXT NOT NULL, module TEXT REFERENCES module(id));
    CREATE VIEW parcours_metier AS
      SELECT me.nom AS metier, mo.rubrique, mo.theme, mo.titre, mm.prioritaire
      FROM module_metier mm JOIN metier me ON me.id = mm.metier JOIN module mo ON mo.id = mm.module
      ORDER BY me.nom, mm.prioritaire DESC, mo.rubrique, mo.id;
    """)
    cx.executemany("INSERT INTO metier VALUES (?,?,?)", [(x["id"], x["nom"], x.get("description")) for x in metiers])
    for fichier, m, st in modules:
        cx.execute("INSERT INTO module VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?)",
                   (m["id"], m["rubrique"], m["theme"], m["titre"], m["reflexe"], m["source"]["nom"], m["source"]["url"],
                    m.get("statut", "brouillon"), m.get("format", "base"), m.get("organisation"), m.get("perime_le"),
                    st["messages_max"], st["mots_max"], str(fichier.relative_to(RACINE))))
        cibles = {x["id"] for x in metiers} if "tous" in m["metiers"] else set(m["metiers"]) | {"tous"}
        for me in sorted(cibles | set(m["prioritaire_pour"])):
            cx.execute("INSERT INTO module_metier VALUES (?,?,?)", (m["id"], me, int(me in m["prioritaire_pour"])))
    cx.executemany("INSERT INTO scenario VALUES (?,?,?)", [(s["slug"], s["titre"], s["module"]) for s in scenarios])
    cx.commit()
    cx.close()
    return f


def construire(org: str, verifier: bool) -> int:
    dossier_org = RACINE / "organisations" / org
    config = json.loads((dossier_org / "config.json").read_text(encoding="utf-8"))
    valeurs = {f"org.{k}": v for k, v in config["org"].items()}
    valeurs["perso"] = config["personnage"]["nom"]
    tous_metiers = json.loads((RACINE / "metiers.json").read_text(encoding="utf-8"))["metiers"]
    garder = config.get("metiers")
    metiers = [x for x in tous_metiers if not garder or x["id"] in garder or x["id"] == "tous"]
    metiers_ids = {x["id"] for x in tous_metiers}
    fichiers = sorted((RACINE / "modules").rglob("*.json")) + sorted((dossier_org / "modules").glob("*.json"))
    modules, erreurs = [], []
    for f in fichiers:
        try:
            m = json.loads(f.read_text(encoding="utf-8"))
            if m.get("organisation") and m["organisation"] != org:
                continue
            m = substituer(m, valeurs, str(f.relative_to(RACINE)))
            m.setdefault("metiers", ["tous"]); m.setdefault("prioritaire_pour", [])
            stats = controler(m, f, metiers_ids)
            modules.append((f, m, stats))
        except (Refus, json.JSONDecodeError, KeyError) as e:
            erreurs.append(str(e))
    scenarios = []
    for f in sorted((RACINE / "scenarios").glob("*.json")):
        try:
            brut = json.loads(f.read_text(encoding="utf-8"))
            brut.pop("message", None)        # faux message : traité par outils/kit_campagne.py, pas publié sur le site
            s = substituer(brut, valeurs, str(f.relative_to(RACINE)))
            if s["slug"] != f.stem:
                raise Refus(f"{f.name} : slug différent du nom du fichier")
            if s["module"] not in {m["id"] for _, m, _ in modules}:
                raise Refus(f"{f.name} : module lié « {s['module']} » introuvable")
            scenarios.append(s)
        except (Refus, json.JSONDecodeError, KeyError) as e:
            erreurs.append(str(e))
    ids = [m["id"] for _, m, _ in modules]
    if len(ids) != len(set(ids)):
        erreurs.append("deux modules portent le même id")
    for _, m, st in modules:
        print(f"  ok  {m['id']:<28} {st['messages_max']:>2} messages max · {st['mots_max']:>3} mots · {st['parcours']} parcours")
    for s in scenarios:
        print(f"  ok  entrainement/{s['slug']}/")
    if erreurs:
        print("\nREFUS :", *erreurs, sep="\n  - ", file=sys.stderr)
        return 1
    print(f"\n{len(modules)} module(s) et {len(scenarios)} page(s) d'entraînement valides.")
    if verifier:
        return 0

    ordre = config["rubriques"]
    modules.sort(key=lambda x: (ordre.index(x[1]["rubrique"]) if x[1]["rubrique"] in ordre else 99, x[0].name))
    sortie = RACINE / "dist" / org
    if sortie.exists():
        shutil.rmtree(sortie)
    shutil.copytree(RACINE / "site", sortie)
    (sortie / "modules").mkdir()
    for _, m, _ in modules:
        (sortie / "modules" / f"{m['id']}.json").write_text(json.dumps(m, ensure_ascii=False), encoding="utf-8")
    catalogue = {
        "nom": config["nom_site"], "slogan": config["slogan"], "personnage": config["personnage"],
        "rubriques": ordre, "pied": remplacer(config["pied"], valeurs, "config.json"),
        "metiers": [{"id": x["id"], "nom": x["nom"]} for x in metiers],
        "modules": [{"id": m["id"], "titre": m["titre"], "rubrique": m["rubrique"], "theme": m["theme"],
                     "metiers": m["metiers"], "prioritaire_pour": m["prioritaire_pour"]} for _, m, _ in modules],
    }
    (sortie / "catalogue.json").write_text(json.dumps(catalogue, ensure_ascii=False, indent=1), encoding="utf-8")
    e = html.escape
    for s in scenarios:
        d = sortie / "entrainement" / s["slug"]
        d.mkdir(parents=True)
        conseils = "\n".join(f"        <li>{c}</li>" for c in s["conseils"])   # HTML simple autorisé (écrit par nous)
        (d / "index.html").write_text(GABARIT.format(
            nom=e(config["nom_site"]), org_nom=e(config["org"]["nom"]), titre=e(s["titre"]),
            accroche=e(s["accroche"]), conseils=conseils, module=e(s["module"]), pied=e(catalogue["pied"])), encoding="utf-8")
    base = ecrire_base(org, config, tous_metiers, modules, scenarios)
    print(f"Site construit dans {sortie.relative_to(RACINE)}/ ; base de données : {base.relative_to(RACINE)}")
    return 0


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--organisation", default="exemple")
    ap.add_argument("--verifier", action="store_true")
    a = ap.parse_args()
    sys.exit(construire(a.organisation, a.verifier))
