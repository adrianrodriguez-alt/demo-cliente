/* Interactions communes de la démo (aucune donnée n'est enregistrée).
   API globale : window.ui (toast, open, close, icons, kanban, chart, colors, gridScales). */
(function () {
  "use strict";
  const $ = (s, r = document) => r.querySelector(s);
  const $$ = (s, r = document) => Array.from(r.querySelectorAll(s));

  const ui = (window.ui = window.ui || {});

  ui.icons = function () {
    if (window.lucide) window.lucide.createIcons({ attrs: { class: "icon" } });
  };

  /* ---------- Toasts ---------- */
  ui.toast = function (msg, type) {
    // Si une modale est ouverte, le toast doit vivre dans sa couche (top layer) pour rester net.
    const host = $$("dialog[open]").pop() || document.body;
    let box = Array.from(host.children).find((c) => c.classList.contains("toasts"));
    if (!box) { box = document.createElement("div"); box.className = "toasts"; box.setAttribute("aria-live", "polite"); host.appendChild(box); }
    const t = document.createElement("div");
    t.className = "toast" + (type === "warn" ? " warn" : "");
    t.setAttribute("role", "status");
    t.innerHTML = '<span class="ti"><i data-lucide="' + (type === "warn" ? "bell" : "check") + '"></i></span><span></span>';
    t.lastChild.textContent = msg;
    box.appendChild(t);
    ui.icons();
    setTimeout(() => { t.classList.add("out"); setTimeout(() => t.remove(), 220); }, 2600);
  };

  /* ---------- Dialogs (modales & tiroirs) ---------- */
  ui.open = function (id) {
    const d = document.getElementById(id);
    if (d && !d.open) { d.showModal(); ui.icons(); }
    return d;
  };
  ui.close = function (el) {
    const d = el && el.closest ? el.closest("dialog") : el;
    if (d && d.open) d.close();
  };

  document.addEventListener("click", function (e) {
    let opener = e.target.closest("[data-open]");
    // Un bouton d'action dans une ligne cliquable (éditer, supprimer, menu) ne doit pas ouvrir la fiche de la ligne
    const inner = e.target.closest("[data-edit], [data-delete], [data-confirm], [data-menu], .menu, [data-toast]");
    if (opener && inner && inner !== opener && opener.contains(inner)) opener = null;
    if (opener) {
      e.preventDefault();
      const d = ui.open(opener.dataset.open);
      // Modale CRUD ouverte par data-open = création : formulaire vide
      const crudForm = d && $("form[data-crud]", d);
      if (crudForm) { crudForm.reset(); d.dataset.mode = "create"; }
      // Pré-remplit les éléments [data-fill="clé"] avec data-* du déclencheur
      if (d) {
        $$("[data-fill]", d).forEach((n) => {
          const v = opener.dataset[n.dataset.fill];
          if (v !== undefined) { if (/^(INPUT|SELECT|TEXTAREA)$/.test(n.tagName)) n.value = v; else n.textContent = v; }
        });
      }
      return;
    }
    if (e.target.closest("[data-close]")) { ui.close(e.target); return; }

    const toaster = e.target.closest("[data-toast]");
    if (toaster && toaster.tagName !== "FORM" && !toaster.matches("[data-delete], [data-confirm]")) {
      ui.toast(toaster.dataset.toast, toaster.dataset.toastType);
      if (toaster.closest(".menu")) toaster.closest(".menu").classList.remove("is-open");
      if (toaster.hasAttribute("data-close-after")) ui.close(toaster);
    }
  });

  // Clic sur le fond = fermeture
  document.addEventListener("mousedown", function (e) {
    if (e.target.tagName === "DIALOG" && e.target.open) {
      const r = e.target.getBoundingClientRect();
      const inside = e.clientX >= r.left && e.clientX <= r.right && e.clientY >= r.top && e.clientY <= r.bottom;
      if (!inside) e.target.close();
    }
  });

  /* ---------- CRUD en modales ----------
     Liste : chaque élément porte [data-row], ses valeurs affichées portent [data-field="nom"]
             (+ data-value="brut" si le texte affiché diffère de la valeur du formulaire).
     Créer : <button data-open="m-x">   → modale en mode « create », formulaire vide.
     Éditer : <button data-edit="m-x">  (dans la ligne) → même modale en mode « edit », champs [name]
             pré-remplis depuis les [data-field] de la ligne.
     Titres : <span data-if="create">Nouveau…</span><span data-if="edit">Modifier…</span>.
     Enregistrer : <form data-demo data-crud="#idListe"> + <template data-row-template> (dans la liste
             ou désigné par data-template="#id") → la ligne est ajoutée en tête, ou mise à jour.
     Supprimer : <button data-delete data-confirm="Supprimer Dupont Industrie ?"> (dans la ligne)
             → modale de confirmation commune (#ui-confirm), puis la ligne disparaît.
     Compteurs : <span data-count-of="#idListe"> = nombre de [data-row] visibles. */
  let currentRow = null;
  const T = () => (window.UI_TEXT || {});
  const fieldValue = (n) => (n.dataset.value !== undefined ? n.dataset.value : n.textContent.trim());
  const inputText = (i) => (i.tagName === "SELECT" ? (i.selectedOptions[0] || {}).text || "" : i.value);

  function setMode(d, mode) {
    d.dataset.mode = mode;
  }

  function refreshCounts() {
    $$("[data-count-of]").forEach((c) => {
      const list = $(c.dataset.countOf);
      if (list) c.textContent = $$("[data-row]", list).filter((r) => !r.hidden).length;
    });
  }
  ui.refreshCounts = refreshCounts;

  function flash(row) {
    row.classList.remove("is-new"); void row.offsetWidth; row.classList.add("is-new");
  }

  document.addEventListener("click", function (e) {
    const ed = e.target.closest("[data-edit]");
    if (ed) {
      e.preventDefault();
      currentRow = ed.closest("[data-row]");
      const d = ui.open(ed.dataset.edit);
      if (!d) return;
      setMode(d, "edit");
      const f = $("form", d);
      if (f && currentRow) {
        $$("[name]", f).forEach((i) => {
          const src = $('[data-field="' + i.name + '"]', currentRow);
          if (!src) return;
          const v = fieldValue(src);
          if (i.type === "checkbox") i.checked = v === "1" || v === "true";
          else if (i.tagName === "SELECT" && ![...i.options].some((o) => o.value === v)) {
            const o = [...i.options].find((o) => o.text.trim() === v); if (o) i.value = o.value;
          } else i.value = v;
        });
      }
      return;
    }
    if (e.target.closest("[data-open]")) currentRow = null;
    const del = e.target.closest("[data-delete], [data-confirm]");
    if (del && !del.closest("#ui-confirm")) {
      e.preventDefault();
      const c = document.getElementById("ui-confirm");
      if (!c) return;
      $("[data-confirm-text]", c).textContent = del.dataset.confirm || T().confirm_delete || "";
      $("[data-confirm-ok]", c).textContent = del.dataset.confirmOk || T().delete || "OK";
      c._target = del;
      ui.open("ui-confirm");
    }
  });

  document.addEventListener("click", function (e) {
    if (!e.target.closest("[data-confirm-ok]")) return;
    const c = document.getElementById("ui-confirm");
    const del = c._target;
    c.close();
    if (!del) return;
    if (del.hasAttribute("data-delete")) {
      const row = del.closest("[data-row]");
      if (row) {
        row.classList.add("is-removing");
        setTimeout(() => { row.remove(); refreshCounts(); document.dispatchEvent(new CustomEvent("crud:deleted", { detail: { row } })); }, 260);
      }
    }
    ui.toast(del.dataset.toast || (del.hasAttribute("data-delete") ? T().deleted : T().done) || "OK", del.dataset.toastType);
  });

  // Formulaires de démo : pas d'envoi, fermeture + toast (+ CRUD si data-crud)
  document.addEventListener("submit", function (e) {
    const f = e.target;
    if (!f.hasAttribute("data-demo")) return;
    e.preventDefault();
    const d = f.closest("dialog");
    const editing = d && d.dataset.mode === "edit" && currentRow;
    if (f.dataset.crud) {
      const values = {};
      $$("[name]", f).forEach((i) => { values[i.name] = { text: inputText(i), value: i.type === "checkbox" ? (i.checked ? "1" : "0") : i.value }; });
      let row = editing ? currentRow : null;
      if (!row) {
        const list = $(f.dataset.crud);
        const tpl = f.dataset.template ? $(f.dataset.template) : $("template[data-row-template]", list ? list.closest("table, .card, section, div") || list : document);
        if (list && tpl) {
          row = tpl.content.firstElementChild.cloneNode(true);
          const body = list.tagName === "TABLE" ? $("tbody", list) : list;
          body.insertBefore(row, body.firstElementChild);
        }
      }
      if (row) {
        Object.entries(values).forEach(([k, v]) => {
          $$('[data-field="' + k + '"]', row).forEach((n) => {
            n.textContent = v.text;
            if (n.dataset.value !== undefined) n.dataset.value = v.value;
            // data-classes='{"livree": "badge success", "ouverte": "badge info"}' : classe selon la valeur
            if (n.dataset.classes) { try { const m = JSON.parse(n.dataset.classes); if (m[v.value]) n.className = m[v.value]; } catch (_) { /* JSON invalide : on garde la classe */ } }
          });
          if (row.dataset[k] !== undefined) row.dataset[k] = v.value;
        });
        ui.icons(); flash(row); refreshCounts();
        document.dispatchEvent(new CustomEvent(editing ? "crud:updated" : "crud:created", { detail: { row, values } }));
      }
    }
    ui.close(f);
    const msg = editing ? (f.dataset.toastEdit || T().saved) : f.dataset.toast;
    if (msg) ui.toast(msg, f.dataset.toastType);
    f.reset();
    currentRow = null;
    f.dispatchEvent(new CustomEvent("demo:submitted", { bubbles: true }));
  });

  /* ---------- Menus déroulants ---------- */
  document.addEventListener("click", function (e) {
    const trigger = e.target.closest("[data-menu]");
    $$(".menu.is-open").forEach((m) => { if (!trigger || m !== trigger.closest(".menu")) m.classList.remove("is-open"); });
    if (trigger) { e.preventDefault(); e.stopPropagation(); trigger.closest(".menu").classList.toggle("is-open"); }
  });

  /* ---------- Popovers (notifications, profil) ---------- */
  document.addEventListener("click", function (e) {
    const t = e.target.closest("[data-popover]");
    const pops = $$(".popover.is-open");
    if (t) {
      e.stopPropagation();
      const p = document.getElementById(t.dataset.popover);
      pops.forEach((x) => { if (x !== p) x.classList.remove("is-open"); });
      p.classList.toggle("is-open");
      return;
    }
    pops.forEach((x) => { if (!x.contains(e.target)) x.classList.remove("is-open"); });
  });
  document.addEventListener("click", function (e) {
    const b = e.target.closest("[data-mark-read]");
    if (!b) return;
    $$(".notif.unread").forEach((n) => n.classList.remove("unread"));
    const dot = $(".icon-btn .dot"); if (dot) dot.remove();
  });

  /* ---------- Onglets ----------
     <div data-tabs> <button class="tab" data-tab="a"> … <div data-panel="a"> */
  document.addEventListener("click", function (e) {
    const tab = e.target.closest("[data-tab]");
    if (!tab) return;
    const scope = tab.closest("[data-tabs]") || document;
    $$("[data-tab]", scope).forEach((t) => t.classList.toggle("is-active", t === tab));
    $$("[data-panel]", scope).forEach((p) => (p.hidden = p.dataset.panel !== tab.dataset.tab));
  });

  /* ---------- Filtres par statut ----------
     Boutons [data-filter="valeur|all"] dans un conteneur [data-filter-target="#id"].
     Les éléments filtrés portent data-status="valeur" (plusieurs valeurs séparées par un espace). */
  document.addEventListener("click", function (e) {
    const b = e.target.closest("[data-filter]");
    if (!b) return;
    const group = b.closest("[data-filter-target]");
    if (!group) return;
    $$("[data-filter]", group).forEach((x) => x.classList.toggle("is-active", x === b));
    const target = $(group.dataset.filterTarget);
    const v = b.dataset.filter;
    $$("[data-status]", target).forEach((row) => {
      row.hidden = !(v === "all" || row.dataset.status.split(" ").includes(v));
    });
  });

  /* ---------- Recherche locale ----------  <input data-search="#id"> */
  document.addEventListener("input", function (e) {
    const i = e.target.closest("[data-search]");
    if (!i) return;
    const q = i.value.trim().toLowerCase();
    const target = $(i.dataset.search);
    const items = $$("tbody tr, [data-searchable]", target);
    items.forEach((row) => (row.hidden = q && !row.textContent.toLowerCase().includes(q)));
  });

  /* ---------- Kanban (glisser-déposer) ---------- */
  ui.kanban = function (root) {
    let dragged = null;
    const refresh = () => $$(".kcol", root).forEach((c) => { const n = $(".kcol-count", c); if (n) n.textContent = $$(".kcard", c).length; });
    $$(".kcard", root).forEach((c) => {
      c.draggable = true;
      c.addEventListener("dragstart", (e) => { dragged = c; c.classList.add("is-dragging"); e.dataTransfer.effectAllowed = "move"; });
      c.addEventListener("dragend", () => { c.classList.remove("is-dragging"); dragged = null; });
    });
    $$(".kcards", root).forEach((zone) => {
      zone.addEventListener("dragover", (e) => {
        e.preventDefault(); zone.classList.add("is-over");
        const after = $$(".kcard:not(.is-dragging)", zone).find((el) => e.clientY < el.getBoundingClientRect().top + el.offsetHeight / 2);
        if (dragged) after ? zone.insertBefore(dragged, after) : zone.appendChild(dragged);
      });
      zone.addEventListener("dragleave", () => zone.classList.remove("is-over"));
      zone.addEventListener("drop", (e) => {
        e.preventDefault(); zone.classList.remove("is-over"); refresh();
        const col = zone.closest(".kcol");
        const name = col && $("h3", col) ? $("h3", col).textContent.trim() : "";
        if (dragged && name) ui.toast((root.dataset.toastPrefix || document.documentElement.dataset.movedTo || "→") + " « " + name + " »");
        root.dispatchEvent(new CustomEvent("kanban:moved", { detail: { card: dragged, column: col } }));
      });
    });
    refresh();
  };

  /* ---------- Palette de commandes (⌘K / Ctrl+K) ---------- */
  function paletteInit() {
    const pal = $("#palette");
    if (!pal) return;
    const input = $("input", pal);
    const items = () => $$(".p-item", pal).filter((i) => !i.hidden);
    let sel = 0;
    const paint = () => items().forEach((it, k) => it.classList.toggle("is-sel", k === sel));
    const openP = () => { pal.showModal(); input.value = ""; $$(".p-item", pal).forEach((i) => (i.hidden = false)); sel = 0; paint(); input.focus(); ui.icons(); };
    document.addEventListener("keydown", (e) => {
      if ((e.metaKey || e.ctrlKey) && e.key.toLowerCase() === "k") { e.preventDefault(); pal.open ? pal.close() : openP(); }
    });
    $$("[data-palette]").forEach((b) => b.addEventListener("click", openP));
    input.addEventListener("input", () => {
      const q = input.value.toLowerCase();
      $$(".p-item", pal).forEach((i) => (i.hidden = q && !i.textContent.toLowerCase().includes(q)));
      sel = 0; paint();
    });
    input.addEventListener("keydown", (e) => {
      const list = items();
      if (e.key === "ArrowDown") { sel = Math.min(sel + 1, list.length - 1); paint(); e.preventDefault(); }
      if (e.key === "ArrowUp") { sel = Math.max(sel - 1, 0); paint(); e.preventDefault(); }
      if (e.key === "Enter" && list[sel]) { window.location = list[sel].getAttribute("href"); }
    });
  }

  /* ---------- Graphiques (Chart.js aux couleurs du client, lues dans tokens.css) ---------- */
  const css = (v) => getComputedStyle(document.documentElement).getPropertyValue(v).trim();
  ui.colors = {};
  function readColors() {
    Object.assign(ui.colors, {
      brand: css("--brand-500"), brandSoft: css("--brand-200"), accent: css("--accent"), accentSoft: css("--accent-200"), dark: css("--ink-900"), gray: css("--ink-300"),
      grid: css("--ink-100"), success: css("--success"), danger: css("--danger"), info: css("--info"), muted: css("--ink-500"),
    });
  }
  readColors();
  ui.chart = function (canvas, config) {
    if (!window.Chart) return null;
    const C = window.Chart;
    readColors();
    C.defaults.font.family = css("--font-body");
    C.defaults.font.size = 12;
    C.defaults.color = ui.colors.muted;
    C.defaults.plugins.legend.display = false;
    C.defaults.plugins.tooltip.backgroundColor = ui.colors.dark;
    C.defaults.plugins.tooltip.padding = 10;
    C.defaults.plugins.tooltip.cornerRadius = 10;
    C.defaults.plugins.tooltip.titleFont = { family: css("--font-title"), weight: "600" };
    C.defaults.maintainAspectRatio = false;
    const el = typeof canvas === "string" ? document.querySelector(canvas) : canvas;
    return new C(el, config);
  };
  ui.gridScales = function (extra) {
    return Object.assign({
      x: { grid: { display: false }, border: { display: false } },
      y: { grid: { color: ui.colors.grid }, border: { display: false }, ticks: { padding: 8 } },
    }, extra || {});
  };

  /* ---------- Menu mobile ---------- */
  document.addEventListener("click", function (e) {
    if (e.target.closest(".burger")) document.body.classList.toggle("nav-open");
  });

  document.addEventListener("DOMContentLoaded", function () {
    ui.icons();
    paletteInit();
    $$("[data-kanban]").forEach(ui.kanban);
    const flash = document.body.dataset.flash;
    if (flash) ui.toast(flash);
  });
})();
