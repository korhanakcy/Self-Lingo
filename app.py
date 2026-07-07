# -*- coding: utf-8 -*-
"""
LİNGO — TDK kelimeleriyle Türkçe kelime oyunu (Streamlit)
Kurallar (TRT Lingo mantığı):
  - 5 / 6 / 7 harfli kelime seçilir, ilk harf verilir.
  - 5 tahmin hakkı vardır. Her tahmin TDK sözlüğünde geçerli bir kelime olmalıdır.
  - Kırmızı kare  = harf doğru ve yeri doğru
  - Sarı yuvarlak = harf kelimede var ama yeri yanlış
  - Düz mavi      = harf kelimede yok
"""

import random
from pathlib import Path

import streamlit as st

# ----------------------------- sabitler -----------------------------
MAX_GUESS = 5
ALPHABET = "abcçdefgğhıijklmnoöprsştuüvyz"
TR_LOWER = str.maketrans("ABCÇDEFGĞHIİJKLMNOÖPRSŞTUÜVYZÂÎÛ",
                         "abcçdefgğhıijklmnoöprsştuüvyzaiu")
DATA_DIR = Path(__file__).parent

st.set_page_config(page_title="Lingo — TDK", page_icon="🟦", layout="centered")


# ----------------------------- yardımcılar -----------------------------
def tr_lower(s: str) -> str:
    return s.strip().translate(TR_LOWER)


@st.cache_data
def load_words(n: int) -> list[str]:
    path = DATA_DIR / f"kelimeler_{n}.txt"
    return path.read_text(encoding="utf-8").split()


def score_guess(guess: str, target: str) -> list[str]:
    """Her harf için 'dogru' / 'var' / 'yok' döndürür (tekrar eden harf sayımı doğru)."""
    result = ["yok"] * len(guess)
    remaining: dict[str, int] = {}
    for g, t in zip(guess, target):
        if g == t:
            pass
        else:
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
    words = load_words(n)
    st.session_state.length = n
    st.session_state.target = random.choice(words)
    st.session_state.guesses = []      # [(kelime, [durumlar])]
    st.session_state.over = False
    st.session_state.won = False
    st.session_state.msg = ""


def init_state():
    if "target" not in st.session_state:
        st.session_state.score = 0
        st.session_state.streak = 0
        st.session_state.played = 0
        st.session_state.wins = 0
        new_game(5)


init_state()

# ----------------------------- stil -----------------------------
st.markdown("""
<style>
.stApp { background: linear-gradient(180deg, #0b1d5b 0%, #12277a 100%); }
h1, h2, h3, p, label, .stMarkdown { color: #eef2ff !important; }
div[data-testid="stForm"] { background: rgba(255,255,255,0.06);
    border: 1px solid rgba(255,255,255,0.15); border-radius: 12px; }
.lingo-title { font-family: Georgia, serif; letter-spacing: .35em;
    text-align:center; font-size: 2.4rem; font-weight: 800; color:#fff;
    text-shadow: 0 2px 0 #071240; margin-bottom: 0; }
.lingo-sub { text-align:center; color:#9db1ff !important; margin-top: 2px; }
.board { display:flex; flex-direction:column; gap:8px; align-items:center; margin:18px 0; }
.row { display:flex; gap:8px; }
.tile { width:52px; height:52px; display:flex; align-items:center; justify-content:center;
    font-size:1.6rem; font-weight:800; color:#fff; text-transform:uppercase;
    background:#2743a8; border:2px solid #4b66d6; border-radius:6px;
    font-family: Georgia, serif; }
.tile.dogru { background:#d92b2b; border-color:#ff6b6b; }
.tile.var   { background:#2743a8; position:relative; }
.tile.var span { background:#f3c614; color:#3a2c00; width:40px; height:40px;
    border-radius:50%; display:flex; align-items:center; justify-content:center; }
.tile.yok   { background:#16265e; border-color:#2c3f8f; color:#8fa0e8; }
.tile.bos   { background:#1b2f7d; border-color:#3a54c0; color:#6f86e8; }
.tile.ipucu { background:#d92b2b; border-color:#ff6b6b; }
.scorebar { display:flex; justify-content:center; gap:26px; color:#cdd8ff;
    font-size:0.95rem; margin-top:6px; }
.scorebar b { color:#ffd54d; }
.klavye { text-align:center; line-height:2.1; letter-spacing:2px; }
.klavye span { display:inline-block; width:30px; padding:3px 0; margin:2px;
    border-radius:5px; font-weight:700; text-transform:uppercase;
    background:#2743a8; color:#fff; }
.klavye span.dogru { background:#d92b2b; }
.klavye span.var { background:#f3c614; color:#3a2c00; }
.klavye span.yok { background:#101c49; color:#4d5fa8; }
</style>
""", unsafe_allow_html=True)

