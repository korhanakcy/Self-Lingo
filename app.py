# -*- coding: utf-8 -*-
"""
LİNGO — TDK kelimeleriyle Türkçe kelime oyunu (Streamlit, mobil öncelikli)
  - Yeşil  = harf doğru ve yeri doğru
  - Sarı   = harf kelimede var ama yeri yanlış
  - Lacivert = varsayılan (olmayan harfte ekstra vurgu yok)
"""

import random
from pathlib import Path

import streamlit as st

MAX_GUESS = 5
ALPHABET = "abcçdefgğhıijklmnoöprsştuüvyz"
TR_LOWER = str.maketrans("ABCÇDEFGĞHIİJKLMNOÖPRSŞTUÜVYZÂÎÛ",
                         "abcçdefgğhıijklmnoöprsştuüvyzaiu")
TR_UPPER = str.maketrans("abcçdefgğhıijklmnoöprsştuüvyz",
                         "ABCÇDEFGĞHIİJKLMNOÖPRSŞTUÜVYZ")
DATA_DIR = Path(__file__).parent

st.set_page_config(page_title="Lingo — TDK", page_icon="🟩", layout="centered")


def tr_lower(s: str) -> str:
    return s.strip().translate(TR_LOWER)


def tr_upper(s: str) -> str:
    return s.translate(TR_UPPER)


@st.cache_data
def load_words(n: int) -> list[str]:
    return (DATA_DIR / f"kelimeler_{n}.txt").read_text(encoding="utf-8").split()


def score_guess(guess: str, target: str) -> list[str]:
    result = ["yok"] * len(guess)
    remaining: dict[str, int] = {}
    for g, t in zip(guess, target):
        if g != t:
            remaining[t] = remaining.get(t, 0) + 1
    for i, (g, t) in enumerate(zip(guess, target)):
        if g == t:
            result[i] = "dogru"
    for i, g in enumerate(guess):
        if result[i] == "dogru":
            continue
        if remaining.get(g, 0) > 0:
            result[i] = "var"
            remaining[g] -= 1
    return result


def new_game(n: int):
    st.session_state.length = n
    st.session_state.target = random.choice(load_words(n))
    st.session_state.guesses = []
    st.session_state.over = False
    st.session_state.won = False


def init_state():
    if "target" not in st.session_state:
        st.session_state.score = 0
        st.session_state.streak = 0
        st.session_state.played = 0
        st.session_state.wins = 0
        new_game(5)


init_state()

# ------------------------------ stil ------------------------------
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Nunito:wght@700;800;900&display=swap');

