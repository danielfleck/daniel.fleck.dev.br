(function () {
    'use strict';

    const legacySectionMap = {
        'privacidade': '/privacidade/',
        'termos': '/termos/',
        'projetos': '/portfolio/',
        'blog': '/blog/',
        'erros': '/erros/',
        'roadmap': '/roadmap/',
        'ferramentas': '/ferramentas/'
    };

    function redirectLegacyHash() {
        if (window.location.pathname !== '/' || !window.location.hash) return;
        const value = decodeURIComponent(window.location.hash.slice(1));
        if (legacySectionMap[value]) {
            window.location.replace(legacySectionMap[value]);
            return;
        }
        if (value.startsWith('post-')) {
            window.location.replace('/blog/' + encodeURIComponent(value.slice(5)) + '/');
            return;
        }
        if (value.startsWith('erro-')) {
            window.location.replace('/erros/' + encodeURIComponent(value.slice(5)) + '/');
        }
    }

    function initCountdown() {
        const days = document.getElementById('cd-days');
        if (!days) return;
        const target = new Date('2027-12-16T00:00:00-03:00').getTime();
        const els = {
            days,
            hours: document.getElementById('cd-hours'),
            mins: document.getElementById('cd-mins'),
            secs: document.getElementById('cd-secs')
        };
        function update() {
            let diff = Math.max(0, target - Date.now());
            els.days.textContent = String(Math.floor(diff / 86400000)).padStart(2, '0');
            els.hours.textContent = String(Math.floor((diff % 86400000) / 3600000)).padStart(2, '0');
            els.mins.textContent = String(Math.floor((diff % 3600000) / 60000)).padStart(2, '0');
            els.secs.textContent = String(Math.floor((diff % 60000) / 1000)).padStart(2, '0');
        }
        update();
        window.setInterval(update, 1000);
    }

    function drawRadar() {
        const canvas = document.getElementById('radarCanvas');
        if (!canvas || !canvas.getContext) return;
        const wrapper = canvas.parentElement;
        const rect = wrapper ? wrapper.getBoundingClientRect() : canvas.getBoundingClientRect();
        const cssWidth = Math.max(300, Math.floor(rect.width || canvas.clientWidth || 640));
        const cssHeight = Math.max(300, Math.floor(rect.height || canvas.clientHeight || 340));
        const dpr = window.devicePixelRatio || 1;
        canvas.style.width = cssWidth + 'px';
        canvas.style.height = cssHeight + 'px';
        canvas.width = Math.floor(cssWidth * dpr);
        canvas.height = Math.floor(cssHeight * dpr);
        const ctx = canvas.getContext('2d');
        ctx.setTransform(dpr, 0, 0, dpr, 0, 0);
        const labels = ['SQL','Python','Indicadores','Requisitos','Jira/Git','Linux/Suporte','Documentação'];
        const current = [45,20,25,50,45,35,60];
        const target = [75,60,60,75,70,55,80];
        const w=cssWidth,h=cssHeight,cx=w/2,cy=h/2+8,radius=Math.min(w,h)*0.32,levels=5;
        ctx.clearRect(0,0,w,h); ctx.lineWidth=1; ctx.textAlign='center'; ctx.textBaseline='middle';
        for(let level=1;level<=levels;level++){
            const r=radius*level/levels; ctx.beginPath();
            labels.forEach((_,i)=>{const a=-Math.PI/2+i*2*Math.PI/labels.length; const x=cx+Math.cos(a)*r,y=cy+Math.sin(a)*r; if(i===0)ctx.moveTo(x,y);else ctx.lineTo(x,y);});
            ctx.closePath();ctx.strokeStyle='#cbd5e1';ctx.stroke();
        }
        labels.forEach((label,i)=>{const a=-Math.PI/2+i*2*Math.PI/labels.length;const ld=radius+Math.min(46,Math.max(28,w*.055));const x=cx+Math.cos(a)*ld,y=cy+Math.sin(a)*ld;ctx.beginPath();ctx.moveTo(cx,cy);ctx.lineTo(cx+Math.cos(a)*radius,cy+Math.sin(a)*radius);ctx.strokeStyle='#e2e8f0';ctx.stroke();ctx.fillStyle='#334155';ctx.font=w<520?'10px Arial':'12px Arial';ctx.fillText(label,x,y);});
        function plot(values,fillStyle,strokeStyle){ctx.beginPath();values.forEach((value,i)=>{const a=-Math.PI/2+i*2*Math.PI/labels.length;const r=radius*value/100;const x=cx+Math.cos(a)*r,y=cy+Math.sin(a)*r;if(i===0)ctx.moveTo(x,y);else ctx.lineTo(x,y);});ctx.closePath();ctx.fillStyle=fillStyle;ctx.fill();ctx.strokeStyle=strokeStyle;ctx.lineWidth=2;ctx.stroke();}
        plot(target,'rgba(37,99,235,.10)','rgba(37,99,235,.35)');
        plot(current,'rgba(20,184,166,.26)','rgba(20,184,166,1)');
        ctx.textAlign='left';ctx.font=w<520?'10px Arial':'12px Arial';ctx.fillStyle='#64748b';ctx.fillText(w<520?'Autoavaliação: azul = alvo • verde = atual':'Autoavaliação meramente ilustrativa • Azul: alvo • Verde: ponto atual estimado',14,h-18);
    }

    redirectLegacyHash();
    window.addEventListener('DOMContentLoaded', function () { initCountdown(); drawRadar(); });
    let timer;
    window.addEventListener('resize', function(){window.clearTimeout(timer);timer=window.setTimeout(drawRadar,120);});
})();