# ----------------------------- başlık + skor -----------------------------
st.markdown('<p class="lingo-title">L İ N G O</p>', unsafe_allow_html=True)
st.markdown('<p class="lingo-sub">TDK sözlüğündeki kelimelerle • 5 tahmin hakkı</p>',
            unsafe_allow_html=True)
st.markdown(
    f'<div class="scorebar"><span>Puan: <b>{st.session_state.score}</b></span>'
    f'<span>Seri: <b>{st.session_state.streak}</b></span>'
    f'<span>Oyun: <b>{st.session_state.wins}/{st.session_state.played}</b></span></div>',
    unsafe_allow_html=True)

# ----------------------------- yeni oyun / uzunluk seçimi -----------------------------
c1, c2 = st.columns([2, 1])
with c1:
    sec = st.radio("Kelime uzunluğu", [5, 6, 7], horizontal=True,
                   index=[5, 6, 7].index(st.session_state.length))
with c2:
    st.write("")
    if st.button("🔄 Yeni kelime", use_container_width=True):
        if not st.session_state.over and st.session_state.guesses:
            st.session_state.streak = 0  # yarıda bırakmak seriyi bozar
        new_game(sec)
        st.rerun()

if sec != st.session_state.length and not st.session_state.guesses:
    new_game(sec)
    st.rerun()

target = st.session_state.target
L = st.session_state.length

# ----------------------------- tahta -----------------------------
def tile(ch: str, cls: str) -> str:
    inner = f"<span>{ch}</span>" if cls == "var" else ch
    return f'<div class="tile {cls}">{inner}</div>'

rows_html = []
for guess, states in st.session_state.guesses:
    rows_html.append('<div class="row">' +
                     "".join(tile(g, s) for g, s in zip(guess, states)) +
                     "</div>")

if not st.session_state.over and len(st.session_state.guesses) < MAX_GUESS:
    # aktif satır: ilk harf ipucu olarak kırmızı gösterilir
    active = tile(target[0], "ipucu") + "".join(tile("·", "bos") for _ in range(L - 1))
    rows_html.append(f'<div class="row">{active}</div>')

while len(rows_html) < MAX_GUESS:
    rows_html.append('<div class="row">' +
                     "".join(tile("", "bos") for _ in range(L)) + "</div>")

st.markdown('<div class="board">' + "".join(rows_html) + "</div>", unsafe_allow_html=True)

# ----------------------------- harf durumu (mini klavye) -----------------------------
letter_state: dict[str, str] = {}
rank = {"yok": 1, "var": 2, "dogru": 3}
for guess, states in st.session_state.guesses:
    for g, s in zip(guess, states):
        if rank[s] > rank.get(letter_state.get(g, ""), 0):
            letter_state[g] = s
kl = "".join(f'<span class="{letter_state.get(h, "")}">{h}</span>' for h in ALPHABET)
st.markdown(f'<div class="klavye">{kl}</div>', unsafe_allow_html=True)

# ----------------------------- tahmin girişi -----------------------------
if not st.session_state.over:
    with st.form("tahmin_form", clear_on_submit=True):
        raw = st.text_input(f"{L} harfli tahminin", max_chars=L,
                            placeholder=f"{target[0].upper()} ile başlıyor…")
        gonder = st.form_submit_button("Tahmin et", use_container_width=True)

    if gonder:
        guess = tr_lower(raw)
        words = load_words(L)
        if len(guess) != L:
            st.warning(f"Kelime {L} harfli olmalı.")
        elif not set(guess) <= set(ALPHABET):
            st.warning("Sadece Türkçe harfler kullan.")
        elif guess not in words:
            st.warning(f"“{guess}” TDK listesinde yok. Başka bir kelime dene.")
        else:
            states = score_guess(guess, target)
            st.session_state.guesses.append((guess, states))
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

# ----------------------------- oyun sonu -----------------------------
if st.session_state.over:
    if st.session_state.won:
        st.success(f"🎉 Bildin! Kelime **{target.upper()}** idi "
                   f"({len(st.session_state.guesses)}. tahminde).")
        st.balloons()
    else:
        st.error(f"Hakların bitti. Kelime **{target.upper()}** idi.")
    if st.button("▶️ Sıradaki kelime", use_container_width=True, type="primary"):
        new_game(sec)
        st.rerun()

with st.expander("Nasıl oynanır?"):
    st.markdown("""
- Bilgisayar TDK sözlüğünden gizli bir kelime seçer, **ilk harfi** sana verilir.
- **5 tahmin** hakkın var; her tahmin sözlükte geçerli, aynı uzunlukta bir kelime olmalı.
- 🟥 **Kırmızı kare** → harf doğru, yeri doğru.
- 🟡 **Sarı yuvarlak** → harf kelimede var ama başka yerde.
- 🟦 **Koyu mavi** → harf kelimede yok.
- Puan: bilirsen 50 + kalan her hak için 25. Üst üste bilerek seri yap!
""")
