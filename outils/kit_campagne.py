#!/usr/bin/env python3
"""Prépare le kit d'une campagne d'entraînement et vérifie où mène chaque faux message.

    python3 outils/kit_campagne.py --organisation exemple --adresse http://localhost:8000

Produit dist/kit-<organisation>/ (jamais publié sur le site) :
- apercu.html : une fausse boîte de réception avec les 6 messages et leurs liens cliquables ;
- <scénario>.eml : chaque faux mail, à ouvrir dans Thunderbird (double-clic) pour le voir
  comme un vrai mail, ou à envoyer à une boîte de test ;
- sms-<scénario>.txt : le texte du faux SMS, à envoyer depuis un téléphone de test ;
- qr-<scénario>.png : le QR code à imprimer (si la commande « qrencode » est installée) ;
- verification.txt : pour chaque message, l'adresse du lien et la réponse du serveur.

Le contrôle échoue (code 1) si un lien ne mène pas à une page d'entraînement qui répond 200,
ou si la page reçue n'est pas une page « Tu t'es fait prendre ».
"""
from __future__ import annotations

import argparse
import html
import json
import re
import shutil
import subprocess
import sys
import urllib.request
from email.message import EmailMessage
from email.utils import formatdate, make_msgid
from pathlib import Path

RACINE = Path(__file__).resolve().parent.parent
VARIABLE = re.compile(r"\{\{\s*([a-z_.]+)\s*\}\}")
LIEN_MD = re.compile(r"\[([^\]]+)\]\(([^)]+)\)")


def remplacer(texte: str, valeurs: dict) -> str:
    return VARIABLE.sub(lambda m: str(valeurs.get(m.group(1), m.group(0))), texte)


def corps_html(texte: str) -> str:
    """Markdown minimal du modèle → HTML de mail (paragraphes et liens [texte](url))."""
    paras = []
    for p in texte.split("\n\n"):
        p = html.escape(p)
        p = LIEN_MD.sub(lambda m: f'<a href="{m.group(2)}" style="background:#1f6feb;color:#fff;padding:8px 14px;'
                                  f'border-radius:6px;text-decoration:none">{m.group(1)}</a>', p)
        paras.append("<p>" + p.replace("\n", "<br>") + "</p>")
    return "\n".join(paras)


def corps_texte(texte: str) -> str:
    return LIEN_MD.sub(lambda m: f"{m.group(1)} : {m.group(2)}", texte)


def verifier(url: str) -> tuple[int | str, bool]:
    try:
        with urllib.request.urlopen(urllib.request.Request(url, headers={"User-Agent": "kit-campagne"}), timeout=10) as r:
            page = r.read().decode("utf-8", "replace")
            return r.status, "Tu t'es fait prendre" in page
    except Exception as e:  # serveur arrêté, mauvaise adresse…
        return f"erreur ({e.__class__.__name__})", False


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--organisation", default="exemple")
    ap.add_argument("--adresse", default="http://localhost:8000", help="adresse du site, sans / final")
    ap.add_argument("--sans-verification", action="store_true")
    a = ap.parse_args()
    base = a.adresse.rstrip("/")
    config = json.loads((RACINE / "organisations" / a.organisation / "config.json").read_text(encoding="utf-8"))
    valeurs = {f"org.{k}": v for k, v in config["org"].items()}
    sortie = RACINE / "dist" / f"kit-{a.organisation}"
    if sortie.exists():
        shutil.rmtree(sortie)
    sortie.mkdir(parents=True)
    qr = shutil.which("qrencode")
    lignes, cartes, echecs = [], [], 0
    for f in sorted((RACINE / "scenarios").glob("*.json")):
        s = json.loads(f.read_text(encoding="utf-8"))
        m = s.get("message")
        if not m:
            continue
        lien = f"{base}/entrainement/{s['slug']}/"
        v = dict(valeurs, lien=lien)
        corps, exp, objet = remplacer(m["corps"], v), remplacer(m["expediteur"], v), remplacer(m["objet"], v)
        if m["canal"] == "mail":
            e = EmailMessage()
            e["From"], e["To"], e["Subject"] = exp, "Boîte de test <test@exemple.invalid>", objet
            e["Date"], e["Message-ID"] = formatdate(localtime=True), make_msgid("entrainement", domain="reflexes-cyber.invalid")
            e["X-Entrainement"] = "Faux message d'entraînement (Réflexes cyber), aucune donnée collectée"
            e.set_content(corps_texte(corps))
            e.add_alternative(f"<html><body style=\"font-family:sans-serif\">{corps_html(corps)}</body></html>", subtype="html")
            (sortie / f"{s['slug']}.eml").write_bytes(bytes(e))
            fichier = f"{s['slug']}.eml"
        elif m["canal"] == "sms":
            (sortie / f"sms-{s['slug']}.txt").write_text(corps_texte(corps) + "\n", encoding="utf-8")
            fichier = f"sms-{s['slug']}.txt"
        else:
            fichier = "(QR code : installer qrencode)"
            if qr:
                subprocess.run([qr, "-s", "8", "-o", str(sortie / f"qr-{s['slug']}.png"), lien], check=True)
                fichier = f"qr-{s['slug']}.png"
        statut, bonne_page = ("non vérifié", False) if a.sans_verification else verifier(lien)
        ok = statut == 200 and bonne_page
        echecs += 0 if (ok or a.sans_verification) else 1
        etat = "OK" if ok else ("non vérifié" if a.sans_verification else "ÉCHEC")
        lignes.append(f"{etat:<11} {m['canal']:<5} {s['slug']:<13} {lien}  → {statut}{'' if bonne_page or a.sans_verification else ' (pas la page d’entraînement)'}  [{fichier}]")
        image = f'<p><img src="qr-{s["slug"]}.png" alt="QR code" width="160"></p>' if m["canal"] == "qr" and qr else ""
        cartes.append(f"""<article style="border:1px solid #ccd;border-radius:10px;padding:12px 16px;margin:12px 0;background:#fff">
<p style="margin:0;color:#555;font-size:.9em">{html.escape(m['canal'].upper())} · de : {html.escape(exp or '—')} · état du lien : <strong>{html.escape(etat)}</strong></p>
<h2 style="font-size:1.05em;margin:6px 0">{html.escape(objet or 'SMS')}</h2>{corps_html(corps)}{image}
<p style="color:#555;font-size:.85em">Destination : <code>{html.escape(lien)}</code> · fichier : {html.escape(fichier)}</p></article>""")
    (sortie / "verification.txt").write_text("\n".join(lignes) + "\n", encoding="utf-8")
    (sortie / "apercu.html").write_text(f"""<!doctype html><html lang="fr"><meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1"><title>Boîte de test · campagne d'entraînement</title>
<body style="font-family:system-ui,sans-serif;background:#eef1f4;color:#1d2733;max-width:720px;margin:0 auto;padding:16px">
<h1 style="font-size:1.3em">Boîte de test : les faux messages de la campagne</h1>
<p>Site testé : <code>{html.escape(base)}</code>. Clique sur chaque lien : tu dois arriver sur la page « Tu t'es fait prendre… ».</p>
{''.join(cartes)}</body></html>
""", encoding="utf-8")
    print("\n".join(lignes))
    print(f"\nKit : {sortie.relative_to(RACINE)}/ (ouvre apercu.html dans le navigateur)")
    if echecs:
        print(f"{echecs} lien(s) en échec : le site tourne-t-il à l'adresse {base} ?", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
