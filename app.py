import streamlit as st

st.set_page_config(
    page_title="CultureDelta",
    page_icon="Δ",
    layout="wide"
)

from agent import run_culture_delta
import datetime
import json
import os
import time

DAILY_LIMIT = 15

# ── Usage tracking ────────────────────────────────────────────────────────
def get_usage():
    usage_file = "usage.json"
    today = str(datetime.date.today())
    if os.path.exists(usage_file):
        with open(usage_file, "r") as f:
            data = json.load(f)
        if data.get("date") == today:
            return data.get("count", 0)
    return 0

def increment_usage():
    usage_file = "usage.json"
    today = str(datetime.date.today())
    count = get_usage() + 1
    with open(usage_file, "w") as f:
        json.dump({"date": today, "count": count}, f)
    return count

# ── Global CSS ────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=IBM+Plex+Mono:wght@400;500;600&family=IBM+Plex+Sans:wght@300;400;500;600;700&family=IBM+Plex+Serif:ital,wght@0,400;0,500;0,600;1,400&display=swap');

:root {
  --ink:#0a0e14; --ink-2:#0d1219; --surface:#10161f; --surface-2:#141c27;
  --border:#1c2330; --border-2:#252e3d;
  --text:#e8ecf2; --text-2:#9aa5b6; --text-3:#5d6a7d; --text-4:#3a4351;
  --now:#5ea1ff; --now-soft:#1a2a44; --now-glow:#5ea1ff33;
  --then:#c39a6a; --then-soft:#2a2218;
  --signal:#5ec98d;
  --mono:'IBM Plex Mono',ui-monospace,monospace;
  --sans:'IBM Plex Sans',system-ui,sans-serif;
  --serif:'IBM Plex Serif',Georgia,serif;
}

html,body,[class*="css"]{font-family:var(--sans);background:var(--ink);color:var(--text);}
.stApp{background:var(--ink);}
#MainMenu,footer,header{visibility:hidden;}
.block-container{padding:2.5rem 3.5rem 5rem;max-width:1280px;}

/* Subtle radial wash */
.stApp::before{
  content:'';position:fixed;inset:0;pointer-events:none;z-index:0;
  background:
    radial-gradient(ellipse 80% 50% at 50% -10%, rgba(94,161,255,0.06), transparent 60%),
    radial-gradient(ellipse 60% 40% at 100% 100%, rgba(195,154,106,0.04), transparent 70%);
}

/* Hide default input labels look */
h1,h2,h3,h4,h5{font-family:var(--serif)!important;letter-spacing:-0.01em!important;color:var(--text)!important;}

/* ─ Top status bar ─ */
.cd-topbar{display:flex;align-items:center;justify-content:space-between;
  padding-bottom:18px;border-bottom:1px solid var(--border);margin-bottom:30px;}
.cd-brand{display:flex;align-items:baseline;gap:14px;}
.cd-brand-mark{font-family:var(--mono);font-size:11px;letter-spacing:.18em;color:var(--now);
  text-transform:uppercase;font-weight:600;}
.cd-brand-name{font-family:var(--serif);font-size:22px;letter-spacing:-0.01em;font-weight:500;color:var(--text);}
.cd-brand-name em{font-style:italic;color:var(--then);font-weight:400;}
.cd-status{display:flex;align-items:center;gap:22px;}
.cd-stat{font-family:var(--mono);font-size:10.5px;letter-spacing:.06em;color:var(--text-3);
  display:flex;align-items:center;gap:8px;}
.cd-stat .k{color:var(--text-4);text-transform:uppercase;letter-spacing:.12em;}
.cd-stat .v{color:var(--text-2);}
.cd-stat .dot{width:6px;height:6px;border-radius:50%;background:var(--signal);
  box-shadow:0 0 8px var(--signal);animation:cd-pulse 2s ease-in-out infinite;}
@keyframes cd-pulse{0%,100%{opacity:1}50%{opacity:.4}}

/* ─ Hero ─ */
.cd-eyebrow{font-family:var(--mono);font-size:11px;color:var(--text-3);
  letter-spacing:.22em;text-transform:uppercase;margin-bottom:22px;}
.cd-eyebrow .glyph{color:var(--now);margin-right:10px;}
.cd-title{font-family:var(--serif)!important;font-weight:400!important;font-size:60px!important;
  line-height:1.05!important;letter-spacing:-0.02em!important;margin:0 0 18px!important;
  max-width:920px;text-wrap:balance;color:var(--text)!important;}
.cd-title em{font-style:italic;color:var(--then);}
.cd-title .arr{color:var(--now);font-style:normal;display:inline-block;transform:translateY(-4px);margin:0 4px;}
.cd-lede{font-family:var(--sans);font-size:17px;line-height:1.65;color:var(--text-2);
  max-width:640px;margin:0 0 36px;}
