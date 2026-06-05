import streamlit as st
import streamlit.components.v1 as components
import random
import json
import math

# ──────────────────────────────────────────────────
# PAGE CONFIG
# ──────────────────────────────────────────────────

st.set_page_config(
    page_title="Truth & Dare Wheel",
    page_icon="🎡",
    layout="centered",
)

# ──────────────────────────────────────────────────
# SESSION STATE
# ──────────────────────────────────────────────────

DEFAULTS = {
    "selected":      None,
    "show_wheel":    False,
    "challenge":     None,
    "history":       [],
    "player_stats":  {},
    "spin_count":    0,
    "custom_truths": [],
    "custom_dares":  [],
}
for k, v in DEFAULTS.items():
    if k not in st.session_state:
        st.session_state[k] = v

# ──────────────────────────────────────────────────
# CUSTOM CSS
# ──────────────────────────────────────────────────

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Poppins:wght@400;600;700;800&display=swap');

.stApp {
    background: linear-gradient(135deg, #0f0c29 0%, #302b63 50%, #24243e 100%) !important;
}

/* ── Typography ── */
html, body, [class*="css"] {
    font-family: 'Poppins', sans-serif !important;
}

.main-title {
    text-align: center;
    font-size: 48px;
    font-weight: 800;
    background: linear-gradient(90deg, #38bdf8, #818cf8, #f472b6);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
    padding: 8px 0;
}
.subtitle {
    text-align: center;
    color: #94a3b8;
    font-size: 13px;
    letter-spacing: 4px;
    text-transform: uppercase;
    margin-top: -6px;
    margin-bottom: 24px;
}

/* ── Section headers ── */
.sec-hdr {
    font-size: 11px;
    font-weight: 700;
    color: #475569;
    text-transform: uppercase;
    letter-spacing: 2.5px;
    margin: 22px 0 8px;
    padding-bottom: 6px;
    border-bottom: 1px solid #1e293b;
}

/* ── Player chips ── */
.player-grid {
    display: flex;
    flex-wrap: wrap;
    gap: 8px;
    margin-bottom: 16px;
}
.p-chip {
    background: #1e293b;
    border: 1px solid #334155;
    padding: 8px 16px;
    border-radius: 50px;
    color: #e2e8f0;
    font-size: 13px;
    font-weight: 600;
    display: flex;
    align-items: center;
    gap: 8px;
}
.p-chip-count {
    font-size: 11px;
    color: #475569;
    font-weight: 400;
    background: #0f172a;
    padding: 1px 7px;
    border-radius: 20px;
}

/* ── Winner box ── */
.winner-box {
    background: linear-gradient(135deg, #14532d, #166534);
    border: 2px solid #22c55e;
    padding: 26px 20px;
    border-radius: 22px;
    text-align: center;
    margin: 16px 0;
    box-shadow: 0 0 40px rgba(34,197,94,0.18);
}

/* ── Challenge box ── */
.ch-box {
    padding: 26px;
    border-radius: 22px;
    margin-top: 16px;
}
.ch-truth {
    background: linear-gradient(135deg, #1e1b4b, #312e81);
    border: 2px solid #818cf8;
    box-shadow: 0 0 40px rgba(129,140,248,0.15);
}
.ch-dare {
    background: linear-gradient(135deg, #450a0a, #7f1d1d);
    border: 2px solid #ef4444;
    box-shadow: 0 0 40px rgba(239,68,68,0.15);
}
.ch-label {
    font-size: 11px;
    font-weight: 700;
    letter-spacing: 3px;
    text-transform: uppercase;
    margin-bottom: 12px;
}
.ch-text {
    font-size: 21px;
    font-weight: 600;
    color: #f1f5f9;
    line-height: 1.5;
}
.ch-by {
    font-size: 12px;
    color: #64748b;
    margin-top: 14px;
}

/* ── Stat cards ── */
.stat-card {
    background: #1e293b;
    border: 1px solid #1e293b;
    padding: 18px 8px;
    border-radius: 18px;
    text-align: center;
}
.stat-num {
    font-size: 32px;
    font-weight: 800;
    line-height: 1;
}
.stat-lbl {
    font-size: 11px;
    color: #64748b;
    text-transform: uppercase;
    letter-spacing: 1px;
    margin-top: 6px;
}

/* ── History items ── */
.hist-item {
    background: #0f172a;
    border-left: 4px solid #334155;
    padding: 11px 15px;
    border-radius: 0 12px 12px 0;
    margin: 7px 0;
}
.hist-item.t { border-left-color: #818cf8; }
.hist-item.d { border-left-color: #ef4444; }
.hist-player { font-size: 13px; font-weight: 700; color: #f1f5f9; }
.hist-q      { font-size: 12px; color: #94a3b8; margin-top: 4px; }

/* ── Empty states ── */
.empty {
    text-align: center;
    padding: 44px 20px;
    color: #475569;
    font-size: 14px;
}

/* ── Streamlit overrides ── */
div[data-testid="stButton"] button {
    border-radius: 12px !important;
    font-weight: 700 !important;
    font-family: 'Poppins', sans-serif !important;
    transition: all 0.15s ease !important;
}
div[data-testid="stButton"] button:hover {
    transform: translateY(-2px) !important;
    box-shadow: 0 8px 20px rgba(0,0,0,0.35) !important;
}
.stTextArea textarea,
.stTextInput input {
    background: #1e293b !important;
    border: 1px solid #334155 !important;
    color: #e2e8f0 !important;
    border-radius: 12px !important;
    font-family: 'Poppins', sans-serif !important;
}
.stTabs [data-baseweb="tab-list"] {
    background: #1e293b !important;
    border-radius: 14px !important;
    padding: 4px !important;
    gap: 4px !important;
}
.stTabs [data-baseweb="tab"] {
    border-radius: 10px !important;
    color: #94a3b8 !important;
    font-weight: 600 !important;
    font-family: 'Poppins', sans-serif !important;
}
.stTabs [aria-selected="true"] {
    background: #0f172a !important;
    color: #38bdf8 !important;
}
</style>
""", unsafe_allow_html=True)

# ──────────────────────────────────────────────────
# QUESTION BANK  (10 truths + 10 dares per difficulty)
# ──────────────────────────────────────────────────

QUESTIONS = {
    "🟢 Mild": {
        "truths": [
            "What is your most embarrassing childhood memory?",
            "What is your weirdest habit?",
            "Who was your first crush?",
            "What is the last lie you told?",
            "What song do you secretly love?",
            "What is your biggest pet peeve?",
            "What is the most childish thing you still do?",
            "What would you do with a million dollars?",
            "Who do you text the most?",
            "Have you ever talked to yourself in public?",
            "What is your deep fantasy?",
            "What is your favourite p category?",
            "What is your favourite position?",
        ],
        "dares": [
            "Do 10 pushups.",
            "Dance for 30 seconds.",
            "Talk in a funny accent for 1 minute.",
            "Act like a cat for 30 seconds.",
            "Tell the funniest joke you know.",
            "Hop on one foot for 30 seconds.",
            "Do your best robot dance.",
            "Sing the chorus of your favourite song.",
            "Do a catwalk across the room.",
            "Imitate a celebrity for 30 seconds.",
        ],
    },
    "🟡 Medium": {
        "truths": [
            "What is your biggest fear?",
            "What is your biggest regret?",
            "Have you ever lied to your best friend?",
            "What is the most embarrassing thing you've Googled?",
            "Have you ever cheated on a test?",
            "What is your biggest insecurity?",
            "Who here would you trust most in a crisis?",
            "What would you change about yourself?",
            "What is the most illegal thing you've done?",
            "What secret have you kept for years?",
        ],
        "dares": [
            "Let someone draw a mustache on you with a marker.",
            "Eat a spoonful of hot sauce.",
            "Text a random contact 'I miss you'.",
            "Call someone and sing Happy Birthday.",
            "Let someone read your last 10 texts aloud.",
            "Do an impression until someone guesses who it is.",
            "Speak only in questions for the next 3 rounds.",
            "Wear socks on your hands for 2 rounds.",
            "Narrate everything you do for the next 2 minutes.",
            "Post an embarrassing photo to your story for 5 min.",
        ],
    },
    "🔴 Wild": {
        "truths": [
            "What is the most embarrassing thing you've done for love?",
            "Have you ever snooped on someone's phone?",
            "What is the biggest secret you know about someone in this room?",
            "What is something you pretend to like but secretly hate?",
            "What is your most controversial opinion?",
            "What is the pettiest thing you've ever done?",
            "Have you ever ghosted someone? Why?",
            "What is the most ridiculous thing you've cried at?",
            "What's your worst autocorrect disaster?",
            "What's the most embarrassing DM or text you've sent?",
        ],
        "dares": [
            "Let someone post anything they want on your social media.",
            "Do your best impression of each person in the room.",
            "Call a family member and say something you've always wanted to.",
            "Swap an item of clothing with someone for 3 rounds.",
            "Let the group style your hair however they like.",
            "Do a 60-second stand-up comedy set right now.",
            "Describe your last dream in full embarrassing detail.",
            "Give every person in the room a genuine heartfelt compliment.",
            "Recreate your best or worst ever pickup line.",
            "Speak only in rhymes for the next 2 rounds.",
            "Seduce the one of opposite gender.",
            "A kiss on the cheeks",
        ],
    },
}

# ──────────────────────────────────────────────────
# WHEEL HTML  (canvas + exact landing on winner)
# ──────────────────────────────────────────────────

WHEEL_COLORS = [
    "#ef4444", "#3b82f6", "#22c55e", "#f59e0b",
    "#a855f7", "#ec4899", "#06b6d4", "#84cc16",
    "#f97316", "#14b8a6", "#8b5cf6", "#e11d48",
]

def make_wheel_html(players: list, selected_player: str) -> str:
    """
    Generates an animated canvas wheel that correctly stops with the
    pointer (▼ at top) aimed at the centre of the selected player's segment.

    Math: drawWheel(rot) paints segment i starting at (rot + i*arc).
    We call it as drawWheel(eased * totalRot  −  π/2).
    At t=1:  segment centre for sel_idx  =  (totalRot − π/2) + sel_idx*arc + arc/2
    We want that to equal −π/2  (top of canvas, where pointer aims).
    → totalRot  +  sel_idx*arc  +  arc/2  =  0
    → final_rot = −(sel_idx + 0.5) * arc
    → totalRot  = 7 * 2π  +  final_rot   (7 full spins before landing)
    """
    n        = len(players)
    arc      = 2 * math.pi / n
    sel_idx  = players.index(selected_player)
    final_rot = -(sel_idx + 0.5) * arc
    total_rot = 7 * 2 * math.pi + final_rot

    players_js = json.dumps(players)
    colors_js  = json.dumps([WHEEL_COLORS[i % len(WHEEL_COLORS)] for i in range(n)])

    return f"""<!DOCTYPE html>
<html>
<head>
<meta charset="utf-8">
<style>
  * {{ margin:0; padding:0; box-sizing:border-box; }}
  body {{
    background: transparent;
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    height: 380px;
    overflow: hidden;
  }}
  .ptr {{
    font-size: 42px;
    line-height: 1;
    margin-bottom: -14px;
    z-index: 10;
    filter: drop-shadow(0 2px 14px rgba(239,68,68,0.95));
    animation: bob 0.6s ease-in-out infinite alternate;
  }}
  @keyframes bob {{
    from {{ transform: translateY(0);   }}
    to   {{ transform: translateY(-5px); }}
  }}
  canvas {{
    border-radius: 50%;
    box-shadow: 0 0 55px rgba(56,189,248,0.3),
                0 0 0 5px rgba(255,255,255,0.06);
  }}
</style>
</head>
<body>
  <div class="ptr">▼</div>
  <canvas id="w" width="300" height="300"></canvas>
<script>
  const players  = {players_js};
  const colors   = {colors_js};
  const totalRot = {total_rot:.8f};
  const n = players.length;
  const cx = 150, cy = 150, r = 140;
  const cvs = document.getElementById("w");
  const ctx = cvs.getContext("2d");

  function draw(rot) {{
    ctx.clearRect(0, 0, 300, 300);
    const arc = 2 * Math.PI / n;

    for (let i = 0; i < n; i++) {{
      const s = rot + i * arc;
      const e = s + arc;

      // Fill segment
      ctx.beginPath();
      ctx.moveTo(cx, cy);
      ctx.arc(cx, cy, r, s, e);
      ctx.closePath();
      ctx.fillStyle = colors[i];
      ctx.fill();

      // Subtle shimmer overlay
      const mid = s + arc / 2;
      const grd = ctx.createLinearGradient(
        cx, cy,
        cx + r * Math.cos(mid),
        cy + r * Math.sin(mid)
      );
      grd.addColorStop(0, "rgba(255,255,255,0.14)");
      grd.addColorStop(1, "rgba(0,0,0,0.08)");
      ctx.beginPath();
      ctx.moveTo(cx, cy);
      ctx.arc(cx, cy, r, s, e);
      ctx.closePath();
      ctx.fillStyle = grd;
      ctx.fill();

      // Divider lines
      ctx.strokeStyle = "rgba(255,255,255,0.2)";
      ctx.lineWidth = 2;
      ctx.stroke();

      // Player name label
      ctx.save();
      ctx.translate(cx, cy);
      ctx.rotate(mid);
      ctx.textAlign = "right";
      ctx.fillStyle  = "rgba(255,255,255,0.95)";
      const fs = Math.max(9, Math.min(15, 130 / Math.max(n, 4)));
      ctx.font = `bold ${{fs}}px sans-serif`;
      ctx.shadowColor = "rgba(0,0,0,0.85)";
      ctx.shadowBlur  = 5;
      const raw = players[i];
      const lbl = raw.length > 11 ? raw.slice(0, 10) + "…" : raw;
      ctx.fillText(lbl, r - 12, fs * 0.38);
      ctx.restore();
    }}

    // Outer ring
    ctx.beginPath();
    ctx.arc(cx, cy, r, 0, 2 * Math.PI);
    ctx.strokeStyle = "rgba(255,255,255,0.55)";
    ctx.lineWidth   = 4;
    ctx.stroke();

    // Centre cap (gradient)
    const cg = ctx.createRadialGradient(cx - 5, cy - 5, 1, cx, cy, 22);
    cg.addColorStop(0, "#334155");
    cg.addColorStop(1, "#0f172a");
    ctx.beginPath();
    ctx.arc(cx, cy, 22, 0, 2 * Math.PI);
    ctx.fillStyle   = cg;
    ctx.fill();
    ctx.strokeStyle = "rgba(255,255,255,0.35)";
    ctx.lineWidth   = 2;
    ctx.stroke();

    // Centre emoji
    ctx.font          = "18px serif";
    ctx.textAlign     = "center";
    ctx.textBaseline  = "middle";
    ctx.shadowBlur    = 0;
    ctx.fillStyle     = "white";
    ctx.fillText("✨", cx, cy);
  }}

  function easeOutQuart(t) {{ return 1 - Math.pow(1 - t, 4); }}

  const dur = 4800;
  let   t0  = null;

  function frame(ts) {{
    if (!t0) t0 = ts;
    const p = Math.min((ts - t0) / dur, 1);
    draw(easeOutQuart(p) * totalRot - Math.PI / 2);
    if (p < 1) requestAnimationFrame(frame);
  }}

  draw(-Math.PI / 2);          // static preview
  requestAnimationFrame(frame); // start animation
</script>
</body>
</html>"""

# ──────────────────────────────────────────────────
# HEADER
# ──────────────────────────────────────────────────

st.markdown('<div class="main-title">🎡 Truth & Dare Wheel</div>', unsafe_allow_html=True)
st.markdown('<div class="subtitle">Spin · Choose · Survive</div>',  unsafe_allow_html=True)

tab_game, tab_history, tab_custom = st.tabs([
    "🎮  Game", "📜  History", "✏️  Custom Q&A"
])

# ──────────────────────────────────────────────────
# TAB 1 — GAME
# ──────────────────────────────────────────────────

with tab_game:

    # ── Player input ──
    st.markdown('<div class="sec-hdr">Players</div>', unsafe_allow_html=True)
    raw = st.text_area(
        "Players",
        height=130,
        placeholder="Alice\nBob\nCharlie\nDiana",
        label_visibility="collapsed",
    )
    players = [p.strip() for p in raw.split("\n") if p.strip()]

    # ── Difficulty ──
    st.markdown('<div class="sec-hdr">Difficulty</div>', unsafe_allow_html=True)
    difficulty = st.select_slider(
        "Difficulty",
        options=list(QUESTIONS.keys()),
        value="🟢 Mild",
        label_visibility="collapsed",
    )

    # ── Player chips ──
    if players:
        chips = '<div class="player-grid">'
        for p in players:
            cnt = st.session_state.player_stats.get(p, 0)
            chips += (
                f'<div class="p-chip">👤 {p}'
                f'<span class="p-chip-count">×{cnt}</span></div>'
            )
        chips += "</div>"
        st.markdown(chips, unsafe_allow_html=True)

    # ── Spin / Reset buttons ──
    if len(players) >= 2:
        col_spin, col_reset = st.columns([5, 1])

        with col_spin:
            if st.button("🎯  SPIN THE WHEEL", use_container_width=True, type="primary"):
                winner = random.choice(players)
                st.session_state.selected    = winner
                st.session_state.show_wheel  = True
                st.session_state.challenge   = None
                st.session_state.spin_count += 1
                st.session_state.player_stats[winner] = (
                    st.session_state.player_stats.get(winner, 0) + 1
                )

        with col_reset:
            if st.button("🔄", use_container_width=True, help="Reset everything"):
                for k, v in DEFAULTS.items():
                    st.session_state[k] = v if not isinstance(v, (list, dict)) else type(v)()
                st.rerun()

    elif len(players) == 1:
        st.warning("Add at least **2 players** to start spinning.")
    else:
        st.markdown(
            '<div class="empty">👆 Enter player names above to begin!</div>',
            unsafe_allow_html=True,
        )

    # ── Spinning wheel (only visible right after spin) ──
    if st.session_state.show_wheel and st.session_state.selected in (players or []):
        components.html(
            make_wheel_html(players, st.session_state.selected),
            height=395,
            scrolling=False,
        )

    # ── Winner banner ──
    if st.session_state.selected and st.session_state.selected in (players or []):
        st.markdown(
            f"""
            <div class="winner-box">
                <div style="font-size:11px;color:#86efac;letter-spacing:3px;
                            text-transform:uppercase;margin-bottom:6px">🎉 Selected</div>
                <div style="font-size:46px;font-weight:800;color:#fff;
                            margin:4px 0">{st.session_state.selected}</div>
                <div style="font-size:12px;color:#86efac;margin-top:4px">
                    Pick your challenge ↓</div>
            </div>
            """,
            unsafe_allow_html=True,
        )

        # Build combined question pool
        t_pool = QUESTIONS[difficulty]["truths"] + st.session_state.custom_truths
        d_pool = QUESTIONS[difficulty]["dares"]  + st.session_state.custom_dares

        c1, c2 = st.columns(2)
        with c1:
            if st.button("🟢  TRUTH", use_container_width=True):
                q = random.choice(t_pool)
                st.session_state.challenge  = ("TRUTH", q)
                st.session_state.show_wheel = False
                st.session_state.history.append(
                    {"player": st.session_state.selected, "type": "TRUTH", "question": q}
                )
        with c2:
            if st.button("🔴  DARE", use_container_width=True):
                q = random.choice(d_pool)
                st.session_state.challenge  = ("DARE", q)
                st.session_state.show_wheel = False
                st.session_state.history.append(
                    {"player": st.session_state.selected, "type": "DARE", "question": q}
                )

    # ── Challenge display ──
    if st.session_state.challenge:
        mode, text = st.session_state.challenge
        if mode == "TRUTH":
            cls, color, icon = "ch-truth", "#818cf8", "🤔"
        else:
            cls, color, icon = "ch-dare", "#ef4444", "🔥"

        st.markdown(
            f"""
            <div class="ch-box {cls}">
                <div class="ch-label" style="color:{color}">{icon} {mode}</div>
                <div class="ch-text">{text}</div>
                <div class="ch-by">— {st.session_state.selected}</div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    # ── Session stats ──
    if st.session_state.spin_count > 0:
        st.markdown('<div class="sec-hdr">Session Stats</div>', unsafe_allow_html=True)
        n_t = sum(1 for h in st.session_state.history if h["type"] == "TRUTH")
        n_d = len(st.session_state.history) - n_t

        s1, s2, s3 = st.columns(3)
        with s1:
            st.markdown(
                f'<div class="stat-card">'
                f'<div class="stat-num" style="color:#38bdf8">{st.session_state.spin_count}</div>'
                f'<div class="stat-lbl">Spins</div></div>',
                unsafe_allow_html=True,
            )
        with s2:
            st.markdown(
                f'<div class="stat-card">'
                f'<div class="stat-num" style="color:#22c55e">{n_t}</div>'
                f'<div class="stat-lbl">Truths</div></div>',
                unsafe_allow_html=True,
            )
        with s3:
            st.markdown(
                f'<div class="stat-card">'
                f'<div class="stat-num" style="color:#ef4444">{n_d}</div>'
                f'<div class="stat-lbl">Dares</div></div>',
                unsafe_allow_html=True,
            )

# ──────────────────────────────────────────────────
# TAB 2 — HISTORY
# ──────────────────────────────────────────────────

with tab_history:
    st.markdown('<div class="sec-hdr">Challenge Log</div>', unsafe_allow_html=True)

    if not st.session_state.history:
        st.markdown(
            '<div class="empty">📭 No challenges yet — start spinning!</div>',
            unsafe_allow_html=True,
        )
    else:
        for item in reversed(st.session_state.history):
            td  = item["type"]
            css = "t" if td == "TRUTH" else "d"
            ico = "🤔" if td == "TRUTH" else "🔥"
            clr = "#818cf8" if td == "TRUTH" else "#ef4444"
            st.markdown(
                f"""
                <div class="hist-item {css}">
                    <div class="hist-player">
                        {item['player']}
                        <span style="font-size:11px;color:{clr};
                                     margin-left:6px">{ico} {td}</span>
                    </div>
                    <div class="hist-q">{item['question']}</div>
                </div>
                """,
                unsafe_allow_html=True,
            )

        st.write("")
        if st.button("🗑️  Clear History"):
            st.session_state.history = []
            st.rerun()

# ──────────────────────────────────────────────────
# TAB 3 — CUSTOM Q&A
# ──────────────────────────────────────────────────

with tab_custom:
    col_t, col_d = st.columns(2)

    # ── Custom Truths ──
    with col_t:
        st.markdown('<div class="sec-hdr">Custom Truths</div>', unsafe_allow_html=True)
        nt = st.text_input(
            "truth",
            placeholder="Your deepest secret?",
            key="t_in",
            label_visibility="collapsed",
        )
        if st.button("➕ Add Truth", use_container_width=True) and nt.strip():
            st.session_state.custom_truths.append(nt.strip())
            st.rerun()

        for i, t in enumerate(st.session_state.custom_truths):
            ca, cb = st.columns([5, 1])
            with ca:
                st.markdown(f"<small style='color:#94a3b8'>• {t}</small>", unsafe_allow_html=True)
            with cb:
                if st.button("✕", key=f"dt{i}"):
                    st.session_state.custom_truths.pop(i)
                    st.rerun()

    # ── Custom Dares ──
    with col_d:
        st.markdown('<div class="sec-hdr">Custom Dares</div>', unsafe_allow_html=True)
        nd = st.text_input(
            "dare",
            placeholder="Stand on one foot!",
            key="d_in",
            label_visibility="collapsed",
        )
        if st.button("➕ Add Dare", use_container_width=True) and nd.strip():
            st.session_state.custom_dares.append(nd.strip())
            st.rerun()

        for i, d in enumerate(st.session_state.custom_dares):
            ca, cb = st.columns([5, 1])
            with ca:
                st.markdown(f"<small style='color:#94a3b8'>• {d}</small>", unsafe_allow_html=True)
            with cb:
                if st.button("✕", key=f"dd{i}"):
                    st.session_state.custom_dares.pop(i)
                    st.rerun()
