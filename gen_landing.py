import os

os.makedirs('frontend/public', exist_ok=True)

html = r"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>NeuroLearn Assist - AI Accessibility Platform</title>
<meta name="description" content="AI-powered learning platform for visually impaired and deaf-blind users. Learn smarter with voice, braille, and adaptive AI.">
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800;900&display=swap" rel="stylesheet">
<style>
:root{--bg:#050816;--bg2:#080d22;--glass:rgba(255,255,255,.04);--gb:rgba(255,255,255,.08);--blue:#3b82f6;--purple:#8b5cf6;--cyan:#06b6d4;--pink:#ec4899;--green:#22c55e;--text:#f1f5f9;--muted:#94a3b8;--card:rgba(14,20,45,.85)}
*,*::before,*::after{box-sizing:border-box;margin:0;padding:0}
html{scroll-behavior:smooth}
body{font-family:Inter,sans-serif;background:var(--bg);color:var(--text);overflow-x:hidden;line-height:1.65}
#pts{position:fixed;inset:0;z-index:0;pointer-events:none;overflow:hidden}
.pt{position:absolute;border-radius:50%;animation:floatUp linear infinite}
@keyframes floatUp{0%{transform:translateY(105vh);opacity:0}10%{opacity:.18}90%{opacity:.18}100%{transform:translateY(-5vh);opacity:0}}
.orb-bg{position:fixed;border-radius:50%;filter:blur(130px);opacity:.12;pointer-events:none;z-index:0;animation:orbP 9s ease-in-out infinite}
@keyframes orbP{0%,100%{opacity:.12;transform:scale(1)}50%{opacity:.22;transform:scale(1.12)}}
nav{position:fixed;top:14px;left:50%;transform:translateX(-50%);z-index:200;width:calc(100% - 48px);max-width:1200px;background:rgba(5,8,22,.75);backdrop-filter:blur(24px);border:1px solid var(--gb);border-radius:16px;padding:14px 28px;display:flex;align-items:center;justify-content:space-between;transition:background .3s}
.logo{display:flex;align-items:center;gap:10px;font-size:1.05rem;font-weight:800;text-decoration:none}
.logo-text{background:linear-gradient(135deg,var(--blue),var(--purple));-webkit-background-clip:text;-webkit-text-fill-color:transparent}
.logo svg{width:26px;height:26px;flex-shrink:0}
.nav-links{display:flex;gap:26px;list-style:none}
.nav-links a{color:var(--muted);text-decoration:none;font-size:.88rem;font-weight:500;transition:color .2s;cursor:pointer}
.nav-links a:hover,.nav-links a:focus-visible{color:var(--text);outline:2px solid var(--blue);border-radius:4px}
.btn-nav{background:linear-gradient(135deg,var(--blue),var(--purple));color:#fff;border:none;border-radius:10px;padding:10px 22px;font-size:.88rem;font-weight:700;cursor:pointer;text-decoration:none;display:inline-block;transition:opacity .2s,transform .2s,box-shadow .2s}
.btn-nav:hover{opacity:.9;transform:translateY(-1px);box-shadow:0 8px 30px rgba(139,92,246,.45)}
#mbt{display:none;background:none;border:none;color:var(--text);cursor:pointer;padding:4px}
.page{position:relative;z-index:1}
section{padding:96px 24px}
.wrap{max-width:1200px;margin:0 auto}
.stag{display:inline-block;font-size:.72rem;font-weight:700;letter-spacing:.1em;text-transform:uppercase;color:var(--blue);background:rgba(59,130,246,.1);border:1px solid rgba(59,130,246,.22);border-radius:100px;padding:4px 14px;margin-bottom:14px}
.sh{font-size:clamp(1.75rem,4vw,2.7rem);font-weight:900;line-height:1.08;margin-bottom:14px}
.ss{color:var(--muted);font-size:1rem;max-width:540px;line-height:1.7}
.shdr{margin-bottom:54px}.center{text-align:center}.center .ss{margin:0 auto}
.gt{background:linear-gradient(135deg,var(--blue) 0%,var(--purple) 55%,var(--pink) 100%);-webkit-background-clip:text;-webkit-text-fill-color:transparent}
.reveal{opacity:0;transform:translateY(38px);transition:opacity .7s,transform .7s}
.reveal.vis{opacity:1;transform:none}
.btn-p{background:linear-gradient(135deg,var(--blue),var(--purple));color:#fff;border:none;border-radius:12px;padding:15px 34px;font-size:.95rem;font-weight:700;cursor:pointer;text-decoration:none;display:inline-flex;align-items:center;gap:9px;transition:transform .2s,box-shadow .2s;animation:pulseG 3s ease-in-out infinite}
@keyframes pulseG{0%,100%{box-shadow:0 0 22px rgba(139,92,246,.3)}50%{box-shadow:0 0 45px rgba(139,92,246,.65)}}
.btn-p:hover{transform:translateY(-2px) scale(1.02)}
.btn-s{background:var(--glass);border:1px solid var(--gb);color:var(--text);border-radius:12px;padding:15px 34px;font-size:.95rem;font-weight:600;cursor:pointer;text-decoration:none;display:inline-flex;align-items:center;gap:9px;backdrop-filter:blur(12px);transition:all .2s}
.btn-s:hover{background:rgba(255,255,255,.09);transform:translateY(-2px)}
#hero{min-height:100vh;display:flex;align-items:center;padding-top:140px;text-align:center;background:radial-gradient(ellipse 80% 65% at 50% 0%,rgba(59,130,246,.13) 0%,transparent 70%)}
.hero-badge{display:inline-flex;align-items:center;gap:8px;background:rgba(59,130,246,.1);border:1px solid rgba(59,130,246,.3);border-radius:100px;padding:7px 18px;font-size:.78rem;font-weight:700;color:var(--blue);margin-bottom:28px;animation:fdU .6s ease both}
.bdot{width:7px;height:7px;background:var(--blue);border-radius:50%;animation:blink 1.5s infinite}
@keyframes blink{0%,100%{opacity:1}50%{opacity:0}}
h1{font-size:clamp(2.5rem,6vw,5rem);font-weight:900;line-height:1.04;letter-spacing:-.02em;animation:fdU .7s .1s ease both}
.hero-sub{font-size:clamp(1rem,2vw,1.2rem);color:var(--muted);max-width:600px;margin:26px auto 40px;animation:fdU .7s .2s ease both}
.hero-btns{display:flex;gap:16px;justify-content:center;flex-wrap:wrap;animation:fdU .7s .3s ease both}
@keyframes fdU{from{opacity:0;transform:translateY(28px)}to{opacity:1;transform:none}}
.hero-visual{margin-top:72px;animation:fdU .7s .4s ease both}
.ai-sphere{width:260px;height:260px;border-radius:50%;margin:0 auto;display:flex;align-items:center;justify-content:center;background:radial-gradient(circle,rgba(59,130,246,.22) 0%,rgba(139,92,246,.12) 60%,transparent 80%);border:1px solid rgba(139,92,246,.25);position:relative;animation:sphereGlow 4s ease-in-out infinite}
@keyframes sphereGlow{0%,100%{box-shadow:0 0 60px rgba(59,130,246,.22)}50%{box-shadow:0 0 110px rgba(139,92,246,.55)}}
.sphere-icon{animation:floatY 3s ease-in-out infinite}
@keyframes floatY{0%,100%{transform:translateY(0)}50%{transform:translateY(-14px)}}
.orbit{position:absolute;border-radius:50%;border:1px dashed;animation:spin linear infinite}
.o1{inset:-34px;border-color:rgba(59,130,246,.22);animation-duration:22s}
.o2{inset:-68px;border-color:rgba(139,92,246,.14);animation-duration:34s;animation-direction:reverse}
@keyframes spin{to{transform:rotate(360deg)}}
.stat-row{display:flex;gap:16px;justify-content:center;flex-wrap:wrap;margin-top:60px;animation:fdU .7s .5s ease both}
.stat-chip{background:var(--card);border:1px solid var(--gb);border-radius:14px;padding:16px 24px;text-align:center;backdrop-filter:blur(20px)}
.sn{font-size:1.6rem;font-weight:900;background:linear-gradient(135deg,var(--blue),var(--purple));-webkit-background-clip:text;-webkit-text-fill-color:transparent}
.sl{font-size:.76rem;color:var(--muted);margin-top:2px}
.fg{display:grid;grid-template-columns:repeat(auto-fit,minmax(310px,1fr));gap:22px}
.fc{background:var(--card);border:1px solid var(--gb);border-radius:20px;padding:30px;backdrop-filter:blur(22px);cursor:pointer;transition:all .3s cubic-bezier(.175,.885,.32,1.275);position:relative;overflow:hidden}
.fc::before{content:"";position:absolute;inset:0;opacity:0;background:linear-gradient(135deg,rgba(59,130,246,.06),rgba(139,92,246,.06));transition:opacity .3s;pointer-events:none}
.fc:hover{transform:translateY(-7px);border-color:rgba(139,92,246,.42);box-shadow:0 22px 60px rgba(0,0,0,.45),0 0 40px rgba(139,92,246,.12)}
.fc:hover::before{opacity:1}
.fi{width:52px;height:52px;border-radius:14px;margin-bottom:18px;display:flex;align-items:center;justify-content:center}
.fc h3{font-size:1.08rem;font-weight:700;margin-bottom:9px}
.fc p{color:var(--muted);font-size:.9rem;line-height:1.68}
.fbadge{display:inline-block;margin-top:14px;font-size:.69rem;font-weight:700;text-transform:uppercase;padding:3px 10px;border-radius:100px;background:rgba(59,130,246,.1);color:var(--blue);border:1px solid rgba(59,130,246,.22)}
.steps{display:grid;grid-template-columns:repeat(auto-fit,minmax(210px,1fr));gap:30px;position:relative}
.steps::before{content:"";position:absolute;top:44px;left:12%;right:12%;height:2px;background:linear-gradient(90deg,var(--blue),var(--purple),var(--pink));opacity:.2}
.step{text-align:center}.step-n{width:88px;height:88px;border-radius:50%;margin:0 auto 22px;background:linear-gradient(135deg,var(--blue),var(--purple));display:flex;align-items:center;justify-content:center;font-size:1.5rem;font-weight:900;color:#fff;box-shadow:0 0 30px rgba(139,92,246,.4);position:relative;z-index:1;transition:transform .3s,box-shadow .3s}
.step:hover .step-n{transform:scale(1.1);box-shadow:0 0 56px rgba(139,92,246,.7)}
.step h3{font-size:.98rem;font-weight:700;margin-bottom:8px}
.step p{color:var(--muted);font-size:.86rem;line-height:1.6}
.dbox{background:var(--card);border:1px solid var(--gb);border-radius:24px;overflow:hidden;backdrop-filter:blur(22px)}
.dbar{background:rgba(255,255,255,.03);border-bottom:1px solid var(--gb);padding:13px 20px;display:flex;align-items:center;gap:8px}
.dd{width:12px;height:12px;border-radius:50%}
.d1{background:#ff5f57}.d2{background:#ffbd2e}.d3{background:#28c940}
.dinner{padding:36px;display:grid;grid-template-columns:1fr 1fr;gap:36px;align-items:start}
.dchat{display:flex;flex-direction:column;gap:12px}
.cm{padding:13px 17px;border-radius:16px;font-size:.88rem;line-height:1.65;max-width:85%}
.mai{background:rgba(59,130,246,.14);border:1px solid rgba(59,130,246,.22);border-radius:4px 16px 16px 16px}
.mu{background:linear-gradient(135deg,var(--blue),var(--purple));border-radius:16px 4px 16px 16px;align-self:flex-end}
.dstats{display:grid;gap:14px}
.dsc{background:rgba(255,255,255,.03);border:1px solid var(--gb);border-radius:14px;padding:18px 22px}
.dsc-label{font-size:.72rem;color:var(--muted);margin-bottom:8px;text-transform:uppercase;letter-spacing:.05em}
.dsc-num{font-size:1.8rem;font-weight:900;background:linear-gradient(135deg,var(--blue),var(--purple));-webkit-background-clip:text;-webkit-text-fill-color:transparent}
.pb{height:6px;background:rgba(255,255,255,.1);border-radius:100px;margin-top:8px;overflow:hidden}
.pf{height:100%;border-radius:100px}
.ttrack-wrap{overflow:hidden;mask:linear-gradient(90deg,transparent,#000 10%,#000 90%,transparent)}
.ttrack{display:flex;gap:22px;animation:scrollT 36s linear infinite;width:max-content}
.ttrack:hover{animation-play-state:paused}
@keyframes scrollT{to{transform:translateX(-50%)}}
.tc{min-width:310px;max-width:330px;background:var(--card);border:1px solid var(--gb);border-radius:20px;padding:26px;backdrop-filter:blur(22px);flex-shrink:0;transition:border-color .3s,box-shadow .3s}
.tc:hover{border-color:rgba(139,92,246,.4);box-shadow:0 0 30px rgba(139,92,246,.12)}
.stars{color:#fbbf24;margin-bottom:12px}
.ttext{color:var(--muted);font-size:.88rem;line-height:1.72;margin-bottom:18px;font-style:italic}
.tauthor{display:flex;align-items:center;gap:12px}
.av{width:38px;height:38px;border-radius:50%;display:flex;align-items:center;justify-content:center;font-size:.82rem;font-weight:800;color:#fff;flex-shrink:0}
.aname{font-size:.88rem;font-weight:700}.atitle{font-size:.72rem;color:var(--muted)}
.ptoggle{display:flex;align-items:center;justify-content:center;gap:14px;margin:26px 0;font-size:.88rem;color:var(--muted)}
.tswitch{width:50px;height:26px;background:rgba(255,255,255,.1);border-radius:100px;cursor:pointer;position:relative;border:1px solid var(--gb);transition:background .3s}
.tswitch.on{background:linear-gradient(90deg,var(--blue),var(--purple))}
.tknob{position:absolute;top:3px;left:3px;width:20px;height:20px;background:#fff;border-radius:50%;transition:transform .35s cubic-bezier(.175,.885,.32,1.275);box-shadow:0 2px 6px rgba(0,0,0,.3)}
.tswitch.on .tknob{transform:translateX(24px)}
.sbadge{background:rgba(34,197,94,.15);color:var(--green);border:1px solid rgba(34,197,94,.3);border-radius:100px;padding:2px 10px;font-size:.7rem;font-weight:700}
.pgrid{display:grid;grid-template-columns:repeat(auto-fit,minmax(290px,1fr));gap:22px}
.pc{background:var(--card);border:1px solid var(--gb);border-radius:24px;padding:38px 34px;backdrop-filter:blur(22px);position:relative;overflow:hidden;transition:transform .3s,box-shadow .3s}
.pc:hover{transform:translateY(-5px);box-shadow:0 20px 60px rgba(0,0,0,.4)}
.pc.pop{border-color:rgba(139,92,246,.5);box-shadow:0 0 42px rgba(139,92,246,.16);background:linear-gradient(160deg,rgba(14,20,45,.9),rgba(20,14,48,.9))}
.pbadge{position:absolute;top:18px;right:18px;background:linear-gradient(135deg,var(--blue),var(--purple));color:#fff;font-size:.68rem;font-weight:700;text-transform:uppercase;padding:4px 12px;border-radius:100px}
.pname{font-size:.76rem;font-weight:700;text-transform:uppercase;letter-spacing:.1em;color:var(--muted);margin-bottom:10px}
.pprice{font-size:2.8rem;font-weight:900;line-height:1;background:linear-gradient(135deg,var(--blue),var(--purple));-webkit-background-clip:text;-webkit-text-fill-color:transparent}
.pperiod{font-size:.82rem;color:var(--muted);margin-top:6px;margin-bottom:26px}
.pfeats{list-style:none;display:flex;flex-direction:column;gap:11px;margin-bottom:28px}
.pfeats li{display:flex;align-items:center;gap:10px;font-size:.88rem;color:var(--muted)}
.check{width:20px;height:20px;border-radius:50%;background:rgba(59,130,246,.15);display:inline-flex;align-items:center;justify-content:center;flex-shrink:0}
.pbtn{width:100%;padding:13px;border-radius:12px;font-size:.92rem;font-weight:700;cursor:pointer;transition:all .2s;border:none}
.psolid{background:linear-gradient(135deg,var(--blue),var(--purple));color:#fff}
.psolid:hover{opacity:.9;transform:translateY(-2px);box-shadow:0 10px 30px rgba(139,92,246,.42)}
.pout{background:transparent;color:var(--text);border:1px solid var(--gb) !important}
.pout:hover{background:rgba(255,255,255,.07);transform:translateY(-2px)}
#cta{text-align:center;background:radial-gradient(ellipse 80% 65% at 50% 50%,rgba(139,92,246,.1) 0%,transparent 70%)}
.cbox{background:var(--card);border:1px solid rgba(139,92,246,.32);border-radius:32px;padding:78px 40px;backdrop-filter:blur(32px);position:relative;overflow:hidden;box-shadow:0 0 88px rgba(139,92,246,.14)}
.cbox::before{content:"";position:absolute;top:-50%;left:-50%;width:200%;height:200%;background:conic-gradient(from 0deg,transparent 0%,rgba(139,92,246,.05) 25%,transparent 50%);animation:cRot 22s linear infinite;pointer-events:none}
@keyframes cRot{to{transform:rotate(360deg)}}
.cbox>*{position:relative;z-index:1}
.cbox h2{font-size:clamp(1.8rem,4vw,2.8rem);font-weight:900;margin-bottom:14px}
.cbox p{color:var(--muted);font-size:1.05rem;max-width:480px;margin:0 auto 36px}
.cacts{display:flex;gap:14px;justify-content:center;flex-wrap:wrap}
.a11y-row{display:flex;gap:18px;justify-content:center;flex-wrap:wrap;margin-top:36px}
.achip{display:flex;align-items:center;gap:8px;background:rgba(255,255,255,.04);border:1px solid var(--gb);border-radius:100px;padding:8px 16px;font-size:.78rem;color:var(--muted)}
footer{background:var(--bg2);border-top:1px solid var(--gb);padding:54px 24px 28px;text-align:center;color:var(--muted);font-size:.86rem}
.flogo{font-size:1.3rem;font-weight:900;background:linear-gradient(135deg,var(--blue),var(--purple));-webkit-background-clip:text;-webkit-text-fill-color:transparent;margin-bottom:14px}
.flinks{display:flex;gap:22px;justify-content:center;flex-wrap:wrap;margin:18px 0}
.flinks a{color:var(--muted);text-decoration:none;transition:color .2s}
.flinks a:hover{color:var(--text)}
.fbot{margin-top:26px;padding-top:18px;border-top:1px solid var(--gb)}
@media(max-width:768px){
  .nav-links{display:none}#mbt{display:block}
  .nav-links.open{display:flex;flex-direction:column;position:absolute;top:66px;left:0;right:0;background:rgba(5,8,22,.97);backdrop-filter:blur(22px);padding:20px;border-bottom:1px solid var(--gb);gap:16px}
  .steps::before{display:none}.dinner{grid-template-columns:1fr}.dstats{grid-template-columns:1fr 1fr}
  section{padding:68px 16px}.cbox{padding:54px 22px}
}
@media(prefers-reduced-motion:reduce){*,*::before,*::after{animation:none !important;transition-duration:.01ms !important}}
</style>
</head>
<body>
<div id="pts" aria-hidden="true"></div>
<div class="orb-bg" style="width:600px;height:600px;top:-200px;left:-200px;background:radial-gradient(circle,#3b82f6,transparent)" aria-hidden="true"></div>
<div class="orb-bg" style="width:500px;height:500px;bottom:-100px;right:-100px;background:radial-gradient(circle,#8b5cf6,transparent);animation-delay:4s" aria-hidden="true"></div>
<div class="page">

<nav id="nav" role="navigation" aria-label="Main navigation">
  <a href="#" class="logo" aria-label="NeuroLearn Assist home">
    <svg viewBox="0 0 24 24" fill="none" stroke-width="2" aria-hidden="true"><defs><linearGradient id="lg" x1="0" y1="0" x2="1" y2="1"><stop offset="0%" stop-color="#3b82f6"/><stop offset="100%" stop-color="#8b5cf6"/></linearGradient></defs><path stroke="url(#lg)" d="M12 2L2 7l10 5 10-5-10-5zM2 17l10 5 10-5M2 12l10 5 10-5"/></svg>
    <span class="logo-text">NeuroLearn Assist</span>
  </a>
  <ul class="nav-links" id="nl"><li><a href="#features">Features</a></li><li><a href="#how">How It Works</a></li><li><a href="#demo">Demo</a></li><li><a href="#pricing">Pricing</a></li></ul>
  <a href="#cta" class="btn-nav">Get Started Free</a>
  <button id="mbt" aria-label="Toggle menu" aria-expanded="false" onclick="const nl=document.getElementById('nl');const o=nl.classList.toggle('open');this.setAttribute('aria-expanded',o)">
    <svg width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" aria-hidden="true"><line x1="3" y1="6" x2="21" y2="6"/><line x1="3" y1="12" x2="21" y2="12"/><line x1="3" y1="18" x2="21" y2="18"/></svg>
  </button>
</nav>

<section id="hero" aria-labelledby="h1">
  <div class="wrap">
    <div class="hero-badge"><span class="bdot" aria-hidden="true"></span>AI-Powered Accessibility Platform</div>
    <h1 id="h1">Learn Beyond <span class="gt">Limits.</span><br>Powered by AI.</h1>
    <p class="hero-sub">NeuroLearn Assist breaks barriers for visually impaired and deaf-blind learners — with adaptive AI tutoring, voice interaction, braille output, and real-time document intelligence.</p>
    <div class="hero-btns">
      <a href="#demo" class="btn-p"><svg width="18" height="18" viewBox="0 0 24 24" fill="currentColor" aria-hidden="true"><polygon points="5 3 19 12 5 21 5 3"/></svg>See It in Action</a>
      <a href="#features" class="btn-s"><svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" aria-hidden="true"><circle cx="12" cy="12" r="10"/><line x1="12" y1="8" x2="12" y2="12"/><line x1="12" y1="16" x2="12.01" y2="16"/></svg>Explore Features</a>
    </div>
    <div class="hero-visual" aria-hidden="true">
      <div class="ai-sphere">
        <div class="orbit o1"></div><div class="orbit o2"></div>
        <div class="sphere-icon">
          <svg width="90" height="90" viewBox="0 0 24 24" fill="none" stroke-width="1.5"><defs><linearGradient id="sg" x1="0" y1="0" x2="1" y2="1"><stop offset="0%" stop-color="#3b82f6"/><stop offset="100%" stop-color="#8b5cf6"/></linearGradient></defs><path stroke="url(#sg)" d="M21 16V8a2 2 0 0 0-1-1.73l-7-4a2 2 0 0 0-2 0l-7 4A2 2 0 0 0 3 8v8a2 2 0 0 0 1 1.73l7 4a2 2 0 0 0 2 0l7-4A2 2 0 0 0 21 16z"/><polyline stroke="url(#sg)" points="3.27 6.96 12 12.01 20.73 6.96"/><line stroke="url(#sg)" x1="12" y1="22.08" x2="12" y2="12"/></svg>
        </div>
      </div>
    </div>
    <div class="stat-row">
      <div class="stat-chip"><div class="sn">10K+</div><div class="sl">Learners Empowered</div></div>
      <div class="stat-chip"><div class="sn">98%</div><div class="sl">AI Accuracy</div></div>
      <div class="stat-chip"><div class="sn">15+</div><div class="sl">Languages</div></div>
      <div class="stat-chip"><div class="sn">24/7</div><div class="sl">AI Availability</div></div>
    </div>
  </div>
</section>

<section id="features" style="background:linear-gradient(180deg,transparent,rgba(8,13,34,.8) 50%,transparent)" aria-labelledby="fh">
  <div class="wrap">
    <div class="shdr center reveal"><div class="stag">Capabilities</div><h2 class="sh" id="fh">Everything You Need to <span class="gt">Learn Freely</span></h2><p class="ss">A full accessibility-first AI platform built for every type of learner.</p></div>
    <div class="fg">
      <article class="fc reveal"><div class="fi" style="background:rgba(59,130,246,.15)"><svg width="26" height="26" viewBox="0 0 24 24" fill="none" stroke="#3b82f6" stroke-width="2" aria-hidden="true"><path d="M12 1a3 3 0 0 0-3 3v8a3 3 0 0 0 6 0V4a3 3 0 0 0-3-3z"/><path d="M19 10v2a7 7 0 0 1-14 0v-2"/><line x1="12" y1="19" x2="12" y2="23"/><line x1="8" y1="23" x2="16" y2="23"/></svg></div><h3>Voice AI Tutor</h3><p>Natural AI-powered voice conversations. Ask questions, get explanations, and learn hands-free through intelligent dialogue.</p><span class="fbadge">Voice First</span></article>
      <article class="fc reveal"><div class="fi" style="background:rgba(139,92,246,.15)"><svg width="26" height="26" viewBox="0 0 24 24" fill="none" stroke="#8b5cf6" stroke-width="2" aria-hidden="true"><path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"/><polyline points="14 2 14 8 20 8"/><line x1="16" y1="13" x2="8" y2="13"/><line x1="16" y1="17" x2="8" y2="17"/></svg></div><h3>PDF Intelligence</h3><p>Upload any PDF and instantly get AI-generated summaries, concept maps, flashcards, and personalized quiz questions.</p><span class="fbadge">AI Powered</span></article>
      <article class="fc reveal"><div class="fi" style="background:rgba(6,182,212,.15)"><svg width="26" height="26" viewBox="0 0 24 24" fill="none" stroke="#06b6d4" stroke-width="2" aria-hidden="true"><rect x="2" y="3" width="20" height="14" rx="2"/><line x1="8" y1="21" x2="16" y2="21"/><line x1="12" y1="17" x2="12" y2="21"/></svg></div><h3>Braille Output</h3><p>Seamless braille conversion with Arduino integration for tactile displays. Full blind-accessible learning experience.</p><span class="fbadge">Hardware</span></article>
      <article class="fc reveal"><div class="fi" style="background:rgba(236,72,153,.15)"><svg width="26" height="26" viewBox="0 0 24 24" fill="none" stroke="#ec4899" stroke-width="2" aria-hidden="true"><path d="M9 3H5a2 2 0 0 0-2 2v4m6-6h10a2 2 0 0 1 2 2v4M9 3v18m0 0h10a2 2 0 0 0 2-2V9M9 21H5a2 2 0 0 1-2-2V9m0 0h18"/></svg></div><h3>Adaptive Quizzes</h3><p>Dynamic difficulty that adjusts in real-time based on your performance. Always learning at exactly the right pace.</p><span class="fbadge">Adaptive AI</span></article>
      <article class="fc reveal"><div class="fi" style="background:rgba(34,197,94,.15)"><svg width="26" height="26" viewBox="0 0 24 24" fill="none" stroke="#22c55e" stroke-width="2" aria-hidden="true"><path d="M17 21v-2a4 4 0 0 0-4-4H5a4 4 0 0 0-4 4v2"/><circle cx="9" cy="7" r="4"/><path d="M23 21v-2a4 4 0 0 0-3-3.87"/><path d="M16 3.13a4 4 0 0 1 0 7.75"/></svg></div><h3>Multi-Agent Tutor</h3><p>A team of AI agents — knowledge, evaluation, command, and voice — working together seamlessly for optimal learning.</p><span class="fbadge">Multi-Agent</span></article>
      <article class="fc reveal"><div class="fi" style="background:rgba(249,115,22,.15)"><svg width="26" height="26" viewBox="0 0 24 24" fill="none" stroke="#f97316" stroke-width="2" aria-hidden="true"><rect x="3" y="11" width="18" height="11" rx="2" ry="2"/><path d="M7 11V7a5 5 0 0 1 10 0v4"/></svg></div><h3>Private &amp; Secure</h3><p>All documents processed with end-to-end security. Your learning data stays completely private, always.</p><span class="fbadge">Privacy First</span></article>
    </div>
  </div>
</section>

<section id="how" style="background:radial-gradient(ellipse 60% 40% at 50% 50%,rgba(139,92,246,.08) 0%,transparent 70%)" aria-labelledby="hwh">
  <div class="wrap">
    <div class="shdr center reveal"><div class="stag">Process</div><h2 class="sh" id="hwh">Simple. <span class="gt">Powerful.</span> Accessible.</h2><p class="ss">Get started in seconds — no technical knowledge required.</p></div>
    <div class="steps">
      <div class="step reveal"><div class="step-n">1</div><h3>Upload Document</h3><p>Upload any PDF. Our AI extracts and understands all content instantly with smart OCR fallback support.</p></div>
      <div class="step reveal"><div class="step-n">2</div><h3>AI Analyzes</h3><p>Multi-agent AI generates summaries, concepts, flashcards, and personalized quiz questions automatically.</p></div>
      <div class="step reveal"><div class="step-n">3</div><h3>Learn Your Way</h3><p>Use voice, braille, flashcards, or quizzes — whichever mode works best for you personally.</p></div>
      <div class="step reveal"><div class="step-n">4</div><h3>Track Progress</h3><p>Adaptive AI monitors performance and continuously fine-tunes difficulty to keep you growing.</p></div>
    </div>
  </div>
</section>

<section id="demo" aria-labelledby="dh">
  <div class="wrap">
    <div class="shdr center reveal"><div class="stag">Live Demo</div><h2 class="sh" id="dh">See the <span class="gt">AI in Action</span></h2><p class="ss">Experience real-time AI tutoring and accessibility features live.</p></div>
    <div class="dbox reveal">
      <div class="dbar" aria-hidden="true"><div class="dd d1"></div><div class="dd d2"></div><div class="dd d3"></div><span style="margin-left:12px;font-size:.78rem;color:var(--muted)">NeuroLearn Assist &mdash; AI Tutor Session</span></div>
      <div class="dinner">
        <div class="dchat" role="log" aria-label="AI conversation demo">
          <div class="cm mai">Hello! I am your AI Tutor. I have analyzed your document. What would you like to learn today?</div>
          <div class="cm mu">Explain the main concepts from Chapter 3</div>
          <div class="cm mai">Chapter 3 covers <strong>Neural Plasticity</strong>. Key concepts:<br><br>1. <strong>Hebbian Learning</strong> &mdash; neurons that fire together, wire together<br>2. <strong>Long-term Potentiation (LTP)</strong> &mdash; strengthening synaptic connections<br>3. <strong>Neurogenesis</strong> &mdash; creation of new neurons in adult brains</div>
          <div class="cm mu">Generate a quiz on this topic</div>
          <div class="cm mai"><strong>Quiz (Medium Difficulty):</strong><br><br>Which process best describes strengthening of synaptic connections through repetition?<br><br>A) Neurogenesis &nbsp;|&nbsp; <strong>B) LTP ✓</strong> &nbsp;|&nbsp; C) Pruning &nbsp;|&nbsp; D) Myelination</div>
        </div>
        <div class="dstats">
          <div class="dsc"><div class="dsc-label">Comprehension</div><div class="dsc-num">98%</div><div class="pb"><div class="pf" style="width:98%;background:linear-gradient(90deg,#3b82f6,#8b5cf6)"></div></div></div>
          <div class="dsc"><div class="dsc-label">Concepts Extracted</div><div class="dsc-num">24</div><div class="pb"><div class="pf" style="width:80%;background:linear-gradient(90deg,#8b5cf6,#ec4899)"></div></div></div>
          <div class="dsc"><div class="dsc-label">Quiz Score</div><div class="dsc-num">87%</div><div class="pb"><div class="pf" style="width:87%;background:linear-gradient(90deg,#06b6d4,#3b82f6)"></div></div></div>
          <div class="dsc"><div class="dsc-label">Voice Sessions</div><div class="dsc-num">12</div><div class="pb"><div class="pf" style="width:60%;background:linear-gradient(90deg,#22c55e,#06b6d4)"></div></div></div>
        </div>
      </div>
    </div>
  </div>
</section>

<section id="testimonials" aria-labelledby="th">
  <div class="wrap"><div class="shdr center reveal"><div class="stag">Testimonials</div><h2 class="sh" id="th">Loved by <span class="gt">Learners Worldwide</span></h2></div></div>
  <div class="ttrack-wrap reveal" role="region" aria-label="Testimonials"><div class="ttrack" id="tt"></div></div>
</section>

<section id="pricing" style="background:radial-gradient(ellipse 70% 50% at 50% 50%,rgba(59,130,246,.07) 0%,transparent 70%)" aria-labelledby="ph">
  <div class="wrap">
    <div class="shdr center reveal"><div class="stag">Pricing</div><h2 class="sh" id="ph">Simple, <span class="gt">Transparent</span> Pricing</h2><p class="ss">Start free. Upgrade anytime. No surprises or hidden fees.</p></div>
    <div class="ptoggle reveal">
      <span>Monthly</span>
      <div class="tswitch" id="ts" onclick="toggleP()" onkeydown="if(event.key==='Enter'||event.key===' '){event.preventDefault();toggleP()}" role="switch" aria-checked="false" tabindex="0"><div class="tknob"></div></div>
      <span>Annual <span class="sbadge">Save 30%</span></span>
    </div>
    <div class="pgrid">
      <div class="pc reveal"><div class="pname">Free</div><div class="pprice">$0</div><div class="pperiod">Forever free &middot; No card needed</div><ul class="pfeats"><li><span class="check"><svg width="10" height="10" viewBox="0 0 12 12" fill="none" stroke="#3b82f6" stroke-width="2" aria-hidden="true"><polyline points="2 6 5 9 10 3"/></svg></span>3 PDF uploads/month</li><li><span class="check"><svg width="10" height="10" viewBox="0 0 12 12" fill="none" stroke="#3b82f6" stroke-width="2" aria-hidden="true"><polyline points="2 6 5 9 10 3"/></svg></span>Basic Voice AI</li><li><span class="check"><svg width="10" height="10" viewBox="0 0 12 12" fill="none" stroke="#3b82f6" stroke-width="2" aria-hidden="true"><polyline points="2 6 5 9 10 3"/></svg></span>Flashcards &amp; Quizzes</li><li><span class="check"><svg width="10" height="10" viewBox="0 0 12 12" fill="none" stroke="#3b82f6" stroke-width="2" aria-hidden="true"><polyline points="2 6 5 9 10 3"/></svg></span>Community support</li></ul><button class="pbtn pout">Get Started Free</button></div>
      <div class="pc pop reveal"><div class="pbadge">Most Popular</div><div class="pname">Pro</div><div class="pprice" id="pp">$19</div><div class="pperiod" id="per">per month</div><ul class="pfeats"><li><span class="check"><svg width="10" height="10" viewBox="0 0 12 12" fill="none" stroke="#3b82f6" stroke-width="2" aria-hidden="true"><polyline points="2 6 5 9 10 3"/></svg></span>Unlimited PDF uploads</li><li><span class="check"><svg width="10" height="10" viewBox="0 0 12 12" fill="none" stroke="#3b82f6" stroke-width="2" aria-hidden="true"><polyline points="2 6 5 9 10 3"/></svg></span>Advanced Voice AI Tutor</li><li><span class="check"><svg width="10" height="10" viewBox="0 0 12 12" fill="none" stroke="#3b82f6" stroke-width="2" aria-hidden="true"><polyline points="2 6 5 9 10 3"/></svg></span>Adaptive Quizzes</li><li><span class="check"><svg width="10" height="10" viewBox="0 0 12 12" fill="none" stroke="#3b82f6" stroke-width="2" aria-hidden="true"><polyline points="2 6 5 9 10 3"/></svg></span>Braille Output Support</li><li><span class="check"><svg width="10" height="10" viewBox="0 0 12 12" fill="none" stroke="#3b82f6" stroke-width="2" aria-hidden="true"><polyline points="2 6 5 9 10 3"/></svg></span>Multi-Agent Sessions</li><li><span class="check"><svg width="10" height="10" viewBox="0 0 12 12" fill="none" stroke="#3b82f6" stroke-width="2" aria-hidden="true"><polyline points="2 6 5 9 10 3"/></svg></span>Priority 24/7 support</li></ul><button class="pbtn psolid">Start Pro Trial</button></div>
      <div class="pc reveal"><div class="pname">Enterprise</div><div class="pprice">Custom</div><div class="pperiod">Contact us for pricing</div><ul class="pfeats"><li><span class="check"><svg width="10" height="10" viewBox="0 0 12 12" fill="none" stroke="#3b82f6" stroke-width="2" aria-hidden="true"><polyline points="2 6 5 9 10 3"/></svg></span>Everything in Pro</li><li><span class="check"><svg width="10" height="10" viewBox="0 0 12 12" fill="none" stroke="#3b82f6" stroke-width="2" aria-hidden="true"><polyline points="2 6 5 9 10 3"/></svg></span>Custom AI model training</li><li><span class="check"><svg width="10" height="10" viewBox="0 0 12 12" fill="none" stroke="#3b82f6" stroke-width="2" aria-hidden="true"><polyline points="2 6 5 9 10 3"/></svg></span>Hardware integration help</li><li><span class="check"><svg width="10" height="10" viewBox="0 0 12 12" fill="none" stroke="#3b82f6" stroke-width="2" aria-hidden="true"><polyline points="2 6 5 9 10 3"/></svg></span>SSO &amp; Admin Dashboard</li><li><span class="check"><svg width="10" height="10" viewBox="0 0 12 12" fill="none" stroke="#3b82f6" stroke-width="2" aria-hidden="true"><polyline points="2 6 5 9 10 3"/></svg></span>Dedicated CSM + SLA</li></ul><button class="pbtn pout">Contact Sales</button></div>
    </div>
  </div>
</section>

<section id="cta" aria-labelledby="ctah">
  <div class="wrap">
    <div class="cbox reveal">
      <div class="stag">Get Started Today</div>
      <h2 id="ctah">Ready to Learn <span class="gt">Without Limits?</span></h2>
      <p>Join thousands of learners who have transformed their education with NeuroLearn Assist.</p>
      <div class="cacts">
        <a href="#" class="btn-p"><svg width="18" height="18" viewBox="0 0 24 24" fill="currentColor" aria-hidden="true"><polygon points="5 3 19 12 5 21 5 3"/></svg>Start for Free Today</a>
        <a href="#demo" class="btn-s"><svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" aria-hidden="true"><path d="M1 12s4-8 11-8 11 8 11 8-4 8-11 8-11-8-11-8z"/><circle cx="12" cy="12" r="3"/></svg>Watch Demo</a>
      </div>
      <div class="a11y-row">
        <div class="achip"><svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" aria-hidden="true"><path d="M12 1a3 3 0 0 0-3 3v8a3 3 0 0 0 6 0V4a3 3 0 0 0-3-3z"/><path d="M19 10v2a7 7 0 0 1-14 0v-2"/></svg>Voice Accessible</div>
        <div class="achip"><svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" aria-hidden="true"><rect x="2" y="3" width="20" height="14" rx="2"/><line x1="8" y1="21" x2="16" y2="21"/></svg>Braille Ready</div>
        <div class="achip"><svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" aria-hidden="true"><path d="M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10z"/></svg>WCAG 2.1 AA</div>
        <div class="achip"><svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" aria-hidden="true"><circle cx="12" cy="12" r="10"/><line x1="2" y1="12" x2="22" y2="12"/><path d="M12 2a15.3 15.3 0 0 1 4 10 15.3 15.3 0 0 1-4 10 15.3 15.3 0 0 1-4-10 15.3 15.3 0 0 1 4-10z"/></svg>15+ Languages</div>
      </div>
    </div>
  </div>
</section>

<footer>
  <div class="flogo">NeuroLearn Assist</div>
  <p>AI-powered learning for every ability, everywhere.</p>
  <nav class="flinks" aria-label="Footer links">
    <a href="#">Product</a><a href="#">Features</a><a href="#">Pricing</a><a href="#">Accessibility</a><a href="#">Privacy</a><a href="#">Terms</a>
  </nav>
  <div class="fbot">&copy; 2025 NeuroLearn Assist. Built with care for accessibility.</div>
</footer>
</div>

<script>
(function(){
  const c=document.getElementById("pts"),cols=["#3b82f6","#8b5cf6","#06b6d4","#ec4899","#22c55e"];
  for(let i=0;i<50;i++){
    const el=document.createElement("div");el.className="pt";
    const s=Math.random()*3+2;
    Object.assign(el.style,{width:s+"px",height:s+"px",left:Math.random()*100+"%",background:cols[i%5],animationDuration:(Math.random()*14+9)+"s",animationDelay:(Math.random()*14)+"s"});
    c.appendChild(el);
  }
})();

const obs=new IntersectionObserver(es=>es.forEach(e=>{if(e.isIntersecting)e.target.classList.add("vis")}),{threshold:.1});
document.querySelectorAll(".reveal").forEach(el=>obs.observe(el));

const td=[
  {n:"Arjun S.",t:"Student, Visual Impairment",q:"NeuroLearn Assist transformed how I study. The voice tutor feels like a real teacher available 24/7.",c:"#3b82f6",i:"AS"},
  {n:"Priya M.",t:"Special Education Teacher",q:"I recommend this to all my students. Braille integration is seamless and adaptive quizzes are exceptional.",c:"#8b5cf6",i:"PM"},
  {n:"Carlos R.",t:"University Student",q:"The PDF analysis understood complex research papers and created perfect flashcards automatically. Incredible.",c:"#06b6d4",i:"CR"},
  {n:"Fatima K.",t:"Deaf-Blind Learner",q:"For the first time I can learn independently. The braille and voice combination is a complete breakthrough for me.",c:"#ec4899",i:"FK"},
  {n:"David L.",t:"Parent of Blind Child",q:"My daughter can now study alongside her peers. This platform gave her confidence and independence she deserved.",c:"#22c55e",i:"DL"},
  {n:"Riya T.",t:"Accessibility Researcher",q:"Real WCAG compliance with actual usability — rare to find. Technically impressive and genuinely helpful.",c:"#f97316",i:"RT"},
];
(function(){
  const tt=document.getElementById("tt");
  tt.innerHTML=[...td,...td].map(t=>
    `<div class="tc"><div class="stars">\u2605\u2605\u2605\u2605\u2605</div><p class="ttext">&ldquo;${t.q}&rdquo;</p><div class="tauthor"><div class="av" style="background:${t.c}22;color:${t.c}">${t.i}</div><div><div class="aname">${t.n}</div><div class="atitle">${t.t}</div></div></div></div>`
  ).join("");
})();

let ann=false;
function toggleP(){
  ann=!ann;
  const ts=document.getElementById("ts");
  ts.classList.toggle("on",ann);ts.setAttribute("aria-checked",ann+"");
  document.getElementById("pp").textContent=ann?"$13":"$19";
  document.getElementById("per").textContent=ann?"per month, billed annually":"per month";
}

window.addEventListener("scroll",()=>{
  document.getElementById("nav").style.background=scrollY>50?"rgba(5,8,22,.96)":"rgba(5,8,22,.75)";
},{passive:true});
</script>
</body>
</html>"""

with open('frontend/public/landing.html', 'w', encoding='utf-8') as f:
    f.write(html)
print(f'Written {len(html)} chars to frontend/public/landing.html')
