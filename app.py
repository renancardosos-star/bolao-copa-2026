
import sqlite3
import hashlib
import hmac
from datetime import datetime
from pathlib import Path

import pandas as pd
import streamlit as st


DB_PATH = "bolao_copa.db"

TEAMS = {
    "Brasil": "🇧🇷",
    "Argentina": "🇦🇷",
    "França": "🇫🇷",
    "Alemanha": "🇩🇪",
    "Espanha": "🇪🇸",
    "Portugal": "🇵🇹",
    "Inglaterra": "🏴",
    "Itália": "🇮🇹",
    "México": "🇲🇽",
    "EUA": "🇺🇸",
    "Holanda": "🇳🇱",
    "Croácia": "🇭🇷",
    "Uruguai": "🇺🇾",
    "Japão": "🇯🇵",
    "Marrocos": "🇲🇦",
    "Canadá": "🇨🇦",
}


st.set_page_config(
    page_title="Bolão da Copa 2026",
    page_icon="⚽",
    layout="wide",
    initial_sidebar_state="expanded",
)


CUSTOM_CSS = """
<style>
[data-testid="stAppViewContainer"] {
    background:
        radial-gradient(circle at top left, rgba(34,197,94,0.22), transparent 28%),
        radial-gradient(circle at top right, rgba(250,204,21,0.18), transparent 30%),
        linear-gradient(135deg, #020617 0%, #061526 45%, #052e16 100%);
    color: white;
}

[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #020617, #052e16);
    border-right: 1px solid rgba(255,255,255,0.08);
}

h1, h2, h3 {
    color: white !important;
}

.hero {
    padding: 34px;
    border-radius: 30px;
    border: 1px solid rgba(255,255,255,0.12);
    background:
        linear-gradient(135deg, rgba(22,163,74,0.45), rgba(15,23,42,0.92), rgba(250,204,21,0.20)),
        url("https://images.unsplash.com/photo-1431324155629-1a6deb1dec8d?q=80&w=1800&auto=format&fit=crop");
    background-size: cover;
    background-position: center;
    box-shadow: 0 24px 60px rgba(0,0,0,0.42);
    margin-bottom: 22px;
}

.hero-title {
    font-size: 58px;
    font-weight: 950;
    line-height: 1.0;
    margin: 0;
}

.hero-title span {
    color: #facc15;
}

.hero-subtitle {
    color: #e2e8f0;
    font-size: 18px;
    margin-top: 14px;
    max-width: 840px;
}

.card {
    background: rgba(8,31,54,0.88);
    border: 1px solid rgba(148,163,184,0.22);
    border-radius: 24px;
    padding: 22px;
    box-shadow: 0 18px 42px rgba(0,0,0,0.28);
    backdrop-filter: blur(10px);
    margin-bottom: 16px;
}

.stat-card {
    background: rgba(8,31,54,0.88);
    border: 1px solid rgba(148,163,184,0.22);
    border-radius: 22px;
    padding: 20px;
    min-height: 118px;
    box-shadow: 0 18px 42px rgba(0,0,0,0.28);
}

.stat-icon {
    font-size: 34px;
}

.stat-number {
    font-size: 30px;
    font-weight: 950;
    color: #f8fafc;
    margin-top: 6px;
}

.stat-label {
    color: #cbd5e1;
    font-size: 14px;
}

.top-card {
    text-align: center;
    border-radius: 24px;
    padding: 22px;
    background: rgba(255,255,255,0.06);
    border: 1px solid rgba(255,255,255,0.12);
    min-height: 230px;
}

.top-card.first {
    background: linear-gradient(135deg, rgba(250,204,21,0.35), rgba(8,31,54,0.90));
    border: 1px solid rgba(250,204,21,0.72);
    box-shadow: 0 0 34px rgba(250,204,21,0.22);
}

.position {
    font-size: 38px;
    font-weight: 950;
    color: #facc15;
}

.avatar {
    width: 72px;
    height: 72px;
    border-radius: 999px;
    margin: 12px auto;
    background: linear-gradient(135deg, #22c55e, #facc15);
    color: #020617;
    font-size: 32px;
    display: flex;
    align-items: center;
    justify-content: center;
    font-weight: 950;
}

.points {
    font-size: 30px;
    color: #22c55e;
    font-weight: 950;
}

.small-muted {
    color: #cbd5e1;
    font-size: 13px;
}

.team-badges {
    display: flex;
    flex-wrap: wrap;
    gap: 12px;
    margin-top: 24px;
}

.team-badge {
    background: rgba(2,6,23,0.62);
    border: 1px solid rgba(255,255,255,0.14);
    border-radius: 18px;
    padding: 10px 13px;
    font-weight: 800;
}

.match-line {
    background: rgba(255,255,255,0.055);
    border: 1px solid rgba(255,255,255,0.09);
    border-radius: 20px;
    padding: 16px;
    margin-bottom: 12px;
}

.admin-warning {
    background: rgba(250,204,21,0.14);
    border: 1px solid rgba(250,204,21,0.35);
    color: #fef9c3;
    border-radius: 18px;
    padding: 15px;
    margin-bottom: 18px;
}

.success-box {
    background: rgba(34,197,94,0.16);
    border: 1px solid rgba(34,197,94,0.35);
    border-radius: 18px;
    padding: 14px;
    color: #bbf7d0;
}

.error-box {
    background: rgba(239,68,68,0.16);
    border: 1px solid rgba(239,68,68,0.35);
    border-radius: 18px;
    padding: 14px;
    color: #fecaca;
}

.stButton > button {
    border-radius: 14px;
    font-weight: 900;
    border: 0;
    background: #facc15;
    color: #020617;
}

.stButton > button:hover {
    background: #fde047;
    color: #020617;
}

div[data-testid="stDataFrame"] {
    border-radius: 18px;
    overflow: hidden;
}

@media (max-width: 768px) {
    .hero-title {
        font-size: 38px;
    }
}
</style>
"""
st.markdown(CUSTOM_CSS, unsafe_allow_html=True)


