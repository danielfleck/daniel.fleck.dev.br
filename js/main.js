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