.cd-lede .accent{color:var(--text);}

/* ─ Console (input area) ─ */
.cd-console{border:1px solid var(--border);border-radius:14px;
  background:linear-gradient(180deg,var(--surface),var(--ink-2));
  padding:0;margin-bottom:18px;
  box-shadow:0 1px 0 rgba(255,255,255,.02) inset, 0 24px 48px -24px rgba(0,0,0,.6);}
.cd-console-head{display:flex;align-items:center;justify-content:space-between;
  padding:12px 18px;border-bottom:1px solid var(--border);}
.cd-lights{display:flex;gap:6px;}
.cd-lights span{width:9px;height:9px;border-radius:50%;background:var(--border-2);}
.cd-lights span.on{background:var(--now);box-shadow:0 0 8px var(--now-glow);}
.cd-console-tag{font-family:var(--mono);font-size:10.5px;letter-spacing:.14em;
  text-transform:uppercase;color:var(--text-3);}
.cd-console-r{font-family:var(--mono);font-size:10.5px;letter-spacing:.08em;color:var(--text-4);}
.cd-console-body{padding:22px 26px 8px;}
.cd-console-foot{padding:14px 26px;border-top:1px solid var(--border);
  font-family:var(--mono);font-size:10.5px;color:var(--text-3);letter-spacing:.06em;
  display:flex;justify-content:space-between;}

/* Streamlit inputs */
.stTextInput label{font-family:var(--mono)!important;font-size:10px!important;
  letter-spacing:.16em!important;text-transform:uppercase!important;color:var(--text-3)!important;
  font-weight:500!important;}
.stTextInput > div > div > input{
  background:var(--ink)!important;border:1px solid var(--border)!important;border-radius:8px!important;
  color:var(--text)!important;font-family:var(--sans)!important;font-size:15px!important;
  padding:0 14px!important;height:48px!important;line-height:48px!important;}
.stTextInput > div > div > input:focus{
  border-color:var(--now)!important;box-shadow:0 0 0 3px var(--now-glow)!important;}
.stTextInput > div > div > input::placeholder{color:var(--text-4)!important;font-style:italic!important;}

