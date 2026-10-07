import streamlit as st
import time
import textwrap

# Intentar cargar streamlit-option-menu para navegación moderna
try:
    from streamlit_option_menu import option_menu
    HAS_OPTION_MENU = True
except ImportError:
    HAS_OPTION_MENU = False

# ---------------------------------------------------------
# CONFIGURACIÓN DE PÁGINA
# ---------------------------------------------------------
st.set_page_config(
    page_title="Reponedor Rush - Supermarket Simulator 3D",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# ---------------------------------------------------------
# GENERADOR SVG AUTO-CONTENIDO (ESTANTERÍA Y CAJAS 3D)
# ---------------------------------------------------------
def get_shelf_box_svg(stock_pct, store_type):
    """Genera una estantería con cajas apiladas en 3D sin sangría Markdown."""
    if store_type == "Mecánica":
        color_top, color_side, color_front = "#f97316", "#c2410c", "#ea580c"
        bg_shelf = "#1e140a"
    elif store_type == "Tecnología":
        color_top, color_side, color_front = "#38bdf8", "#0284c7", "#0369a1"
        bg_shelf = "#081d2c"
    else: # Carpintería
        color_top, color_side, color_front = "#eab308", "#a16207", "#ca8a04"
        bg_shelf = "#1d1508"

    if stock_pct <= 0:
        return textwrap.dedent("""\
        <svg width="100%" height="110" viewBox="0 0 160 110" style="background: rgba(0,0,0,0.3); border-radius: 8px;">
        <rect x="10" y="95" width="140" height="8" fill="#475569" rx="2"/>
        <text x="80" y="50" font-size="28" text-anchor="middle" fill="#ef4444">⚠️</text>
        <text x="80" y="75" font-size="11" font-weight="800" text-anchor="middle" fill="#fca5a5" letter-spacing="1">ESTANTE VACÍO</text>
        </svg>""")

    box_count = 1
    if stock_pct > 75: box_count = 4
    elif stock_pct > 50: box_count = 3
    elif stock_pct > 25: box_count = 2

    positions = [(20, 48), (85, 48), (52, 18), (85, 18)]
    boxes_xml = ""
    for i in range(box_count):
        x, y = positions[i]
        boxes_xml += f'<g transform="translate({x}, {y})"><polygon points="20,5 38,14 20,22 2,14" fill="{color_top}"/><polygon points="2,14 20,22 20,40 2,32" fill="{color_side}"/><polygon points="20,22 38,14 38,32 20,40" fill="{color_front}"/><rect x="18" y="8" width="4" height="30" fill="#ffffff" opacity="0.35"/></g>'

    return textwrap.dedent(f"""\
    <svg width="100%" height="110" viewBox="0 0 160 110" style="background: {bg_shelf}; border-radius: 8px; border: 1px solid rgba(255,255,255,0.08);">
    <rect x="5" y="92" width="150" height="10" rx="3" fill="#475569"/>
    <rect x="5" y="98" width="150" height="4" rx="1" fill="#1e293b"/>
    {boxes_xml}
    </svg>""")

# ---------------------------------------------------------
# ESTADO DEL JUEGO
# ---------------------------------------------------------
def reset_game():
    st.session_state.game_state = "PLAYING"
    st.session_state.current_store = "Mecánica"
    st.session_state.global_timer = 300
    st.session_state.start_time = time.time()
    st.session_state.last_tick = time.time()
    st.session_state.active_alert = None
    st.session_state.fail_reason = ""
    st.session_state.score = 0
    
    st.session_state.inventario = {
        "Mecánica": [
            {"id": 101, "nombre": "Filtro de Aceite", "stock": 90, "speed": 3.2},
            {"id": 102, "nombre": "Pastillas de Freno", "stock": 70, "speed": 4.1},
            {"id": 103, "nombre": "Batería 12V Pro", "stock": 85, "speed": 2.9},
        ],
        "Tecnología": [
            {"id": 201, "nombre": "Procesador OctaCore", "stock": 80, "speed": 4.5},
            {"id": 202, "nombre": "Tarjeta Gráfica RTX", "stock": 65, "speed": 5.2},
            {"id": 203, "nombre": "Monitor Gamer 240Hz", "stock": 75, "speed": 3.4},
        ],
        "Carpintería": [
            {"id": 301, "nombre": "Disco de Sierra 12''", "stock": 95, "speed": 3.0},
            {"id": 302, "nombre": "Taladro Inalámbrico", "stock": 60, "speed": 4.3},
            {"id": 303, "nombre": "Barniz Mate Roble", "stock": 80, "speed": 3.7},
        ]
    }

if "game_state" not in st.session_state:
    st.session_state.game_state = "MENU"

# ---------------------------------------------------------
# ESTILOS DINÁMICOS POR TIENDA
# ---------------------------------------------------------
store_bg = "#0b0d12"
accent_color = "#6366f1"

if st.session_state.get("game_state") == "PLAYING":
    curr = st.session_state.get("current_store", "Mecánica")
    if curr == "Mecánica":
        store_bg = "linear-gradient(135deg, #18110c 0%, #0d0f14 100%)"
        accent_color = "#f97316"
    elif curr == "Tecnología":
        store_bg = "linear-gradient(135deg, #091322 0%, #05070c 100%)"
        accent_color = "#38bdf8"
    else:
        store_bg = "linear-gradient(135deg, #1c130b 0%, #0c0805 100%)"
        accent_color = "#eab308"

st.markdown(textwrap.dedent(f"""\
<style>
.stApp {{
    background: {store_bg};
    color: #f8fafc;
    font-family: 'Inter', system-ui, sans-serif;
}}

#MainMenu, header, footer {{visibility: hidden;}}

div.stButton > button {{
    background: linear-gradient(135deg, #1e293b 0%, #0f172a 100%);
    color: #f8fafc;
    border: 1px solid #334155;
    border-radius: 10px;
    padding: 10px 14px;
    font-weight: 800;
    font-size: 12px;
    transition: all 0.2s cubic-bezier(0.175, 0.885, 0.32, 1.275);
    width: 100%;
    cursor: pointer;
    text-transform: uppercase;
    letter-spacing: 0.5px;
}}

div.stButton > button:hover {{
    transform: translateY(-2px) scale(1.02);
    border-color: {accent_color};
    color: #ffffff;
    box-shadow: 0 6px 18px {accent_color}40;
}}

div.stButton > button:active {{
    transform: translateY(1px) scale(0.98);
}}

.emergency-banner {{
    background: linear-gradient(90deg, #742a2a 0%, #9b2c2c 50%, #742a2a 100%);
    border: 2px solid #ef4444;
    border-radius: 12px;
    padding: 12px 20px;
    margin-bottom: 18px;
    display: flex;
    justify-content: space-between;
    align-items: center;
    box-shadow: 0 0 20px rgba(239, 68, 68, 0.5);
}}

.hud-box {{
    background: #0f172a;
    border: 1px solid #1e293b;
    padding: 10px 16px;
    border-radius: 10px;
    text-align: center;
}}
</style>"""), unsafe_allow_html=True)

# ---------------------------------------------------------
# VISTA 1: MENÚ INICIAL
# ---------------------------------------------------------
if st.session_state.game_state == "MENU":
    st.markdown("<br><br>", unsafe_allow_html=True)
    c1, c2, c3 = st.columns([1, 2, 1])
    with c2:
        st.markdown(textwrap.dedent("""\
        <div style='background: #0f172a; padding: 35px; border-radius: 20px; border: 1px solid #1e293b; text-align: center;'>
        <span style='background:#312e81; color:#c7d2fe; font-size:11px; font-weight:800; padding:4px 10px; border-radius:6px;'>SIMULADOR DE ALMACÉN</span>
        <h1 style='color:#ffffff; margin:12px 0 0 0; font-size:30px;'>REPONEDOR RUSH 3D</h1>
        <p style='color:#94a3b8; font-size:14px; margin-top:6px;'>Estilo Supermarket Simulator</p>
        <hr style='border-color:#1e293b; margin:20px 0;'>
        <div style='text-align:left; color:#cbd5e1; font-size:13px; line-height:1.7;'>
        • <strong>3 Sectores Inmersivos:</strong> Taller Mecánico, Tienda Tech y Carpintería.<br>
        • <strong>Venta en Vivo:</strong> Los clientes consumen stock de las 3 tiendas al mismo tiempo.<br>
        • <strong>Alerta de Emergencia:</strong> Si un estante llega al 0%, tendrás <strong>30 SEGUNDOS</strong> para ir y reponerlo.<br>
        • <strong>Objetivo:</strong> Sobrevivir el turno de 5 minutos.
        </div>
        </div>"""), unsafe_allow_html=True)
        st.markdown("<br>", unsafe_allow_html=True)
        if st.button("COMENZAR TURNO DE REPONEDOR ⚡"):
            reset_game()
            st.rerun()

# ---------------------------------------------------------
# VISTA 2: GAME OVER / VICTORIA
# ---------------------------------------------------------
elif st.session_state.game_state in ["GAMEOVER", "WIN"]:
    st.markdown("<br><br>", unsafe_allow_html=True)
    c1, c2, c3 = st.columns([1, 2, 1])
    with c2:
        if st.session_state.game_state == "GAMEOVER":
            st.markdown(textwrap.dedent(f"""\
            <div style='background: #1c1010; padding: 35px; border-radius: 20px; border: 2px solid #ef4444; text-align: center;'>
            <h1 style='color:#ef4444; margin:0; font-size:28px;'>TE HAS QUEDADO SIN STOCK</h1>
            <p style='color:#fca5a5; font-size:14px; margin-top:10px;'>{st.session_state.fail_reason}</p>
            <h3 style='color:#fff; margin-top:15px;'>Puntaje Final: {st.session_state.score} PTS</h3>
            </div>"""), unsafe_allow_html=True)
        else:
            st.markdown(textwrap.dedent(f"""\
            <div style='background: #0f291e; padding: 35px; border-radius: 20px; border: 2px solid #22c55e; text-align: center;'>
            <h1 style='color:#22c55e; margin:0; font-size:28px;'>¡TURNO COMPLETADO CON ÉXITO!</h1>
            <p style='color:#bbf7d0; font-size:14px; margin-top:10px;'>Mantuviste reabastecidos los 3 sectores del almacén.</p>
            <h3 style='color:#fff; margin-top:15px;'>Puntaje Final: {st.session_state.score} PTS</h3>
            </div>"""), unsafe_allow_html=True)

        st.markdown("<br>", unsafe_allow_html=True)
        if st.button("JUGAR OTRO TURNO"):
            reset_game()
            st.rerun()

# ---------------------------------------------------------
# VISTA 3: BUCLE PRINCIPAL DE JUEGO (PLAYING)
# ---------------------------------------------------------
else:
    # --- BUCLE DE TIEMPO REAL ---
    now = time.time()
    dt = now - st.session_state.last_tick
    st.session_state.last_tick = now

    # 1. Consumo continuo de stock
    for store_name, items in st.session_state.inventario.items():
        for item in items:
            item["stock"] = max(0.0, item["stock"] - (item["speed"] * dt * 1.2))

            # Disparar Alerta Crítica
            if item["stock"] == 0 and st.session_state.active_alert is None:
                st.session_state.active_alert = {
                    "store": store_name,
                    "item_id": item["id"],
                    "item_name": item["nombre"],
                    "deadline": time.time() + 30.0
                }

    # 2. Control de Alerta
    if st.session_state.active_alert is not None:
        time_left_alert = st.session_state.active_alert["deadline"] - time.time()
        alert_store = st.session_state.active_alert["store"]
        alert_id = st.session_state.active_alert["item_id"]
        target_item = next(x for x in st.session_state.inventario[alert_store] if x["id"] == alert_id)
        
        if target_item["stock"] > 0:
            st.session_state.active_alert = None
        elif time_left_alert <= 0:
            st.session_state.game_state = "GAMEOVER"
            st.session_state.fail_reason = f"Se agotó el tiempo de réplica (30s) para reponer '{st.session_state.active_alert['item_name']}' en {alert_store}."
            st.rerun()

    # 3. Temporizador Global de 5 Minutos
    elapsed_global = time.time() - st.session_state.start_time
    remaining_global = max(0, st.session_state.global_timer - elapsed_global)
    if remaining_global <= 0:
        st.session_state.game_state = "WIN"
        st.rerun()

    # --- BARRA SUPERIOR HUD ---
    mins = int(remaining_global // 60)
    secs = int(remaining_global % 60)

    h1, h2, h3 = st.columns([2, 2, 1])
    with h1:
        st.markdown(textwrap.dedent(f"""\
        <div class='hud-box'>
        <span style='color:#94a3b8; font-size:11px; font-weight:800;'>TIEMPO RESTANTE</span>
        <div style='font-size:22px; font-weight:900; color:#818cf8;'>{mins:02d}:{secs:02d}</div>
        </div>"""), unsafe_allow_html=True)
    with h2:
        st.markdown(textwrap.dedent(f"""\
        <div class='hud-box'>
        <span style='color:#94a3b8; font-size:11px; font-weight:800;'>PUNTAJE REPONEDOR</span>
        <div style='font-size:22px; font-weight:900; color:#22c55e;'>{st.session_state.score} PTS</div>
        </div>"""), unsafe_allow_html=True)
    with h3:
        if st.button("REINICIAR"):
            reset_game()
            st.rerun()

    st.markdown("<br>", unsafe_allow_html=True)

    # --- BANNER DE ALERTA DE EMERGENCIA ---
    if st.session_state.active_alert is not None:
        t_alert = max(0, int(st.session_state.active_alert["deadline"] - time.time()))
        st.markdown(textwrap.dedent(f"""\
        <div class='emergency-banner'>
        <div>
        <strong style='color:#fff; font-size:15px;'>
        ⚠️ ¡ALERTA URGENTE EN {st.session_state.active_alert['store'].upper()}!
        </strong>
        <div style='color:#fca5a5; font-size:12px; margin-top:2px;'>
        Estante vacío: {st.session_state.active_alert['item_name']}
        </div>
        </div>
        <div style='text-align:right;'>
        <span style='font-size:11px; color:#fca5a5; font-weight:800;'>TIEMPO RÉPLICA</span>
        <div style='font-size:24px; font-weight:900; color:#fff;'>{t_alert}s</div>
        </div>
        </div>"""), unsafe_allow_html=True)

    # --- NAVEGACIÓN ENTRE TIENDAS ---
    if HAS_OPTION_MENU:
        selected = option_menu(
            menu_title=None,
            options=["Mecánica", "Tecnología", "Carpintería"],
            icons=["tools", "cpu", "hammer"],
            default_index=["Mecánica", "Tecnología", "Carpintería"].index(st.session_state.current_store),
            orientation="horizontal",
            styles={
                "container": {"padding": "0!important", "background-color": "#0f172a", "border-radius": "12px"},
                "nav-link": {"font-size": "13px", "text-align": "center", "color": "#94a3b8", "font-weight": "800", "text-transform": "uppercase"},
                "nav-link-selected": {"background-color": "#1e1b4b", "color": "#ffffff", "border-radius": "10px"},
            }
        )
        st.session_state.current_store = selected
    else:
        st.session_state.current_store = st.radio("Sector:", ["Mecánica", "Tecnología", "Carpintería"], horizontal=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # --- CABECERA DE LA TIENDA ACTUAL ---
    st.markdown(textwrap.dedent(f"""\
    <div style='background: rgba(15, 23, 42, 0.7); border: 1px solid #1e293b; border-radius: 12px; padding: 12px 20px; margin-bottom: 15px; display:flex; justify-content:space-between; align-items:center;'>
    <span style='font-weight:900; color:#f8fafc; font-size:15px; letter-spacing:1px;'>
    SECTOR ACTUAL: {st.session_state.current_store.upper()}
    </span>
    <span style='font-size:12px; color:#818cf8; font-weight:800;'>3 ESTANTES EN VIVO</span>
    </div>"""), unsafe_allow_html=True)

    # --- ESTANTERÍAS DE PRODUCTOS ---
    current_items = st.session_state.inventario[st.session_state.current_store]
    cols = st.columns(len(current_items))

    for idx, item in enumerate(current_items):
        with cols[idx]:
            st_val = int(item["stock"])
            svg_shelf = get_shelf_box_svg(st_val, st.session_state.current_store)

            # Tarjeta de producto 100% autocontenida sin sangría
            st.markdown(textwrap.dedent(f"""\
            <div style='background: rgba(15, 23, 42, 0.7); border: 1px solid #1e293b; border-radius: 14px; padding: 16px; text-align: center;'>
            <div style='font-size:11px; font-weight:800; color:#818cf8;'>ID #{item['id']}</div>
            <div style='margin: 10px 0;'>
            {svg_shelf}
            </div>
            <div style='font-weight:800; font-size:14px; color:#f8fafc;'>{item['nombre']}</div>
            <div style='font-size:12px; color:#94a3b8; margin-top:4px;'>
            STOCK ESTANTE: <strong style='color:{"#ef4444" if st_val < 25 else "#22c55e"};'>{st_val}%</strong>
            </div>
            </div>"""), unsafe_allow_html=True)

            st.markdown("<br>", unsafe_allow_html=True)

            # Botón interactivo de reposición
            if st.button(f"REPONER ESTANTE (+40%)", key=f"btn_repon_{item['id']}"):
                item["stock"] = min(100.0, item["stock"] + 40.0)
                st.session_state.score += 20
                st.rerun()

    # Actualización automática fluida cada 0.4s
    time.sleep(0.4)
    st.rerun()