.stApp { background: #fff2f2; }
.block-container { padding-top: 1.2rem; max-width: 520px; }
html, body, [class*="css"] { font-family: 'Nunito', system-ui, sans-serif; }
h1,h2,h3,p,label,.stMarkdown { color: #1d2b6b !important; }

/* başlık bandı */
.banner { background: #e63946; color: #fff; text-align: center;
  font-weight: 900; font-size: 1.25rem; letter-spacing: .06em;
  padding: 10px 14px; border-radius: 14px;
  box-shadow: 0 4px 0 #b32230; margin-bottom: 4px; }
.logo { text-align:center; font-weight: 900; font-size: 2rem;
  letter-spacing: .3em; color:#1d2b6b; margin: 6px 0 0 0; }
.logo span:nth-child(1){color:#e63946}.logo span:nth-child(2){color:#f4a61d}
.logo span:nth-child(3){color:#26a653}.logo span:nth-child(4){color:#1d78d1}
.logo span:nth-child(5){color:#e63946}

.scorebar { display:flex; justify-content:center; gap:22px;
  color:#5a679f; font-size:.92rem; margin:4px 0 2px 0; }
.scorebar b { color:#1d2b6b; }

/* tahta — mobil öncelikli, 7 harf de sığar */
.board { display:flex; flex-direction:column; gap:7px; align-items:center; margin:14px 0 10px 0; }
.row { display:flex; gap:7px; }
.tile { width: clamp(40px, 11.5vw, 58px); aspect-ratio: 1;
  display:flex; align-items:center; justify-content:center;
  font-size: clamp(1.35rem, 5.8vw, 1.85rem); font-weight: 900;
  color:#ffffff !important; -webkit-text-fill-color:#ffffff;
  text-shadow: 0 1px 2px rgba(0,0,0,.35);
  background:#243472; border-radius:12px;
  box-shadow: 0 3px 0 rgba(20,30,80,.45); }
.tile.dogru { background:#26a653; box-shadow: 0 3px 0 #1a7a3c; }
.tile.var   { background:#f4a61d; box-shadow: 0 3px 0 #c07f0a; }
.tile.yok   { background:#243472; }                    /* vurgu yok */
.tile.bos   { background:#e9e2ea; color:#b9aec4 !important;
  -webkit-text-fill-color:#b9aec4; text-shadow:none; box-shadow: 0 3px 0 #d8cede; }
.tile.ipucu { background:#26a653; box-shadow: 0 3px 0 #1a7a3c; }

/* mini klavye */
.klavye { text-align:center; line-height:2.2; }
.klavye span { display:inline-block; min-width:29px; padding:4px 2px; margin:2px;
  border-radius:7px; font-weight:800; font-size:.95rem;
  background:#fff; color:#1d2b6b; border:1.5px solid #e3d3d6; }
.klavye span.dogru { background:#26a653; color:#fff; border-color:#26a653; }
.klavye span.var   { background:#f4a61d; color:#fff; border-color:#f4a61d; }
.klavye span.yok   { background:#f3e9ea; color:#c5b6bc; border-color:#eddfe2; }

/* form ve butonlar */
div[data-testid="stForm"] { background:#fff; border:1.5px solid #f0d9dc;
  border-radius:16px; box-shadow: 0 3px 10px rgba(230,57,70,.07); }
.stTextInput input { font-size:1.15rem !important; font-weight:800;
  letter-spacing:.15em; text-align:center; color:#1d2b6b !important;
  background:#fff2f2 !important; border-radius:10px !important; }
.stButton button, .stFormSubmitButton button {
  background:#1d2b6b; color:#ffffff !important; font-weight:800; border:none;
  border-radius:12px; box-shadow: 0 3px 0 #121d4d; }
.stButton button p, .stFormSubmitButton button p { color:#ffffff !important; }
.stButton button:hover, .stFormSubmitButton button:hover { background:#26357f; color:#fff; }
button[kind="primary"] { background:#26a653 !important; box-shadow: 0 3px 0 #1a7a3c !important; }
</style>
""", unsafe_allow_html=True)

# ------------------------------ başlık ------------------------------
st.markdown('<p class="logo"><span>L</span><span>İ</span><span>N</span><span>G</span><span>O</span></p>',
            unsafe_allow_html=True)
st.markdown('<div class="banner">DOĞRU KELİMEYİ BUL!</div>', unsafe_allow_html=True)
st.markdown(
    f'<div class="scorebar"><span>Puan <b>{st.session_state.score}</b></span>'
    f'<span>Seri <b>{st.session_state.streak}</b></span>'
    f'<span>Oyun <b>{st.session_state.wins}/{st.session_state.played}</b></span></div>',
    unsafe_allow_html=True)

# ------------------------------ uzunluk / yeni oyun ------------------------------
c1, c2 = st.columns([2, 1])
with c1:
    sec = st.radio("Kelime uzunluğu", [5, 6, 7], horizontal=True,
                   index=[5, 6, 7].index(st.session_state.length),
                   label_visibility="collapsed")
with c2:
    if st.button("🔄 Yeni kelime", use_container_width=True):
        if not st.session_state.over and st.session_state.guesses:
            st.session_state.streak = 0
        new_game(sec)
        st.rerun()

if sec != st.session_state.length and not st.session_state.guesses:
    new_game(sec)
    st.rerun()

target = st.session_state.target
L = st.session_state.length

# ------------------------------ tahta ------------------------------
def tile(ch: str, cls: str) -> str:
    return f'<div class="tile {cls}">{tr_upper(ch)}</div>'

rows = []
for guess, states in st.session_state.guesses:
    rows.append('<div class="row">' + "".join(tile(g, s) for g, s in zip(guess, states)) + "</div>")

if not st.session_state.over and len(st.session_state.guesses) < MAX_GUESS:
    # Lingo kuralı: yeri kesin bilinen harfler sonraki satırda hazır gelir
    known = [None] * L
    known[0] = target[0]
    for guess, states in st.session_state.guesses:
        for i, s in enumerate(states):
            if s == "dogru":
                known[i] = guess[i]
    active = "".join(tile(k, "ipucu") if k else tile("·", "bos") for k in known)
    rows.append(f'<div class="row">{active}</div>')

while len(rows) < MAX_GUESS:
    rows.append('<div class="row">' + "".join(tile("", "bos") for _ in range(L)) + "</div>")

st.markdown('<div class="board">' + "".join(rows) + "</div>", unsafe_allow_html=True)

# ------------------------------ mini klavye ------------------------------
letter_state: dict[str, str] = {}
rank = {"yok": 1, "var": 2, "dogru": 3}
for guess, states in st.session_state.guesses:
    for g, s in zip(guess, states):
        if rank[s] > rank.get(letter_state.get(g, ""), 0):
            letter_state[g] = s
kl = "".join(f'<span class="{letter_state.get(h, "")}">{tr_upper(h)}</span>' for h in ALPHABET)
st.markdown(f'<div class="klavye">{kl}</div>', unsafe_allow_html=True)

# ------------------------------ tahmin ------------------------------
if not st.session_state.over:
    with st.form("tahmin_form", clear_on_submit=True):
        raw = st.text_input(f"{L} harfli tahminin", max_chars=L,
                            placeholder=f"{tr_upper(target[0])} ile başlıyor…",
                            label_visibility="collapsed")
        gonder = st.form_submit_button("TAHMİN ET", use_container_width=True)

    if gonder:
        guess = tr_lower(raw)
        if len(guess) != L:
            st.warning(f"Kelime {L} harfli olmalı.")
        elif not set(guess) <= set(ALPHABET):
            st.warning("Sadece Türkçe harfler kullan.")
        elif guess not in load_words(L):
            st.warning(f"“{tr_upper(guess)}” TDK listesinde yok. Başka bir kelime dene.")
        else:
            st.session_state.guesses.append((guess, score_guess(guess, target)))
            if guess == target:
                st.session_state.over = True
                st.session_state.won = True
                kalan = MAX_GUESS - len(st.session_state.guesses)
                st.session_state.score += 50 + kalan * 25
                st.session_state.streak += 1
                st.session_state.played += 1
                st.session_state.wins += 1
            elif len(st.session_state.guesses) >= MAX_GUESS:
                st.session_state.over = True
                st.session_state.streak = 0
                st.session_state.played += 1
            st.rerun()

# ------------------------------ oyun sonu ------------------------------
if st.session_state.over:
    if st.session_state.won:
        st.success(f"🎉 Bildin! Kelime **{tr_upper(target)}** idi "
                   f"({len(st.session_state.guesses)}. tahminde).")
        st.balloons()
    else:
        st.error(f"Hakların bitti. Kelime **{tr_upper(target)}** idi.")
    if st.button("▶️ Sıradaki kelime", use_container_width=True, type="primary"):
        new_game(sec)
        st.rerun()

with st.expander("Nasıl oynanır?"):
    st.markdown("""
- Gizli kelimenin **ilk harfi** yeşil kutuda verilir.
- **5 tahmin** hakkın var; her tahmin TDK'da geçerli, aynı uzunlukta bir kelime olmalı.
- 🟩 **Yeşil** → harf doğru, yeri doğru.
- 🟨 **Sarı** → harf kelimede var ama başka yerde.
- Olmayan harflerde ekstra bir işaret yok, kutu lacivert kalır.
- Puan: bilirsen 50 + kalan her hak için 25.
""")