/* Year inputs get color hint via parent class — handled inline */
.cd-then .stTextInput > div > div > input{font-family:var(--mono)!important;text-align:center;
  color:var(--then)!important;border-color:#2a2218!important;letter-spacing:.04em;}
.cd-now  .stTextInput > div > div > input{font-family:var(--mono)!important;text-align:center;
  color:var(--now)!important;border-color:#1a2a44!important;letter-spacing:.04em;}

.cd-arrow-cell{height:48px;display:flex;align-items:center;justify-content:center;margin-top:26px;}
.cd-arrow-cell .arr-line{width:100%;height:1px;
  background:linear-gradient(90deg,var(--then),var(--now));position:relative;}
.cd-arrow-cell .arr-line::after{content:'▸';position:absolute;right:-3px;top:-10px;
  color:var(--now);font-size:14px;}

/* Run button */
.stButton > button{
  background:linear-gradient(180deg,#6db1ff,#4a8fec)!important;color:#061021!important;
  border:none!important;border-radius:8px!important;font-family:var(--sans)!important;
  font-weight:600!important;font-size:14px!important;height:48px!important;width:100%!important;
  margin-top:26px!important;letter-spacing:.02em!important;
  box-shadow:0 4px 20px -6px var(--now-glow), inset 0 1px 0 rgba(255,255,255,.3)!important;}
.stButton > button:hover{
  background:linear-gradient(180deg,#7bbaff,#5398f0)!important;
  box-shadow:0 8px 24px -6px var(--now-glow), inset 0 1px 0 rgba(255,255,255,.3)!important;}

/* Example chips row */
.cd-chips{display:flex;flex-wrap:wrap;gap:6px;}
.cd-chip{font-family:var(--mono);font-size:10.5px;color:var(--text-2);
  background:var(--surface-2);border:1px solid var(--border);border-radius:999px;
  padding:4px 10px;}
.cd-chip .from{color:var(--then);}
.cd-chip .to{color:var(--now);}

/* Quota bar */
.cd-quota{margin-top:6px;display:flex;align-items:center;justify-content:space-between;
  font-family:var(--mono);font-size:10.5px;color:var(--text-4);letter-spacing:.08em;}
.cd-quota .bar{flex:1;height:2px;background:var(--border);margin:0 16px;overflow:hidden;}
.cd-quota .bar i{display:block;height:100%;
  background:linear-gradient(90deg,var(--now),var(--then));}

/* Section dividers */
.cd-rule{display:grid;grid-template-columns:auto 1fr auto;align-items:center;gap:16px;
  margin:60px 0 26px;}
.cd-rule .label{font-family:var(--mono);font-size:11px;letter-spacing:.2em;
  text-transform:uppercase;color:var(--text-3);}
.cd-rule .label span{color:var(--now);margin-right:8px;}
.cd-rule .line{height:1px;background:linear-gradient(90deg,var(--border),transparent);}
.cd-rule .meta{font-family:var(--mono);font-size:10.5px;color:var(--text-4);letter-spacing:.08em;}

/* How-it-works cards */
.cd-how{background:var(--surface);border:1px solid var(--border);border-radius:12px;
  padding:22px;position:relative;overflow:hidden;height:100%;}
.cd-how::before{content:'';position:absolute;left:0;top:0;bottom:0;width:2px;
  background:linear-gradient(180deg,var(--now),transparent);opacity:.6;}
.cd-how-step{font-family:var(--mono);font-size:10px;letter-spacing:.18em;
  text-transform:uppercase;color:var(--now);margin-bottom:14px;}
.cd-how-title{font-family:var(--serif);font-size:18px;color:var(--text);margin:0 0 10px;font-weight:500;}
.cd-how-desc{font-size:13.5px;line-height:1.7;color:var(--text-2);}
.cd-how-tech{margin-top:16px;padding-top:14px;border-top:1px dashed var(--border);
  font-family:var(--mono);font-size:10px;color:var(--text-3);line-height:1.9;}
.cd-pill{display:inline-block;padding:2px 6px;background:var(--ink);
  border:1px solid var(--border);border-radius:3px;margin-right:4px;}

/* ─ Analyzing pipeline (3 steps) ─ */
.cd-pipe{display:flex;gap:14px;margin:24px 0;}
.cd-pipe-step{flex:1;background:var(--surface);border:2px solid var(--border);
  border-radius:10px;padding:18px;min-height:160px;}
.cd-pipe-step.active{border-color:var(--now);background:#0f1726;}
.cd-pipe-step.done{border-color:var(--signal);background:#0d1812;}
.cd-pipe-num{font-family:var(--mono);font-size:10px;letter-spacing:.18em;
  text-transform:uppercase;color:var(--text-4);margin-bottom:8px;}
.cd-pipe-step.active .cd-pipe-num{color:var(--now);}
.cd-pipe-step.done   .cd-pipe-num{color:var(--signal);}
.cd-pipe-title{font-family:var(--serif);font-size:16px;color:var(--text);font-weight:500;margin-bottom:8px;}
.cd-pipe-desc{font-size:12.5px;color:var(--text-3);line-height:1.7;}
.cd-pipe-status{margin-top:14px;font-family:var(--mono);font-size:10px;letter-spacing:.05em;color:var(--text-4);}
.cd-pipe-step.active .cd-pipe-status{color:var(--now);}
.cd-pipe-step.active .cd-pipe-status::before{content:'● ';animation:cd-pulse 1.2s ease-in-out infinite;}
.cd-pipe-step.done .cd-pipe-status{color:var(--signal);}
.cd-pipe-step.done .cd-pipe-status::before{content:'✓ ';}

/* ─ Report masthead ─ */
.cd-masthead{display:grid;grid-template-columns:1fr auto;align-items:end;gap:24px;
  padding-bottom:18px;border-bottom:1px solid var(--border);margin-bottom:30px;}
.cd-report-eyebrow{font-family:var(--mono);font-size:11px;letter-spacing:.2em;
  text-transform:uppercase;color:var(--text-3);margin-bottom:12px;}
.cd-report-eyebrow span{color:var(--now);}
.cd-report-title{font-family:var(--serif);font-size:44px;line-height:1.05;
  letter-spacing:-0.01em;font-weight:400;margin:0;text-wrap:balance;color:var(--text);}
.cd-report-title em{font-style:italic;color:var(--then);}
.cd-report-title .arr{color:var(--now);font-style:normal;}
.cd-report-meta{font-family:var(--mono);font-size:10.5px;color:var(--text-3);
  letter-spacing:.06em;text-align:right;line-height:1.9;}
.cd-report-meta .v{color:var(--text);}

/* ─ Findings ─ */
.cd-finding{border:1px solid var(--border);border-radius:14px;background:var(--surface);
  padding:26px 30px;margin-bottom:16px;}
.cd-finding-num{font-family:var(--mono);font-size:11px;letter-spacing:.18em;
  text-transform:uppercase;color:var(--now);margin-bottom:6px;}
.cd-finding-title{font-family:var(--serif);font-size:26px;color:var(--text);
  font-weight:500;margin:0 0 10px;letter-spacing:-0.01em;}
.cd-finding-desc{font-size:14px;line-height:1.7;color:var(--text-2);
  max-width:720px;margin:0 0 22px;padding-bottom:20px;border-bottom:1px dashed var(--border);}

/* Language shift rows */
.cd-lang-then{background:linear-gradient(180deg,rgba(195,154,106,.04),transparent);
  border:1px solid #2a2218;border-radius:10px;padding:18px 20px;}
.cd-lang-now{background:linear-gradient(180deg,rgba(94,161,255,.06),transparent);
  border:1px solid #1a2a44;border-radius:10px;padding:18px 20px;}
.cd-lang-period{font-family:var(--mono);font-size:10px;letter-spacing:.16em;
  text-transform:uppercase;margin-bottom:10px;}
.cd-lang-then .cd-lang-period{color:var(--then);}
.cd-lang-now  .cd-lang-period{color:var(--now);}
.cd-lang-quote{font-family:var(--serif);font-size:18px;line-height:1.45;color:var(--text);}
.cd-lang-then .cd-lang-quote{font-style:italic;color:#c9b69a;opacity:.9;}
.cd-lang-now  .cd-lang-quote{font-weight:500;}
.cd-lang-arrow{display:flex;flex-direction:column;align-items:center;justify-content:center;
  height:100%;padding:0 4px;}
.cd-lang-arrow .arr-line{width:100%;height:1px;
  background:linear-gradient(90deg,var(--then),var(--now));position:relative;}
.cd-lang-arrow .arr-line::after{content:'▸';position:absolute;right:-3px;top:-9px;
  color:var(--now);font-size:13px;}
.cd-lang-arrow .yrs{font-family:var(--mono);font-size:9.5px;color:var(--text-4);
  letter-spacing:.08em;display:flex;justify-content:space-between;width:100%;margin-top:4px;}
.cd-lang-sig{padding:14px 4px 18px;font-size:13.5px;line-height:1.75;color:var(--text-2);
  border-bottom:1px dashed var(--border);margin-bottom:14px;}
.cd-lang-sig::before{content:'Significance —';font-family:var(--mono);font-size:10px;
  letter-spacing:.16em;text-transform:uppercase;color:var(--text-4);margin-right:10px;}

/* Value items */
.cd-value{display:grid;grid-template-columns:28px 1fr;gap:14px;padding:14px 16px;
  background:var(--ink-2);border:1px solid var(--border);border-radius:8px;margin-bottom:10px;}
.cd-value .vnum{font-family:var(--mono);font-size:11px;color:var(--now);padding-top:2px;}
.cd-value .vtitle{font-family:var(--serif);font-size:17px;color:var(--text);
  font-weight:500;margin-bottom:4px;}
.cd-value .vev{font-size:13px;color:var(--text-3);line-height:1.7;font-style:italic;}
.cd-value .vev::before{content:'“';color:var(--text-4);margin-right:4px;}
.cd-value .vev::after{content:'”';color:var(--text-4);margin-left:4px;}

/* Behavior tags */
.cd-tag-new{display:inline-flex;align-items:center;gap:8px;font-size:13px;padding:8px 14px;
  border-radius:999px;background:rgba(94,201,141,.06);border:1px solid #234436;color:#9adcb6;
  margin:3px;}
.cd-tag-new::before{content:'＋';color:var(--signal);font-weight:600;}
.cd-tag-faded{display:inline-flex;align-items:center;gap:8px;font-size:13px;padding:8px 14px;
  border-radius:999px;background:var(--ink-2);border:1px solid var(--border);color:var(--text-3);
  text-decoration:line-through;text-decoration-color:var(--border-2);margin:3px;}
.cd-tag-faded::before{content:'−';color:var(--text-4);font-weight:600;text-decoration:none;}

/* Forward + Opportunity */
.cd-forward{border:1px solid #234436;border-radius:14px;padding:22px 28px;margin-bottom:16px;
  background:linear-gradient(180deg,rgba(94,201,141,.05),transparent 60%);
  position:relative;overflow:hidden;}
.cd-forward::before{content:'';position:absolute;left:0;top:0;bottom:0;width:3px;
  background:linear-gradient(180deg,var(--signal),transparent);}
.cd-forward-eyebrow{font-family:var(--mono);font-size:11px;letter-spacing:.2em;
  text-transform:uppercase;color:var(--signal);margin-bottom:10px;}
.cd-forward-title{font-family:var(--serif);font-size:26px;color:var(--text);
  font-weight:500;margin:0 0 14px;letter-spacing:-0.01em;}
.cd-forward-body{
  font-family:var(--sans);
  font-size:14px;
  line-height:1.65;
  color:var(--text-2);
  max-width:820px;
  text-wrap:pretty;
}

.cd-opp{border:1px solid #1a2e4a;border-radius:14px;padding:22px 28px;margin-bottom:16px;
  background:linear-gradient(180deg,rgba(94,161,255,.05),transparent 60%);
  position:relative;overflow:hidden;}
.cd-opp::before{content:'';position:absolute;left:0;top:0;bottom:0;width:3px;
  background:linear-gradient(180deg,var(--now),transparent);}
.cd-opp-eyebrow{font-family:var(--mono);font-size:11px;letter-spacing:.2em;
  text-transform:uppercase;color:var(--now);margin-bottom:10px;}
.cd-opp-title{font-family:var(--serif);font-size:26px;color:var(--text);
  font-weight:500;margin:0 0 14px;letter-spacing:-0.01em;}
.cd-opp-body{
  font-family:var(--sans);
  font-size:14px;
  line-height:1.65;
  color:var(--text-2);
  max-width:820px;
  text-wrap:pretty;
}

/* Reddit warning */
.cd-warn{background:#1F1800;border:1px solid #3A2E00;border-radius:8px;
  padding:12px 16px;margin-bottom:14px;font-size:13px;color:#BBAA44;
  font-family:var(--sans);}

/* TL;DR */
.cd-tldr{display:grid;grid-template-columns:200px 1fr;gap:40px;padding:14px 0 30px;}
.cd-tldr-aside{font-family:var(--mono);font-size:10px;letter-spacing:.2em;
  text-transform:uppercase;color:var(--text-3);padding-top:6px;}
.cd-tldr-body{font-family:var(--serif);font-size:21px;line-height:1.5;color:var(--text);text-wrap:pretty;}
.cd-tldr-body em{font-style:italic;color:var(--then);}
.cd-tldr-body b{font-weight:500;color:var(--now);font-style:normal;}

/* Footer */
.cd-foot{margin-top:60px;padding-top:24px;border-top:1px solid var(--border);
  display:flex;justify-content:space-between;
  font-family:var(--mono);font-size:10.5px;color:var(--text-4);letter-spacing:.08em;}
.cd-foot .builder{color:var(--text-3);}
.cd-foot .builder a{color:var(--text);text-decoration:none;border-bottom:1px solid var(--border-2);}
.cd-foot .builder a:hover{color:var(--now);border-bottom-color:var(--now);}

[data-testid="column"]{padding:0 .4rem!important;}
hr{border-color:var(--border)!important;margin:1.5rem 0!important;}
</style>
""", unsafe_allow_html=True)

# ── Top bar ───────────────────────────────────────────────────────────────
current_usage = get_usage()
st.markdown(f"""
<div class="cd-topbar">
  <div class="cd-brand">
    <div class="cd-brand-mark">Δ · CD-04</div>
    <div class="cd-brand-name">Culture<em>Delta</em></div>
  </div>
  <div class="cd-status">
    <div class="cd-stat"><span class="k">model</span><span class="v">haiku-4-5</span></div>
    <div class="cd-stat"><span class="k">agents</span><span class="v">3 · parallel</span></div>
    <div class="cd-stat"><span class="k">tools</span><span class="v">tavily · reddit</span></div>
    <div class="cd-stat"><span class="dot"></span><span class="v">standby</span></div>
  </div>
</div>
""", unsafe_allow_html=True)

# ── Hero ──────────────────────────────────────────────────────────────────
st.markdown("""
<div class="cd-eyebrow"><span class="glyph">Δ</span>Cultural drift analysis · v0.4</div>
<h1 class="cd-title">Map how <em>markets</em> and <em>culture</em> <span class="arr">▸</span> shift over time.</h1>
<p class="cd-lede">Most market research gives you a snapshot. CultureDelta gives you the <span class="accent">trajectory</span> — the language, values, and behaviors that drifted between two points in time, and the forward signal those shifts reveal.</p>
""", unsafe_allow_html=True)

# ── Console (input) ───────────────────────────────────────────────────────
st.markdown("""
<div class="cd-console">
  <div class="cd-console-head">
    <div style="display:flex;align-items:center;gap:12px;">
      <div class="cd-lights"><span class="on"></span><span></span><span></span></div>
      <div class="cd-console-tag">Δ · Two-period analyzer</div>
    </div>
    <div class="cd-console-r">SESSION 0xCD-04 · READY</div>
  </div>
  <div class="cd-console-body">
""", unsafe_allow_html=True)

col1, col2, col_arr, col3, col4 = st.columns([5, 1.2, 0.4, 1.2, 1.8])

with col1:
    topic = st.text_input("Subject of inquiry",
                          placeholder="e.g. athletic wear, remote work, crypto, fast food")
with col2:
    st.markdown('<div class="cd-then">', unsafe_allow_html=True)
    year_from = st.text_input("Then", value="2019", max_chars=4)
    st.markdown('</div>', unsafe_allow_html=True)
with col_arr:
    st.markdown('<div class="cd-arrow-cell"><div class="arr-line"></div></div>', unsafe_allow_html=True)
with col3:
    st.markdown('<div class="cd-now">', unsafe_allow_html=True)
    year_to = st.text_input("Now", value="2025", max_chars=4)
    st.markdown('</div>', unsafe_allow_html=True)
with col4:
    run_button = st.button("Run delta analysis  ▸", type="primary")

st.markdown("</div>", unsafe_allow_html=True)  # close console-body

# Console foot — example chips + quota
EXAMPLES = [
    ("remote work", "2019", "2024"),
    ("crypto", "2017", "2023"),
    ("fast food", "2015", "2025"),
    ("luxury fashion", "2010", "2024"),
    ("social media", "2015", "2025"),
]
chips_html = "".join(
    f'<span class="cd-chip">{t} <span class="from">{f}</span> → <span class="to">{to}</span></span>'
    for t, f, to in EXAMPLES
)
st.markdown(f"""
  <div class="cd-console-foot">
    <div class="cd-chips">{chips_html}</div>
    <div>QUOTA · {current_usage} / {DAILY_LIMIT} today</div>
  </div>
</div>
""", unsafe_allow_html=True)

pct = int((current_usage / DAILY_LIMIT) * 100)
st.markdown(f"""
<div class="cd-quota">
  <span>DAILY ANALYSES</span>
  <span class="bar"><i style="width:{pct}%;"></i></span>
  <span>RESETS 00:00 UTC</span>
</div>
""", unsafe_allow_html=True)

# ─────────────────────────────────────────────────────────────────────────
if run_button:
    if not topic:
        st.warning("Please enter a topic.")
        st.stop()
    if not year_from or not year_to:
        st.warning("Please enter both years.")
        st.stop()
    if year_from == year_to:
        st.warning("Please enter two different years.")
        st.stop()
    if current_usage >= DAILY_LIMIT:
        st.error(f"Daily limit of {DAILY_LIMIT} analyses reached. Come back tomorrow.")
        st.stop()

    try:
        if int(year_from) < 2006:
            st.markdown(
                '<div class="cd-warn"><strong>⚠ Note:</strong> Reddit launched in 2005. '
                'For years before 2006, Reddit data will be limited. Tavily web search '
                'will still cover news archives and publications from that era.</div>',
                unsafe_allow_html=True
            )
    except ValueError:
        pass

    # Section header
    st.markdown(f"""
    <div class="cd-rule">
      <div class="label"><span>§</span>Analyzing</div>
      <div class="line"></div>
      <div class="meta">{topic} · {year_from} → {year_to}</div>
    </div>
    """, unsafe_allow_html=True)

    progress_placeholder = st.empty()

    def render_steps(active_step):
        steps = [
            ("01", "Parallel Research",
             f"Two Claude agents launch simultaneously via ThreadPoolExecutor — "
             f"one researches {year_from}, the other {year_to}. Each autonomously "
             "calls Tavily and Reddit tools."),
            ("02", "Delta Synthesis",
             "A third Claude call receives both summaries. No new API calls — "
             "pure reasoning. Maps language, value, and behavior shifts between "
             "the two periods."),
            ("03", "Forward Signal",
             "Extracts a 2-year forward read from the detected trajectory — "
             "where this is heading and the specific opening the drift reveals."),
        ]
        cards = []
        for i, (num, title, desc) in enumerate(steps):
            step_num = i + 1
            if step_num == active_step:
                cls, status = "active", "Running…"
            elif step_num < active_step:
                cls, status = "done", "Complete"
            else:
                cls, status = "", "Waiting"
            cards.append(
                f'<div class="cd-pipe-step {cls}">'
                f'  <div class="cd-pipe-num">Step {num}</div>'
                f'  <div class="cd-pipe-title">{title}</div>'
                f'  <div class="cd-pipe-desc">{desc}</div>'
                f'  <div class="cd-pipe-status">{status}</div>'
                f'</div>'
            )
        progress_placeholder.markdown(
            f'<div class="cd-pipe">{"".join(cards)}</div>',
            unsafe_allow_html=True
        )

    result = run_culture_delta(topic, year_from, year_to, progress_callback=render_steps)
    increment_usage()
    progress_placeholder.empty()

    if "error" in result:
        st.error("Something went wrong: " + result.get("error", ""))
        if "raw" in result:
            st.code(result["raw"])
        st.stop()

    # ── REPORT ───────────────────────────────────────────────────────────
    today = datetime.date.today().strftime("%b %d, %Y")
    st.markdown(f"""
    <div class="cd-masthead">
      <div>
        <div class="cd-report-eyebrow"><span>Δ · Report 0xCD-04 · {today}</span></div>
        <h1 class="cd-report-title"><em>{topic}</em> <span class="arr">▸</span> a {abs(int(year_to)-int(year_from))}-year drift</h1>
      </div>
      <div class="cd-report-meta">
        PERIOD <span class="v">{year_from} → {year_to}</span><br/>
        MODEL <span class="v">claude-haiku-4-5</span><br/>
        TOOLS <span class="v">tavily · reddit</span>
      </div>
    </div>
    """, unsafe_allow_html=True)

    # ── Language shifts ──────────────────────────────────────────────────
    language_shifts = result.get("language_shifts", [])
    if language_shifts:
        st.markdown(f"""
        <div class="cd-rule">
          <div class="label"><span>§ 01</span>Language</div>
          <div class="line"></div>
          <div class="meta">{len(language_shifts)} shifts detected</div>
        </div>
        <div class="cd-finding">
          <div class="cd-finding-num">Findings · 01</div>
          <h2 class="cd-finding-title">When the words change, the values already have.</h2>
          <p class="cd-finding-desc">How the vocabulary around {topic} drifted between {year_from} and {year_to}. Language shifts are early signals of deeper cultural change.</p>
        </div>
        """, unsafe_allow_html=True)

        for shift in language_shifts:
            then_lang = shift.get("then", "")
            now_lang = shift.get("now", "")
            significance = shift.get("significance", "")

            c_then, c_arr, c_now = st.columns([5, 1, 5])
            with c_then:
                st.markdown(
                    f'<div class="cd-lang-then">'
                    f'  <div class="cd-lang-period">Then — {year_from}</div>'
                    f'  <div class="cd-lang-quote">{then_lang}</div>'
                    f'</div>', unsafe_allow_html=True
                )
            with c_arr:
                st.markdown(
                    f'<div class="cd-lang-arrow">'
                    f'  <div class="arr-line"></div>'
                    f'  <div class="yrs"><span>{year_from}</span><span>{year_to}</span></div>'
                    f'</div>', unsafe_allow_html=True
                )
            with c_now:
                st.markdown(
                    f'<div class="cd-lang-now">'
                    f'  <div class="cd-lang-period">Now — {year_to}</div>'
                    f'  <div class="cd-lang-quote">{now_lang}</div>'
                    f'</div>', unsafe_allow_html=True
                )
            if significance:
                st.markdown(f'<div class="cd-lang-sig">{significance}</div>', unsafe_allow_html=True)

    # ── Value shifts ─────────────────────────────────────────────────────
    value_shifts = result.get("value_shifts", [])
    if value_shifts:
        st.markdown(f"""
        <div class="cd-rule">
          <div class="label"><span>§ 02</span>Values</div>
          <div class="line"></div>
          <div class="meta">{len(value_shifts)} shifts detected</div>
        </div>
        <div class="cd-finding">
          <div class="cd-finding-num">Findings · 02</div>
          <h2 class="cd-finding-title">What people stopped wanting. What they want instead.</h2>
          <p class="cd-finding-desc">Underneath language, what people fundamentally cared about, feared, or valued — and how those attitudes evolved.</p>
        """, unsafe_allow_html=True)

        for i, vs in enumerate(value_shifts, 1):
            st.markdown(
                f'<div class="cd-value">'
                f'  <div class="vnum">0{i}</div>'
                f'  <div>'
                f'    <div class="vtitle">{vs.get("shift","")}</div>'
                f'    <div class="vev">{vs.get("evidence","")}</div>'
                f'  </div>'
                f'</div>', unsafe_allow_html=True
            )
        st.markdown('</div>', unsafe_allow_html=True)

    # ── Emerged + Faded ──────────────────────────────────────────────────
    new_behaviors = result.get("new_behaviors", [])
    faded_behaviors = result.get("faded_behaviors", [])

    if new_behaviors or faded_behaviors:
        st.markdown(f"""
        <div class="cd-rule">
          <div class="label"><span>§ 03</span>Behaviors</div>
          <div class="line"></div>
          <div class="meta">{len(new_behaviors)} emerged · {len(faded_behaviors)} faded</div>
        </div>
        """, unsafe_allow_html=True)

        col_new, col_faded = st.columns(2)
        with col_new:
            new_tags = "".join(f'<span class="cd-tag-new">{b}</span>' for b in new_behaviors)
            st.markdown(f"""
            <div class="cd-finding">
              <div class="cd-finding-num">Findings · 03</div>
              <h2 class="cd-finding-title">Emerged in {year_to}</h2>
              <p class="cd-finding-desc">New behaviors that didn't exist or weren't mainstream in {year_from} — the new normal.</p>
              <div>{new_tags}</div>
            </div>
            """, unsafe_allow_html=True)

        with col_faded:
            faded_tags = "".join(f'<span class="cd-tag-faded">{b}</span>' for b in faded_behaviors)
            st.markdown(f"""
            <div class="cd-finding">
              <div class="cd-finding-num">Findings · 04</div>
              <h2 class="cd-finding-title">Faded since {year_from}</h2>
              <p class="cd-finding-desc">Common or dominant in {year_from} — significantly declined or gone. What faded matters as much as what emerged.</p>
              <div>{faded_tags}</div>
            </div>
            """, unsafe_allow_html=True)

    # ── Forward Signal ───────────────────────────────────────────────────
    forward_signal = result.get("forward_signal", "")
    opportunity = result.get("opportunity", "")

    if forward_signal or opportunity:
        st.markdown("""
        <div class="cd-rule">
          <div class="label"><span>§ 04</span>Forward</div>
          <div class="line"></div>
          <div class="meta">2-year horizon · trajectory + opportunity</div>
        </div>
        """, unsafe_allow_html=True)

    if forward_signal:
        st.markdown(f"""
        <div class="cd-forward">
          <div class="cd-forward-eyebrow">Forward signal</div>
          <h2 class="cd-forward-title">Where this is heading.</h2>
          <p class="cd-forward-body">{forward_signal}</p>
        </div>
        """, unsafe_allow_html=True)

    if opportunity:
        st.markdown(f"""
        <div class="cd-opp">
          <div class="cd-opp-eyebrow">The opportunity</div>
          <h2 class="cd-opp-title">The opening the drift reveals.</h2>
          <p class="cd-opp-body">{opportunity}</p>
        </div>
        """, unsafe_allow_html=True)

else:
    # ── Empty state: How it works ────────────────────────────────────────
    st.markdown("""
    <div class="cd-rule">
      <div class="label"><span>§</span>Architecture</div>
      <div class="line"></div>
      <div class="meta">3 agents · 1 synthesis pass · ~14s typical</div>
    </div>
    """, unsafe_allow_html=True)

    c1, c2, c3 = st.columns(3)
    with c1:
        st.markdown("""
        <div class="cd-how">
          <div class="cd-how-step">Step 01 · Parallel research</div>
          <h3 class="cd-how-title">Two researchers, one clock</h3>
          <p class="cd-how-desc">A Claude agent for <em style="color:var(--then);font-style:italic;">then</em> and another for <b style="color:var(--now);">now</b> run side-by-side via Python's ThreadPoolExecutor, each calling Tavily and Reddit tools autonomously.</p>
          <div class="cd-how-tech">
            <span class="cd-pill">ThreadPoolExecutor</span>
            <span class="cd-pill">Tavily API</span>
            <span class="cd-pill">Reddit API</span>
            <span class="cd-pill">Claude tool-use</span>
          </div>
        </div>
        """, unsafe_allow_html=True)
    with c2:
        st.markdown("""
        <div class="cd-how">
          <div class="cd-how-step">Step 02 · Delta synthesis</div>
          <h3 class="cd-how-title">A reasoning pass, no extra calls</h3>
          <p class="cd-how-desc">A third Claude call receives both research summaries and maps the exact shifts in language, values, and behavior between the two periods — pure reasoning, structured JSON out.</p>
          <div class="cd-how-tech">
            <span class="cd-pill">claude-haiku-4-5</span>
            <span class="cd-pill">Structured JSON</span>
            <span class="cd-pill">Chain-of-thought</span>
          </div>
        </div>
        """, unsafe_allow_html=True)
    with c3:
        st.markdown("""
        <div class="cd-how">
          <div class="cd-how-step">Step 03 · Forward signal</div>
          <h3 class="cd-how-title">Where this is heading</h3>
          <p class="cd-how-desc">From the detected trajectory, the synthesis agent extracts a 2-year forward read and the specific opening the drift creates — for brands, investors, or builders moving before the market catches up.</p>
          <div class="cd-how-tech">
            <span class="cd-pill">Trajectory framing</span>
            <span class="cd-pill">Opportunity sizing</span>
          </div>
        </div>
        """, unsafe_allow_html=True)

# ── Page footer ───────────────────────────────────────────────────────────
st.markdown("""
<div class="cd-foot">
  <div class="builder">Δ &nbsp; Built by <a href="https://linkedin.com/in/enriquechernandez" target="_blank">Enrique C. Hernandez</a> · Python · Streamlit · Claude · Tavily · Reddit</div>
  <div>v0.4 · OPEN SOURCE</div>
</div>
""", unsafe_allow_html=True)