def get_conn():
    conn = sqlite3.connect(DB_PATH, check_same_thread=False)
    conn.row_factory = sqlite3.Row
    return conn


def hash_password(password: str) -> str:
    return hashlib.sha256(password.encode("utf-8")).hexdigest()


def check_password(password: str, password_hash: str) -> bool:
    return hmac.compare_digest(hash_password(password), password_hash)


def calculate_points(pred_a: int, pred_b: int, real_a: int, real_b: int) -> int:
    pred_result = 1 if pred_a > pred_b else 0 if pred_a == pred_b else -1
    real_result = 1 if real_a > real_b else 0 if real_a == real_b else -1
    pred_diff = pred_a - pred_b
    real_diff = real_a - real_b

    if pred_a == real_a and pred_b == real_b:
        return 10

    if pred_result == real_result and pred_diff == real_diff:
        return 7

    if pred_result == real_result:
        return 5

    return 0


def init_db():
    conn = get_conn()
    cur = conn.cursor()

    cur.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            email TEXT UNIQUE NOT NULL,
            password_hash TEXT NOT NULL,
            role TEXT NOT NULL DEFAULT 'apostador',
            created_at TEXT NOT NULL
        )
    """)

    cur.execute("""
        CREATE TABLE IF NOT EXISTS matches (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            team_a TEXT NOT NULL,
            team_b TEXT NOT NULL,
            match_datetime TEXT NOT NULL,
            score_a INTEGER,
            score_b INTEGER,
            status TEXT NOT NULL DEFAULT 'aberto',
            created_at TEXT NOT NULL
        )
    """)

    cur.execute("""
        CREATE TABLE IF NOT EXISTS predictions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            match_id INTEGER NOT NULL,
            pred_a INTEGER NOT NULL,
            pred_b INTEGER NOT NULL,
            points INTEGER NOT NULL DEFAULT 0,
            updated_at TEXT NOT NULL,
            UNIQUE(user_id, match_id),
            FOREIGN KEY(user_id) REFERENCES users(id),
            FOREIGN KEY(match_id) REFERENCES matches(id)
        )
    """)

    conn.commit()

    admin = cur.execute("SELECT * FROM users WHERE email = ?", ("admin@bolao.com",)).fetchone()
    if not admin:
        cur.execute(
            """
            INSERT INTO users (name, email, password_hash, role, created_at)
            VALUES (?, ?, ?, ?, ?)
            """,
            ("Administrador", "admin@bolao.com", hash_password("admin123"), "admin", datetime.now().isoformat()),
        )

    count_matches = cur.execute("SELECT COUNT(*) AS total FROM matches").fetchone()["total"]
    if count_matches == 0:
        sample_matches = [
            ("Brasil", "França", "2026-06-12 16:00"),
            ("Argentina", "Alemanha", "2026-06-13 16:00"),
            ("Espanha", "Inglaterra", "2026-06-14 16:00"),
            ("Portugal", "Itália", "2026-06-15 16:00"),
            ("México", "EUA", "2026-06-16 18:00"),
            ("Holanda", "Croácia", "2026-06-17 15:00"),
            ("Uruguai", "Japão", "2026-06-18 19:00"),
            ("Marrocos", "Canadá", "2026-06-19 13:00"),
        ]
        for team_a, team_b, dt in sample_matches:
            cur.execute(
                """
                INSERT INTO matches (team_a, team_b, match_datetime, status, created_at)
                VALUES (?, ?, ?, 'aberto', ?)
                """,
                (team_a, team_b, dt, datetime.now().isoformat()),
            )

    conn.commit()
    conn.close()


def create_user(name: str, email: str, password: str):
    conn = get_conn()
    cur = conn.cursor()
    try:
        cur.execute(
            """
            INSERT INTO users (name, email, password_hash, role, created_at)
            VALUES (?, ?, ?, 'apostador', ?)
            """,
            (name.strip(), email.strip().lower(), hash_password(password), datetime.now().isoformat()),
        )
        conn.commit()
        return True, "Cadastro criado com sucesso. Agora faça login."
    except sqlite3.IntegrityError:
        return False, "Este e-mail já está cadastrado."
    finally:
        conn.close()


def login_user(email: str, password: str):
    conn = get_conn()
    user = conn.execute("SELECT * FROM users WHERE email = ?", (email.strip().lower(),)).fetchone()
    conn.close()

    if not user:
        return None

    if not check_password(password, user["password_hash"]):
        return None

    return dict(user)


def logout():
    st.session_state.user = None
    st.rerun()


def require_login():
    if "user" not in st.session_state:
        st.session_state.user = None

    if st.session_state.user is None:
        login_screen()
        st.stop()


def is_admin():
    return st.session_state.user and st.session_state.user.get("role") == "admin"


def get_matches(status=None):
    conn = get_conn()
    if status:
        rows = conn.execute(
            "SELECT * FROM matches WHERE status = ? ORDER BY match_datetime ASC",
            (status,),
        ).fetchall()
    else:
        rows = conn.execute("SELECT * FROM matches ORDER BY match_datetime ASC").fetchall()
    conn.close()
    return [dict(row) for row in rows]


def get_prediction(user_id: int, match_id: int):
    conn = get_conn()
    row = conn.execute(
        "SELECT * FROM predictions WHERE user_id = ? AND match_id = ?",
        (user_id, match_id),
    ).fetchone()
    conn.close()
    return dict(row) if row else None


def save_prediction(user_id: int, match_id: int, pred_a: int, pred_b: int):
    conn = get_conn()
    cur = conn.cursor()
    match = cur.execute("SELECT * FROM matches WHERE id = ?", (match_id,)).fetchone()

    if not match:
        conn.close()
        return False, "Jogo não encontrado."

    if match["status"] != "aberto":
        conn.close()
        return False, "Este jogo já foi encerrado."

    try:
        match_time = datetime.strptime(match["match_datetime"], "%Y-%m-%d %H:%M")
        if datetime.now() >= match_time:
            conn.close()
            return False, "Palpite bloqueado: o jogo já começou."
    except ValueError:
        pass

    cur.execute(
        """
        INSERT INTO predictions (user_id, match_id, pred_a, pred_b, points, updated_at)
        VALUES (?, ?, ?, ?, 0, ?)
        ON CONFLICT(user_id, match_id)
        DO UPDATE SET pred_a = excluded.pred_a,
                      pred_b = excluded.pred_b,
                      updated_at = excluded.updated_at
        """,
        (user_id, match_id, pred_a, pred_b, datetime.now().isoformat()),
    )
    conn.commit()
    conn.close()
    return True, "Palpite salvo com sucesso!"


def add_match(team_a: str, team_b: str, match_datetime: str):
    conn = get_conn()
    conn.execute(
        """
        INSERT INTO matches (team_a, team_b, match_datetime, status, created_at)
        VALUES (?, ?, ?, 'aberto', ?)
        """,
        (team_a, team_b, match_datetime, datetime.now().isoformat()),
    )
    conn.commit()
    conn.close()


def update_match_result(match_id: int, score_a: int, score_b: int):
    conn = get_conn()
    cur = conn.cursor()

    cur.execute(
        """
        UPDATE matches
        SET score_a = ?, score_b = ?, status = 'encerrado'
        WHERE id = ?
        """,
        (score_a, score_b, match_id),
    )

    predictions = cur.execute(
        "SELECT * FROM predictions WHERE match_id = ?",
        (match_id,),
    ).fetchall()

    for prediction in predictions:
        points = calculate_points(
            prediction["pred_a"],
            prediction["pred_b"],
            score_a,
            score_b,
        )

        cur.execute(
            """
            UPDATE predictions
            SET points = ?, updated_at = ?
            WHERE id = ?
            """,
            (points, datetime.now().isoformat(), prediction["id"]),
        )

    conn.commit()
    conn.close()


def reopen_match(match_id: int):
    conn = get_conn()
    conn.execute(
        """
        UPDATE matches
        SET score_a = NULL, score_b = NULL, status = 'aberto'
        WHERE id = ?
        """,
        (match_id,),
    )
    conn.execute(
        """
        UPDATE predictions
        SET points = 0, updated_at = ?
        WHERE match_id = ?
        """,
        (datetime.now().isoformat(), match_id),
    )
    conn.commit()
    conn.close()


def get_ranking():
    conn = get_conn()
    rows = conn.execute(
        """
        SELECT
            u.id,
            u.name,
            u.email,
            COALESCE(SUM(p.points), 0) AS pontos,
            COALESCE(SUM(CASE WHEN p.points > 0 THEN 1 ELSE 0 END), 0) AS palpites_certos,
            COUNT(p.id) AS total_palpites
        FROM users u
        LEFT JOIN predictions p ON p.user_id = u.id
        WHERE u.role = 'apostador'
        GROUP BY u.id, u.name, u.email
        ORDER BY pontos DESC, palpites_certos DESC, total_palpites DESC, u.name ASC
        """
    ).fetchall()
    conn.close()
    return [dict(row) for row in rows]


def get_stats():
    conn = get_conn()
    total_users = conn.execute("SELECT COUNT(*) AS total FROM users WHERE role = 'apostador'").fetchone()["total"]
    total_matches = conn.execute("SELECT COUNT(*) AS total FROM matches").fetchone()["total"]
    finished = conn.execute("SELECT COUNT(*) AS total FROM matches WHERE status = 'encerrado'").fetchone()["total"]
    open_matches = conn.execute("SELECT COUNT(*) AS total FROM matches WHERE status = 'aberto'").fetchone()["total"]
    conn.close()
    ranking = get_ranking()
    leader = ranking[0]["name"] if ranking else "-"
    best_score = ranking[0]["pontos"] if ranking else 0
    return total_users, total_matches, finished, open_matches, leader, best_score


def get_recent_results():
    conn = get_conn()
    rows = conn.execute(
        """
        SELECT *
        FROM matches
        WHERE status = 'encerrado'
        ORDER BY match_datetime DESC
        LIMIT 6
        """
    ).fetchall()
    conn.close()
    return [dict(row) for row in rows]


def team_label(team: str) -> str:
    return f"{TEAMS.get(team, '🏳️')} {team}"


def login_screen():
    st.markdown(
        """
        <div class="hero">
            <p style="font-weight:900; color:#86efac; letter-spacing:4px;">BOLÃO PROFISSIONAL</p>
            <h1 class="hero-title">Bolão da <span>Copa 2026</span></h1>
            <p class="hero-subtitle">
                Faça login, registre seus palpites, acompanhe o ranking geral e dispute o Top 5 apostadores.
            </p>
            <div class="team-badges">
                <div class="team-badge">🇧🇷 Brasil</div>
                <div class="team-badge">🇦🇷 Argentina</div>
                <div class="team-badge">🇫🇷 França</div>
                <div class="team-badge">🇩🇪 Alemanha</div>
                <div class="team-badge">🇪🇸 Espanha</div>
                <div class="team-badge">🇵🇹 Portugal</div>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    col1, col2 = st.columns([1, 1])

    with col1:
        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.subheader("Entrar no bolão")
        email = st.text_input("E-mail", key="login_email")
        password = st.text_input("Senha", type="password", key="login_password")

        if st.button("Entrar", use_container_width=True):
            user = login_user(email, password)
            if user:
                st.session_state.user = user
                st.rerun()
            else:
                st.error("E-mail ou senha inválidos.")
        st.markdown("</div>", unsafe_allow_html=True)

        st.info("Administrador inicial: admin@bolao.com / senha: admin123")

    with col2:
        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.subheader("Criar cadastro")
        name = st.text_input("Nome completo", key="register_name")
        email_reg = st.text_input("E-mail", key="register_email")
        password_reg = st.text_input("Senha", type="password", key="register_password")
        password_confirm = st.text_input("Confirmar senha", type="password", key="register_password_confirm")

        if st.button("Cadastrar", use_container_width=True):
            if not name or not email_reg or not password_reg:
                st.error("Preencha todos os campos.")
            elif password_reg != password_confirm:
                st.error("As senhas não conferem.")
            elif len(password_reg) < 6:
                st.error("A senha precisa ter pelo menos 6 caracteres.")
            else:
                ok, msg = create_user(name, email_reg, password_reg)
                if ok:
                    st.success(msg)
                else:
                    st.error(msg)
        st.markdown("</div>", unsafe_allow_html=True)


