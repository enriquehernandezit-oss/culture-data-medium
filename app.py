import streamlit as st
from agent import run_culture_delta

st.set_page_config(
    page_title="CultureDelta",
    page_icon="📊",
    layout="wide"
)

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=IBM+Plex+Mono:wght@400;500&family=IBM+Plex+Sans:wght@300;400;500;600;700&display=swap');

html, body, [class*="css"] {
    font-family: 'IBM Plex Sans', sans-serif;
    background-color: #111111;
    color: #CCCCCC;
}
.stApp { background-color: #111111; }
#MainMenu {visibility: hidden;}
footer {visibility: hidden;}
header {visibility: hidden;}

.block-container {
    padding: 3.5rem 4rem;
    max-width: 1300px;
}

h1 {
    font-family: 'IBM Plex Sans', sans-serif !important;
    font-size: 2.8rem !important;
    font-weight: 700 !important;
    color: #FFFFFF !important;
    letter-spacing: -0.02em !important;
    text-transform: none !important;
    margin-bottom: 0 !important;
}

h3 {
    font-family: 'IBM Plex Sans', sans-serif !important;
    font-size: 1rem !important;
    font-weight: 300 !important;
    color: #666666 !important;
    margin-top: 0.25rem !important;
}

.stTextInput label {
    font-family: 'IBM Plex Sans', sans-serif !important;
    font-size: 0.7rem !important;
    font-weight: 600 !important;
    color: #666666 !important;
    text-transform: uppercase !important;
    letter-spacing: 0.1em !important;
}

.stTextInput > div > div > input {
    background-color: #1A1A1A !important;
    border: 1px solid #2A2A2A !important;
    border-radius: 6px !important;
    color: #FFFFFF !important;
    font-family: 'IBM Plex Sans', sans-serif !important;
    font-size: 0.95rem !important;
    padding: 0 1rem !important;
    height: 44px !important;
    line-height: 44px !important;
}
.stTextInput > div > div > input:focus {
    border-color: #4A90E2 !important;
    box-shadow: 0 0 0 2px rgba(74,144,226,0.1) !important;
}
.stTextInput > div > div > input::placeholder {
    color: #444444 !important;
    font-style: italic !important;
}

.stButton > button {
    background-color: #4A90E2 !important;
    color: #FFFFFF !important;
    border: none !important;
    border-radius: 6px !important;
    font-family: 'IBM Plex Sans', sans-serif !important;
    font-weight: 600 !important;
    font-size: 0.9rem !important;
    height: 44px !important;
    width: 100% !important;
    margin-top: 24px !important;
}
.stButton > button:hover {
    background-color: #357ABD !important;
}

hr {
    border-color: #1E1E1E !important;
    margin: 2.5rem 0 !important;
}

.result-card {
    background: #181818;
    border: 1px solid #222222;
    border-radius: 10px;
    padding: 1.75rem 2rem;
    margin-bottom: 1.5rem;
}

.result-card-label {
    font-family: 'IBM Plex Mono', monospace;
    font-size: 0.62rem;
    font-weight: 500;
    color: #4A90E2;
    text-transform: uppercase;
    letter-spacing: 0.12em;
    margin-bottom: 0.5rem;
}

.result-card-title {
    font-size: 1.2rem;
    font-weight: 700;
    color: #FFFFFF;
    margin-bottom: 0.5rem;
}

.result-card-desc {
    font-size: 0.92rem;
    color: #666666;
    line-height: 1.75;
    margin-bottom: 1.5rem;
    padding-bottom: 1.25rem;
    border-bottom: 1px solid #222222;
}

.then-col {
    background: #141414;
    border: 1px solid #222222;
    border-radius: 8px;
    padding: 1.1rem 1.25rem;
}

.now-col {
    background: #141E2A;
    border: 1px solid #1E3050;
    border-radius: 8px;
    padding: 1.1rem 1.25rem;
}

.col-period {
    font-family: 'IBM Plex Mono', monospace;
    font-size: 0.62rem;
    font-weight: 500;
    text-transform: uppercase;
    letter-spacing: 0.12em;
    margin-bottom: 0.5rem;
}
.col-then { color: #555555; }
.col-now { color: #4A90E2; }

.col-text-then {
    font-size: 1rem;
    color: #888888;
    line-height: 1.6;
}

.col-text-now {
    font-size: 1rem;
    color: #E8E8E8;
    font-weight: 500;
    line-height: 1.6;
}

.significance {
    font-size: 0.82rem;
    color: #888888;
    font-style: normal;
}

.value-item {
    background: #141414;
    border-left: 3px solid #4A90E2;
    border-radius: 0 6px 6px 0;
    padding: 0.9rem 1.1rem;
    margin-bottom: 0.6rem;
}

.value-title {
    font-size: 1rem;
    font-weight: 600;
    color: #E8E8E8;
    margin-bottom: 0.3rem;
}

.value-evidence {
    font-size: 0.88rem;
    color: #666666;
    font-style: italic;
    line-height: 1.6;
}

.tag-new {
    display: inline-block;
    background: #0D1F0D;
    color: #4CAF50;
    border: 1px solid #1E4020;
    border-radius: 4px;
    font-size: 0.85rem;
    font-weight: 500;
    padding: 0.3rem 0.8rem;
    margin: 0.2rem;
}

.tag-faded {
    display: inline-block;
    background: #181818;
    color: #555555;
    border: 1px solid #2A2A2A;
    border-radius: 4px;
    font-size: 0.85rem;
    padding: 0.3rem 0.8rem;
    margin: 0.2rem;
}

.forward-box {
    background: #0D1A0D;
    border: 1px solid #1A3020;
    border-left: 3px solid #4CAF50;
    border-radius: 8px;
    padding: 1.75rem 2rem;
    margin-bottom: 1.5rem;
}

.forward-label-tag {
    font-family: 'IBM Plex Mono', monospace;
    font-size: 0.62rem;
    font-weight: 500;
    color: #4CAF50;
    text-transform: uppercase;
    letter-spacing: 0.12em;
    margin-bottom: 0.4rem;
}

.forward-title {
    font-size: 1.2rem;
    font-weight: 700;
    color: #FFFFFF;
    margin-bottom: 0.4rem;
}

.forward-subdesc {
    font-size: 0.92rem;
    color: #555555;
    line-height: 1.75;
    margin-bottom: 1.25rem;
    padding-bottom: 1.25rem;
    border-bottom: 1px solid #1A3020;
}

.opportunity-box {
    background: #0D1525;
    border: 1px solid #1A2E4A;
    border-left: 3px solid #4A90E2;
    border-radius: 8px;
    padding: 1.75rem 2rem;
    margin-bottom: 1.5rem;
}

.opportunity-label-tag {
    font-family: 'IBM Plex Mono', monospace;
    font-size: 0.62rem;
    font-weight: 500;
    color: #4A90E2;
    text-transform: uppercase;
    letter-spacing: 0.12em;
    margin-bottom: 0.4rem;
}

.opportunity-title {
    font-size: 1.2rem;
    font-weight: 700;
    color: #FFFFFF;
    margin-bottom: 0.4rem;
}

.opportunity-subdesc {
    font-size: 0.92rem;
    color: #555555;
    line-height: 1.75;
    margin-bottom: 1.25rem;
    padding-bottom: 1.25rem;
    border-bottom: 1px solid #1A2E4A;
}

.box-text {
    font-size: 1rem;
    color: #DDDDDD;
    line-height: 1.85;
}

.delta-definition {
    background: #181818;
    border: 1px solid #222222;
    border-left: 3px solid #4A90E2;
    border-radius: 8px;
    padding: 1.75rem 2rem;
    margin-bottom: 2.5rem;
}

.step-card {
    background: #181818;
    border: 1px solid #222222;
    border-radius: 10px;
    padding: 1.5rem 1.75rem;
    height: 100%;
}

.step-num {
    font-family: 'IBM Plex Mono', monospace;
    font-size: 0.62rem;
    font-weight: 500;
    color: #4A90E2;
    text-transform: uppercase;
    letter-spacing: 0.12em;
    margin-bottom: 0.6rem;
}

.step-title {
    font-size: 1rem;
    font-weight: 700;
    color: #FFFFFF;
    margin-bottom: 0.6rem;
}

.step-desc {
    font-size: 0.83rem;
    color: #777777;
    line-height: 1.75;
}

.step-tech {
    font-family: 'IBM Plex Mono', monospace;
    font-size: 0.65rem;
    color: #4A90E2;
    margin-top: 1rem;
    padding-top: 0.75rem;
    border-top: 1px solid #222222;
    line-height: 1.6;
}

.example-tag {
    display: inline-block;
    background: #181818;
    border: 1px solid #222222;
    border-radius: 4px;
    font-size: 0.78rem;
    color: #666666;
    padding: 0.3rem 0.8rem;
    margin: 0.2rem;
    font-family: 'IBM Plex Mono', monospace;
}

.results-bar {
    background: #181818;
    border: 1px solid #222222;
    border-radius: 8px;
    padding: 1rem 1.5rem;
    margin-bottom: 2rem;
}

.reddit-warning {
    background: #1F1800;
    border: 1px solid #3A2E00;
    border-radius: 6px;
    padding: 0.75rem 1rem;
    margin-bottom: 1rem;
    font-size: 0.82rem;
    color: #BBAA44;
}

[data-testid="column"] { padding: 0 0.5rem !important; }
</style>
""", unsafe_allow_html=True)

# ── Header ────────────────────────────────────────────────────────────────
st.markdown('<h1>CultureDelta</h1>', unsafe_allow_html=True)
st.markdown("<h3>Map how markets and culture shift over time.</h3>",
            unsafe_allow_html=True)
st.markdown('<hr>', unsafe_allow_html=True)

# ── Inputs ────────────────────────────────────────────────────────────────
col1, col2, col3, col4 = st.columns([5, 1.2, 1.2, 1.8])

with col1:
    topic = st.text_input(
        "Topic",
        placeholder="e.g. athletic wear, remote work, crypto, fast food"
    )

with col2:
    year_from = st.text_input("From year", value="2019")

with col3:
    year_to = st.text_input("To year", value="2025")

with col4:
    run_button = st.button("Analyze Shift →", type="primary")

# ── Logic ─────────────────────────────────────────────────────────────────
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

    try:
        if int(year_from) < 2006:
            st.markdown(
                '<div class="reddit-warning">'
                '⚠️ <strong>Note:</strong> Reddit launched in 2005. '
                'For years before 2006, Reddit data will be limited. '
                'Tavily web search will still cover news archives and '
                'publications from that era.'
                '</div>',
                unsafe_allow_html=True
            )
    except ValueError:
        pass

    st.markdown('<hr>', unsafe_allow_html=True)

    progress_placeholder = st.empty()

    def render_steps(active_step):
        steps = [
            ("01", "Parallel Research",
             "Two Claude agents running simultaneously via Python ThreadPoolExecutor — "
             "one calls Tavily API + Reddit API for " + year_from + ", "
             "the other does the same for " + year_to + ". "
             "Claude autonomously decides what to search using native tool use."),
            ("02", "Delta Synthesis",
             "A third Claude call receives both agents' full research summaries. "
             "No additional API calls — pure reasoning. Claude maps language shifts, "
             "value changes, new and faded behaviors between the two periods."),
            ("03", "Forward Signal",
             "The synthesis agent extracts a forward-looking signal from the detected "
             "trajectory — where this market is heading and the specific opportunity "
             "the cultural drift reveals for brands, investors, or builders."),
        ]

        html = '<div style="display:flex; gap:1rem; margin:2rem 0;">'
        for i, (num, title, desc) in enumerate(steps):
            step_num = i + 1
            if step_num == active_step:
                bg = "#1A2A3A"
                border = "border:2px solid #4A90E2;"
                num_color = "#4A90E2"
                title_color = "#FFFFFF"
                desc_color = "#AAAAAA"
                status = '<div style="margin-top:1.25rem; font-size:0.7rem; color:#4A90E2; font-family:IBM Plex Mono,monospace; letter-spacing:0.05em;">● Running...</div>'
            elif step_num < active_step:
                bg = "#111A11"
                border = "border:2px solid #4CAF50;"
                num_color = "#4CAF50"
                title_color = "#888888"
                desc_color = "#555555"
                status = '<div style="margin-top:1.25rem; font-size:0.7rem; color:#4CAF50; font-family:IBM Plex Mono,monospace; letter-spacing:0.05em;">✓ Complete</div>'
            else:
                bg = "#141414"
                border = "border:2px solid #222222;"
                num_color = "#333333"
                title_color = "#3A3A3A"
                desc_color = "#2A2A2A"
                status = '<div style="margin-top:1.25rem; font-size:0.7rem; color:#333333; font-family:IBM Plex Mono,monospace; letter-spacing:0.05em;">○ Waiting</div>'

            html += (
                '<div style="flex:1; background:' + bg + '; ' + border +
                ' border-radius:10px; padding:1.75rem; min-height:240px;">'
                '<div style="font-family:IBM Plex Mono,monospace; font-size:0.62rem; '
                'color:' + num_color + '; text-transform:uppercase; '
                'letter-spacing:0.15em; margin-bottom:0.75rem;">Step ' + num + '</div>'
                '<div style="font-size:1rem; color:' + title_color + '; '
                'font-weight:700; margin-bottom:0.75rem;">' + title + '</div>'
                '<div style="font-size:0.78rem; color:' + desc_color + '; '
                'line-height:1.7;">' + desc + '</div>'
                + status +
                '</div>'
            )
        html += '</div>'
        progress_placeholder.markdown(html, unsafe_allow_html=True)

    result = run_culture_delta(
        topic, year_from, year_to,
        progress_callback=render_steps
    )
    progress_placeholder.empty()

    if "error" in result:
        st.error("Something went wrong: " + result.get("error", ""))
        if "raw" in result:
            st.code(result["raw"])
        st.stop()

    # ── Results bar ───────────────────────────────────────────────────────
    st.markdown(
        '<div class="results-bar">'
        '<span style="font-family:IBM Plex Mono,monospace; font-size:0.62rem; '
        'color:#444; text-transform:uppercase; letter-spacing:0.12em;">Analysis complete</span>'
        '<span style="color:#2A2A2A; margin:0 0.75rem;">|</span>'
        '<span style="font-family:IBM Plex Mono,monospace; font-size:0.62rem; '
        'color:#4A90E2; text-transform:uppercase; letter-spacing:0.1em; font-weight:600;">'
        + topic.upper() + '</span>'
        '<span style="font-family:IBM Plex Mono,monospace; font-size:0.62rem; '
        'color:#444; margin:0 0.5rem;">·</span>'
        '<span style="font-family:IBM Plex Mono,monospace; font-size:0.62rem; '
        'color:#666; letter-spacing:0.05em;">'
        + year_from + ' → ' + year_to + '</span>'
        '</div>',
        unsafe_allow_html=True
    )

    # ── Language shifts ───────────────────────────────────────────────────
    language_shifts = result.get("language_shifts", [])
    if language_shifts:
        st.markdown(
            '<div class="result-card">'
            '<div class="result-card-label">Findings · 01</div>'
            '<div class="result-card-title">Language Shifts</div>'
            '<div class="result-card-desc">How the words, phrases, and vocabulary '
            'people used to describe this topic changed between ' + year_from + ' and '
            + year_to + '. Language shifts are early signals of deeper cultural change '
            '— when the words change, the values behind them are already shifting.</div>',
            unsafe_allow_html=True
        )
        for shift in language_shifts:
            then_lang = shift.get("then", "")
            now_lang = shift.get("now", "")
            significance = shift.get("significance", "")

            col_then, col_arrow, col_now = st.columns([5, 1, 5])
            with col_then:
                st.markdown(
                    '<div class="then-col">'
                    '<div class="col-period col-then">Then — ' + year_from + '</div>'
                    '<div class="col-text-then">' + then_lang + '</div>'
                    '</div>',
                    unsafe_allow_html=True
                )
            with col_arrow:
                st.markdown(
                    '<div style="display:flex; align-items:center; '
                    'justify-content:center; height:100%; padding-top:0.5rem;">'
                    '<span style="color:#4A90E2; font-size:1.1rem;">→</span>'
                    '</div>',
                    unsafe_allow_html=True
                )
            with col_now:
                st.markdown(
                    '<div class="now-col">'
                    '<div class="col-period col-now">Now — ' + year_to + '</div>'
                    '<div class="col-text-now">' + now_lang + '</div>'
                    '</div>',
                    unsafe_allow_html=True
                )
            if significance:
                st.markdown(
                    '<div class="significance">' + significance + '</div>',
                    unsafe_allow_html=True
                )
        st.markdown('</div>', unsafe_allow_html=True)

    # ── Value shifts ──────────────────────────────────────────────────────
    value_shifts = result.get("value_shifts", [])
    if value_shifts:
        st.markdown(
            '<div class="result-card">'
            '<div class="result-card-label">Findings · 02</div>'
            '<div class="result-card-title">Value & Attitude Shifts</div>'
            '<div class="result-card-desc">What people fundamentally cared about, '
            'feared, or valued around this topic — and how those attitudes evolved. '
            'Value shifts drive purchasing decisions, community formation, and brand '
            'loyalty. They are harder to see than language shifts but more durable.</div>',
            unsafe_allow_html=True
        )
        for vs in value_shifts:
            st.markdown(
                '<div class="value-item">'
                '<div class="value-title">' + vs.get("shift", "") + '</div>'
                '<div class="value-evidence">' + vs.get("evidence", "") + '</div>'
                '</div>',
                unsafe_allow_html=True
            )
        st.markdown('</div>', unsafe_allow_html=True)

    # ── New vs faded ──────────────────────────────────────────────────────
    new_behaviors = result.get("new_behaviors", [])
    faded_behaviors = result.get("faded_behaviors", [])

    if new_behaviors or faded_behaviors:
        col_new, col_faded = st.columns(2)
        with col_new:
            st.markdown(
                '<div class="result-card">'
                '<div class="result-card-label">Findings · 03</div>'
                '<div class="result-card-title">Emerged in ' + year_to + '</div>'
                '<div class="result-card-desc">New behaviors, habits, and patterns '
                'that appeared in the later period. These did not exist or were not '
                'mainstream in ' + year_from + ' — they represent the new normal '
                'that brands and investors need to understand.</div>',
                unsafe_allow_html=True
            )
            for b in new_behaviors:
                st.markdown(
                    '<span class="tag-new">' + b + '</span>',
                    unsafe_allow_html=True
                )
            st.markdown('</div>', unsafe_allow_html=True)

        with col_faded:
            st.markdown(
                '<div class="result-card">'
                '<div class="result-card-label">Findings · 04</div>'
                '<div class="result-card-title">Faded since ' + year_from + '</div>'
                '<div class="result-card-desc">Behaviors, attitudes, and patterns '
                'that were common or dominant in ' + year_from + ' but have '
                'significantly declined or disappeared. Understanding what faded '
                'is just as important as understanding what emerged.</div>',
                unsafe_allow_html=True
            )
            for b in faded_behaviors:
                st.markdown(
                    '<span class="tag-faded">' + b + '</span>',
                    unsafe_allow_html=True
                )
            st.markdown('</div>', unsafe_allow_html=True)

    # ── Forward signal ────────────────────────────────────────────────────
    forward_signal = result.get("forward_signal", "")
    if forward_signal:
        st.markdown(
            '<div class="forward-box">'
            '<div class="forward-label-tag">Forward Signal</div>'
            '<div class="forward-title">Where This Is Heading</div>'
            '<div class="forward-subdesc">Based on the trajectory detected above, '
            'where is this market moving in the next 2 years? This is Claude\'s '
            'forward-looking read on the cultural momentum — not a prediction, '
            'but a signal worth tracking.</div>'
            '<div class="box-text">' + forward_signal + '</div>'
            '</div>',
            unsafe_allow_html=True
        )

    # ── Opportunity ───────────────────────────────────────────────────────
    opportunity = result.get("opportunity", "")
    if opportunity:
        st.markdown(
            '<div class="opportunity-box">'
            '<div class="opportunity-label-tag">Opportunity</div>'
            '<div class="opportunity-title">The Opportunity</div>'
            '<div class="opportunity-subdesc">The specific business, product, or '
            'positioning opportunity this cultural delta reveals — for brands, '
            'investors, founders, or strategists looking to move before the '
            'market catches up.</div>'
            '<div class="box-text">' + opportunity + '</div>'
            '</div>',
            unsafe_allow_html=True
        )

else:
    st.markdown('<hr>', unsafe_allow_html=True)

    st.markdown("""
    <div class="delta-definition">
        <div style="font-size:0.65rem; font-weight:700; color:#4A90E2;
        text-transform:uppercase; letter-spacing:0.12em; margin-bottom:0.6rem;">
        What is a Cultural Delta?</div>
        <div style="font-size:1.05rem; color:#FFFFFF; font-weight:600;
        margin-bottom:0.5rem; line-height:1.4;">
        Delta (Δ) = the measurable difference between two states over time.
        </div>
        <div style="font-size:0.92rem; color:#777777; line-height:1.85;">
        A cultural delta maps exactly how a market, behavior, or idea changed
        between two points in time — the language people used, the values they
        held, and the behaviors that emerged or faded. It tells you not just
        where a market is today, but the direction and velocity of its drift —
        and where it is heading next.
        </div>
    </div>
    """, unsafe_allow_html=True)

    c1, c2, c3 = st.columns(3)

    with c1:
        st.markdown("""
        <div class="step-card">
            <div class="step-num">Step 01</div>
            <div class="step-title">Parallel Research</div>
            <div class="step-desc">
            Two Claude agents launch simultaneously using Python's
            ThreadPoolExecutor. Each agent is given the Tavily web search API
            and Reddit API as callable tools and autonomously decides
            what to search — one focused on the earlier period,
            one on the later.
            </div>
            <div class="step-tech">
            Tavily API · Reddit API · Claude tool use · ThreadPoolExecutor
            </div>
        </div>
        """, unsafe_allow_html=True)

    with c2:
        st.markdown("""
        <div class="step-card">
            <div class="step-num">Step 02</div>
            <div class="step-title">Delta Synthesis</div>
            <div class="step-desc">
            A third Claude call receives both agents' research summaries.
            No additional API calls — pure reasoning. Claude maps the exact
            shifts in language, values, community attitudes, and behaviors
            that occurred between the two periods.
            </div>
            <div class="step-tech">
            Claude API · Structured JSON output · Chain-of-thought reasoning
            </div>
        </div>
        """, unsafe_allow_html=True)

    with c3:
        st.markdown("""
        <div class="step-card">
            <div class="step-num">Step 03</div>
            <div class="step-title">Forward Signal</div>
            <div class="step-desc">
            The synthesis agent extracts a forward-looking signal from the
            detected trajectory — where this market is heading in the next
            2 years and what specific opportunity the cultural drift reveals
            for brands, investors, or product builders.
            </div>
            <div class="step-tech">
            Claude API · JSON parsing · Opportunity framing
            </div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown('<br>', unsafe_allow_html=True)

    st.markdown("""
    <div style="font-size:0.65rem; font-weight:700; color:#444444;
    text-transform:uppercase; letter-spacing:0.12em;
    margin-bottom:0.75rem; font-family:IBM Plex Mono,monospace;">
    Example analyses</div>
    <div>
        <span class="example-tag">athletic wear 2019 → 2025</span>
        <span class="example-tag">remote work 2019 → 2024</span>
        <span class="example-tag">crypto 2017 → 2023</span>
        <span class="example-tag">fast food 2015 → 2025</span>
        <span class="example-tag">luxury fashion 2010 → 2024</span>
        <span class="example-tag">social media 2015 → 2025</span>
    </div>
    """, unsafe_allow_html=True)