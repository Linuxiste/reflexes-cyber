// Réflexes cyber : page d'accueil (choix du métier, module du jour, liste par rubrique).
// Le métier choisi et les modules faits restent dans ce navigateur : rien n'est envoyé, aucun compte.
(function () {
  "use strict";
  function lire(cle, defaut) {
    try { return JSON.parse(localStorage.getItem(cle) || "null") || defaut; } catch (e) { return defaut; }
  }
  function ecrire(cle, valeur) {
    try { localStorage.setItem(cle, JSON.stringify(valeur)); } catch (e) { /* navigation privée */ }
  }
  function el(tag, classe, texte) {
    var n = document.createElement(tag);
    if (classe) n.className = classe;
    if (texte !== undefined) n.textContent = texte;
    return n;
  }

  function afficher(c) {
    var metier = lire("reflexes-metier", "tous");
    if (!c.metiers.some(function (x) { return x.id === metier; })) metier = "tous";
    var deja = lire("reflexes-faits", []);
    // modules du métier, ceux qui lui sont prioritaires d'abord (l'ordre des rubriques est conservé ensuite)
    var mods = c.modules.filter(function (m) {
      return m.metiers.indexOf("tous") >= 0 || m.metiers.indexOf(metier) >= 0;
    });
    var ordonnes = mods.filter(function (m) { return m.prioritaire_pour.indexOf(metier) >= 0; })
      .concat(mods.filter(function (m) { return m.prioritaire_pour.indexOf(metier) < 0; }));
    var prochain = ordonnes.find(function (m) { return deja.indexOf(m.id) < 0; }) || ordonnes[0];
    if (prochain) {
      document.getElementById("jour-texte").textContent = prochain.titre + " · avec " + c.personnage.nom;
      document.getElementById("jour-lien").href = "module.html?m=" + encodeURIComponent(prochain.id);
    }
    var faitsMetier = mods.filter(function (m) { return deja.indexOf(m.id) >= 0; }).length;
    document.getElementById("progression").textContent = faitsMetier + " module(s) faits sur " + mods.length + " pour ce parcours.";
    var zone = document.getElementById("rubriques");
    zone.textContent = "";
    c.rubriques.forEach(function (rub) {
      var liste = ordonnes.filter(function (m) { return m.rubrique === rub; });
      if (!liste.length) return;
      var s = el("section", "rubrique");
      s.appendChild(el("h2", "", rub));
      var ul = el("ul", "liste");
      liste.forEach(function (m) {
        var li = el("li"), a = el("a");
        a.href = "module.html?m=" + encodeURIComponent(m.id);
        var t = m.theme + " · " + m.titre;
        if (m.prioritaire_pour.indexOf(metier) >= 0) t = "★ " + t;
        a.appendChild(el("span", "", t));
        if (deja.indexOf(m.id) >= 0) a.appendChild(el("span", "fait", "✓ fait"));
        li.appendChild(a); ul.appendChild(li);
      });
      s.appendChild(ul); zone.appendChild(s);
    });
  }

  fetch("catalogue.json").then(function (r) { return r.json(); }).then(function (c) {
    document.title = c.nom;
    document.getElementById("nom").textContent = c.nom;
    document.getElementById("slogan").textContent = c.slogan;
    document.getElementById("perso-avatar").textContent = c.personnage.avatar;
    document.getElementById("pied").textContent = c.pied;
    var choix = document.getElementById("metier");
    c.metiers.forEach(function (x) {
      var o = el("option", "", x.nom); o.value = x.id; choix.appendChild(o);
    });
    choix.value = lire("reflexes-metier", "tous");
    if (!choix.value) choix.value = "tous";
    choix.addEventListener("change", function () { ecrire("reflexes-metier", choix.value); afficher(c); });
    afficher(c);
  });
})();