def render_sidebar():
    user = st.session_state.user
    st.sidebar.markdown("## ⚽ Bolão da Copa 2026")
    st.sidebar.markdown(f"**Logado como:**  \n{user['name']}")
    st.sidebar.markdown(f"**Tipo:** `{user['role']}`")
    st.sidebar.divider()

    pages = ["Dashboard", "Jogos e Palpites", "Ranking Geral", "Resultados"]
    if user["role"] == "admin":
        pages.append("Painel do Administrador")

    page = st.sidebar.radio("Menu", pages)
    st.sidebar.divider()

    if st.sidebar.button("Sair", use_container_width=True):
        logout()

    return page


def render_dashboard():
    total_users, total_matches, finished, open_matches, leader, best_score = get_stats()

    st.markdown(
        f"""
        <div class="hero">
            <p style="font-weight:900; color:#86efac; letter-spacing:4px;">DASHBOARD OFICIAL</p>
            <h1 class="hero-title">Bolão da <span>Copa 2026</span></h1>
            <p class="hero-subtitle">
                Acompanhe os palpites, veja sua colocação e dispute o topo com todos os apostadores.
            </p>
            <div class="team-badges">
                <div class="team-badge">🇧🇷 Brasil</div>
                <div class="team-badge">🇦🇷 Argentina</div>
                <div class="team-badge">🇫🇷 França</div>
                <div class="team-badge">🇩🇪 Alemanha</div>
                <div class="team-badge">🇪🇸 Espanha</div>
                <div class="team-badge">🇵🇹 Portugal</div>
                <div class="team-badge">🏴 Inglaterra</div>
                <div class="team-badge">🇮🇹 Itália</div>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    c1, c2, c3, c4 = st.columns(4)
    with c1:
        st.markdown(f'<div class="stat-card"><div class="stat-icon">👥</div><div class="stat-number">{total_users}</div><div class="stat-label">Total de Apostadores</div></div>', unsafe_allow_html=True)
    with c2:
        st.markdown(f'<div class="stat-card"><div class="stat-icon">⚽</div><div class="stat-number">{finished}</div><div class="stat-label">Jogos Disputados</div></div>', unsafe_allow_html=True)
    with c3:
        st.markdown(f'<div class="stat-card"><div class="stat-icon">📅</div><div class="stat-number">{open_matches}</div><div class="stat-label">Próximos Jogos</div></div>', unsafe_allow_html=True)
    with c4:
        st.markdown(f'<div class="stat-card"><div class="stat-icon">⭐</div><div class="stat-number">{best_score}</div><div class="stat-label">Melhor Pontuação</div></div>', unsafe_allow_html=True)

    st.write("")
    render_top_five()
    st.write("")
    render_ranking_table()


def render_top_five():
    ranking = get_ranking()[:5]
    st.markdown("## ⭐ Top 5 Apostadores")

    if not ranking:
        st.info("Ainda não há apostadores no ranking.")
        return

    cols = st.columns(5)

    for idx, user in enumerate(ranking):
        class_name = "top-card first" if idx == 0 else "top-card"
        initial = user["name"][:1].upper()
        with cols[idx]:
            st.markdown(
                f"""
                <div class="{class_name}">
                    <div class="position">{idx + 1}º</div>
                    <div class="avatar">{initial}</div>
                    <div style="font-size:18px; font-weight:900;">{user["name"]}</div>
                    <div class="points">{user["pontos"]}</div>
                    <div class="small-muted">pontos</div>
                </div>
                """,
                unsafe_allow_html=True,
            )


def render_ranking_table():
    ranking = get_ranking()

    st.markdown("## 🏆 Ranking Geral")

    if not ranking:
        st.info("Ainda não há ranking.")
        return

    df = pd.DataFrame(ranking)
    df.insert(0, "Posição", range(1, len(df) + 1))
    df = df.rename(
        columns={
            "name": "Nome",
            "pontos": "Pontos",
            "palpites_certos": "Palpites certos",
            "total_palpites": "Total de palpites",
        }
    )

    df = df[["Posição", "Nome", "Pontos", "Palpites certos", "Total de palpites"]]
    st.dataframe(df, use_container_width=True, hide_index=True)


def render_matches_predictions():
    st.markdown("## 🎯 Jogos e Palpites")
    st.caption("Você pode alterar seus palpites até o horário de início do jogo.")

    matches = get_matches()
    user_id = st.session_state.user["id"]

    if not matches:
        st.info("Nenhum jogo cadastrado.")
        return

    for match in matches:
        prediction = get_prediction(user_id, match["id"])
        default_a = prediction["pred_a"] if prediction else 0
        default_b = prediction["pred_b"] if prediction else 0

        st.markdown('<div class="match-line">', unsafe_allow_html=True)
        col1, col2, col3, col4 = st.columns([3, 1, 1, 1])

        with col1:
            st.markdown(f"### {team_label(match['team_a'])} x {team_label(match['team_b'])}")
            st.caption(f"Data: {match['match_datetime']} | Status: {match['status']}")
            if match["status"] == "encerrado":
                st.markdown(f"**Resultado:** {match['score_a']} x {match['score_b']}")

        with col2:
            pred_a = st.number_input(
                f"{match['team_a']}",
                min_value=0,
                max_value=20,
                value=int(default_a),
                key=f"pred_a_{match['id']}",
                disabled=match["status"] != "aberto",
            )

        with col3:
            pred_b = st.number_input(
                f"{match['team_b']}",
                min_value=0,
                max_value=20,
                value=int(default_b),
                key=f"pred_b_{match['id']}",
                disabled=match["status"] != "aberto",
            )

        with col4:
            st.write("")
            st.write("")
            if st.button("Salvar", key=f"save_pred_{match['id']}", disabled=match["status"] != "aberto"):
                ok, msg = save_prediction(user_id, match["id"], int(pred_a), int(pred_b))
                if ok:
                    st.success(msg)
                else:
                    st.error(msg)

        st.markdown("</div>", unsafe_allow_html=True)


def render_results():
    st.markdown("## 📋 Últimos Resultados")
    results = get_recent_results()

    if not results:
        st.info("Ainda não existem jogos encerrados.")
        return

    for match in results:
        st.markdown(
            f"""
            <div class="match-line">
                <strong>{match["match_datetime"]}</strong><br>
                <span style="font-size:22px;">
                    {team_label(match["team_a"])} <strong>{match["score_a"]}</strong>
                    x
                    <strong>{match["score_b"]}</strong> {team_label(match["team_b"])}
                </span>
            </div>
            """,
            unsafe_allow_html=True,
        )


def render_admin():
    if not is_admin():
        st.error("Acesso restrito ao administrador.")
        return

    st.markdown("## 👑 Painel do Administrador")
    st.markdown(
        """
        <div class="admin-warning">
            Aqui o administrador cadastra jogos, lança resultados e o sistema recalcula automaticamente a pontuação.
            Para produção, altere a senha padrão do administrador.
        </div>
        """,
        unsafe_allow_html=True,
    )

    tab1, tab2, tab3 = st.tabs(["Cadastrar jogo", "Lançar resultado", "Usuários"])

    with tab1:
        st.subheader("Cadastrar novo jogo")
        c1, c2 = st.columns(2)
        with c1:
            team_a = st.selectbox("Time A", sorted(TEAMS.keys()), key="new_team_a")
        with c2:
            team_b = st.selectbox("Time B", sorted(TEAMS.keys()), key="new_team_b")

        c3, c4 = st.columns(2)
        with c3:
            date = st.date_input("Data do jogo")
        with c4:
            time = st.time_input("Horário do jogo")

        if st.button("Cadastrar jogo", use_container_width=True):
            if team_a == team_b:
                st.error("Escolha times diferentes.")
            else:
                dt = datetime.combine(date, time).strftime("%Y-%m-%d %H:%M")
                add_match(team_a, team_b, dt)
                st.success("Jogo cadastrado com sucesso.")

    with tab2:
        st.subheader("Lançar resultados")
        matches = get_matches()

        for match in matches:
            st.markdown('<div class="match-line">', unsafe_allow_html=True)
            c1, c2, c3, c4 = st.columns([3, 1, 1, 2])

            with c1:
                st.markdown(f"### {team_label(match['team_a'])} x {team_label(match['team_b'])}")
                st.caption(f"{match['match_datetime']} | Status: {match['status']}")
                if match["status"] == "encerrado":
                    st.markdown(f"Resultado atual: **{match['score_a']} x {match['score_b']}**")

            with c2:
                score_a = st.number_input(
                    match["team_a"],
                    min_value=0,
                    max_value=30,
                    value=int(match["score_a"] or 0),
                    key=f"score_a_{match['id']}",
                )

            with c3:
                score_b = st.number_input(
                    match["team_b"],
                    min_value=0,
                    max_value=30,
                    value=int(match["score_b"] or 0),
                    key=f"score_b_{match['id']}",
                )

            with c4:
                st.write("")
                if st.button("Encerrar e pontuar", key=f"finish_{match['id']}", use_container_width=True):
                    update_match_result(match["id"], int(score_a), int(score_b))
                    st.success("Resultado lançado e pontuação recalculada.")
                    st.rerun()

                if match["status"] == "encerrado":
                    if st.button("Reabrir jogo", key=f"reopen_{match['id']}", use_container_width=True):
                        reopen_match(match["id"])
                        st.warning("Jogo reaberto e pontuação zerada para este jogo.")
                        st.rerun()

            st.markdown("</div>", unsafe_allow_html=True)

    with tab3:
        st.subheader("Usuários cadastrados")
        conn = get_conn()
        users = conn.execute(
            "SELECT id, name, email, role, created_at FROM users ORDER BY created_at DESC"
        ).fetchall()
        conn.close()

        df = pd.DataFrame([dict(u) for u in users])
        if not df.empty:
            df = df.rename(columns={
                "id": "ID",
                "name": "Nome",
                "email": "E-mail",
                "role": "Tipo",
                "created_at": "Criado em",
            })
            st.dataframe(df, use_container_width=True, hide_index=True)
        else:
            st.info("Nenhum usuário cadastrado.")


def main():
    init_db()

    if "user" not in st.session_state:
        st.session_state.user = None

    require_login()
    page = render_sidebar()

    if page == "Dashboard":
        render_dashboard()
    elif page == "Jogos e Palpites":
        render_matches_predictions()
    elif page == "Ranking Geral":
        render_top_five()
        render_ranking_table()
    elif page == "Resultados":
        render_results()
    elif page == "Painel do Administrador":
        render_admin()


if __name__ == "__main__":
    main()