/* PRIVACY-LINK-GUARD
 * Racional:
 * - links externos: transparência de saída, não consentimento LGPD;
 * - contato: não manter mailto do endereço oficial no HTML estático;
 * - nenhum fetch/preview/preload do destino;
 * - racional completo em /docs/conformidade/.
 */
(function () {
  "use strict";

  const CONTACT_LOCAL = "contato";
  const CONTACT_DOMAIN = "fleck.dev.br";
  let active = null;
  let previousFocus = null;

  function officialMailto() {
    return "mailto:" + CONTACT_LOCAL + "@" + CONTACT_DOMAIN;
  }

  function closeGuard() {
    if (!active) return;
    active.remove();
    active = null;
    if (previousFocus && typeof previousFocus.focus === "function") {
      previousFocus.focus();
    }
    previousFocus = null;
  }

  function node(tag, text, className) {
    const element = document.createElement(tag);
    if (className) element.className = className;
    if (text !== undefined) element.textContent = text;
    return element;
  }

  function openGuard(trigger, kind, destination) {
    closeGuard();
    previousFocus = trigger;

    const backdrop = node("div", undefined, "link-guard-backdrop");
    const dialog = node("section", undefined, "link-guard-dialog");
    dialog.setAttribute("role", "dialog");
    dialog.setAttribute("aria-modal", "true");
    dialog.setAttribute("aria-labelledby", "link-guard-title");

    const title = node(
      "h2",
      kind === "email" ? "Antes de abrir o e-mail" : "Você está saindo deste site"
    );
    title.id = "link-guard-title";
    dialog.appendChild(title);

    if (kind === "email") {
      dialog.appendChild(node(
        "p",
        "Ao continuar, seu aplicativo ou serviço de e-mail será aberto. " +
        "Envie apenas o necessário para o assunto."
      ));
      const warning = node(
        "p",
        "Não envie senhas, tokens, dados bancários, documentos de identidade " +
        "ou dados pessoais sensíveis sem necessidade.",
        "link-guard-warning"
      );
      dialog.appendChild(warning);
      dialog.appendChild(node(
        "p",
        "Dados técnicos de autenticação, transporte e entrega podem ser tratados " +
        "pela infraestrutura do provedor de e-mail. O responsável pelo site trata " +
        "os dados que efetivamente chegam à caixa postal para responder e adotar " +
        "as providências cabíveis."
      ));
      dialog.appendChild(node(
        "code",
        CONTACT_LOCAL + " [arroba] " + CONTACT_DOMAIN,
        "link-guard-destination"
      ));
    } else {
      const url = new URL(destination, window.location.href);
      dialog.appendChild(node(
        "p",
        "O destino pertence a outro site. A partir da saída, a navegação fica " +
        "sujeita aos termos, política de privacidade, cookies e controles do serviço externo."
      ));
      dialog.appendChild(node("code", url.hostname, "link-guard-destination"));
      dialog.appendChild(node(
        "p",
        "O conteúdo do destino não é consultado nem carregado para exibir este aviso. " +
        "A navegação ocorre somente após sua confirmação.",
        "link-guard-note"
      ));
    }

    const actions = node("div", undefined, "link-guard-actions");
    const cancel = node("button", "Cancelar");
    cancel.type = "button";
    cancel.addEventListener("click", closeGuard);

    const proceed = node(
      "a",
      kind === "email" ? "Abrir aplicativo de e-mail" : "Continuar para o site externo"
    );
    proceed.dataset.linkGuardBypass = "true";
    proceed.href = destination;

    if (kind !== "email") {
      const originalTarget = trigger.getAttribute("target");
      if (originalTarget) proceed.setAttribute("target", originalTarget);
      if (originalTarget === "_blank") {
        proceed.setAttribute("rel", "noopener noreferrer");
      }
    }

    proceed.addEventListener("click", function () {
      window.setTimeout(closeGuard, 0);
    });

    actions.append(cancel, proceed);
    dialog.appendChild(actions);
    backdrop.appendChild(dialog);
    document.body.appendChild(backdrop);
    active = backdrop;

    backdrop.addEventListener("click", function (event) {
      if (event.target === backdrop) closeGuard();
    });

    proceed.focus();
  }

  function classify(anchor) {
    if (!anchor || anchor.dataset.linkGuardBypass === "true") return null;
    if (anchor.hasAttribute("download")) return null;

    const raw = (anchor.getAttribute("href") || "").trim();
    if (!raw || raw.startsWith("#") || raw.startsWith("tel:") ||
        raw.startsWith("javascript:") || raw.startsWith("data:") ||
        raw.startsWith("blob:")) return null;

    if (/^mailto:/i.test(raw)) {
      return { kind: "email", url: raw };
    }

    let parsed;
    try {
      parsed = new URL(raw, window.location.href);
    } catch (_) {
      return null;
    }

    if (!["http:", "https:"].includes(parsed.protocol)) return null;
    if (parsed.origin === window.location.origin) return null;
    return { kind: "external", url: parsed.href };
  }

  document.addEventListener("click", function (event) {
    const contactTrigger = event.target.closest &&
      event.target.closest("[data-contact-open]");
    if (contactTrigger) {
      event.preventDefault();
      event.stopPropagation();
      openGuard(contactTrigger, "email", officialMailto());
      return;
    }

    const anchor = event.target.closest && event.target.closest("a[href]");
    const info = classify(anchor);
    if (!info) return;

    event.preventDefault();
    event.stopPropagation();
    openGuard(anchor, info.kind, info.url);
  }, true);

  document.addEventListener("keydown", function (event) {
    if (active && event.key === "Escape") closeGuard();
  });
})();
