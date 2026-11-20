// Réflexes cyber : moteur de conversation (un seul fichier, aucune dépendance, aucune donnée envoyée).
// Un module = un fichier JSON : { id, titre, reflexe, source:{nom,url}, etapes:{ debut:{msg, choix:[{txt,va}] | va | fin} } }
(function () {
  "use strict";

  const params = new URLSearchParams(location.search);
  const id = params.get("m");
  const fil = document.getElementById("fil");
  const lent = !window.matchMedia("(prefers-reduced-motion: reduce)").matches;

  function memoire(lire, valeur) {
    try {
      const fait = JSON.parse(localStorage.getItem("reflexes-faits") || "[]");
      if (lire) return fait;
      if (!fait.includes(valeur)) fait.push(valeur);
      localStorage.setItem("reflexes-faits", JSON.stringify(fait));
    } catch (e) { /* navigation privée : on continue sans mémoire */ }
    return [];
  }

  function el(tag, classe, texte) {
    const n = document.createElement(tag);
    if (classe) n.className = classe;
    if (texte !== undefined) n.textContent = texte;
    return n;
  }

  function attendre(ms) {
    return new Promise((ok) => setTimeout(ok, lent ? ms : 0));
  }

  async function direPerso(texte) {
    const f = el("div", "frappe", "… ");
    f.setAttribute("aria-hidden", "true");
    fil.appendChild(f);
    // temps de « frappe » proportionnel au texte, borné pour tenir les 2 minutes
    await attendre(Math.min(1600, 350 + texte.length * 12));
    f.remove();
    fil.appendChild(el("div", "bulle perso", texte));
    window.scrollTo({ top: document.body.scrollHeight, behavior: lent ? "smooth" : "auto" });
  }

  function proposer(choix) {
    return new Promise((ok) => {
      const zone = el("div", "choix");
      zone.setAttribute("role", "group");
      zone.setAttribute("aria-label", "Ta réponse");
      choix.forEach((c, i) => {
        const texte = c.txt.charAt(0).toUpperCase() + c.txt.slice(1);   // « la personne… » → « La personne… »
        const b = el("button", "", texte);
        b.type = "button";
        b.addEventListener("click", () => {
          zone.remove();
          fil.appendChild(el("div", "bulle moi", texte));
          ok(c.va);
        });
        zone.appendChild(b);
        if (i === 0) setTimeout(() => b.focus(), 0);
      });
      fil.appendChild(zone);
    });
  }

  async function jouer(m, catalogue) {
    document.title = m.titre + " · " + catalogue.nom;
    document.getElementById("titre").textContent = m.titre;
    let cle = "debut";
    while (cle) {
      const e = m.etapes[cle];
      await direPerso(e.msg);
      if (e.fin) break;
      cle = e.choix ? await proposer(e.choix) : (await attendre(500), e.va);
    }
    memoire(false, m.id);
    const fin = el("section", "retenir");
    fin.setAttribute("aria-label", "À retenir");
    fin.appendChild(el("h2", "", "✅ À retenir"));
    fin.appendChild(el("p", "", m.reflexe));
    const src = el("p", "source");
    src.append("Source : ");
    const a = el("a", "", m.source.nom);
    a.href = m.source.url; a.rel = "noopener"; a.target = "_blank";
    src.appendChild(a);
    fin.appendChild(src);
    const act = el("div", "actions");
    const liste = catalogue.modules.map((x) => x.id);
    const suivant = liste[liste.indexOf(m.id) + 1];
    if (suivant) {
      const s = el("a", "bouton plein", "Module suivant");
      s.href = "module.html?m=" + encodeURIComponent(suivant);
      act.appendChild(s);
    }
    const r = el("a", "bouton", "Tous les modules");
    r.href = "./";
    act.appendChild(r);
    fin.appendChild(act);
    fil.appendChild(fin);
  }

  async function demarrer() {
    const catalogue = await (await fetch("catalogue.json")).json();
    document.getElementById("perso-nom").textContent = catalogue.personnage.nom;
    document.getElementById("perso-avatar").textContent = catalogue.personnage.avatar;
    document.getElementById("slogan").textContent = catalogue.slogan;
    if (!id || !catalogue.modules.some((x) => x.id === id)) {
      fil.appendChild(el("div", "bulle perso", "Je ne trouve pas ce module. Retourne à la liste des modules."));
      return;
    }
    const m = await (await fetch("modules/" + encodeURIComponent(id) + ".json")).json();
    await jouer(m, catalogue);
  }

  demarrer().catch(() => {
    fil.appendChild(el("div", "bulle perso", "Oups, le module n'a pas pu se charger. Réessaie dans un instant."));
  });
})();
