import streamlit as st
import time
import random

# Intentar cargar streamlit-option-menu para navegación moderna
try:
    from streamlit_option_menu import option_menu
    HAS_OPTION_MENU = True
except ImportError:
    HAS_OPTION_MENU = False

# ---------------------------------------------------------
# CONFIGURACIÓN DE PÁGINA (WIDE + GAME HUD MATE)
# ---------------------------------------------------------
st.set_page_config(
    page_title="Reponedor Rush HUD - Game Simulator",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# ---------------------------------------------------------
# GENERADORES SVG VECTORIALES (SIN EMOJIS EN DISEÑO)
# ---------------------------------------------------------
def get_box_svg(status="full", store_type="mecánica"):
    """Genera cajas 3D en SVG mate según tienda y nivel de stock."""
    # Color base por tipo de tienda
    if store_type == "mecánica":
        base_color = "#2b5c8f" if status == "full" else ("#785327" if status == "medium" else "#8c2828")
        top_color  = "#3a7bd5" if status == "full" else ("#a87336" if status == "medium" else "#b83b3b")
    elif store_type == "tecnología":
        base_color = "#276e5a" if status == "full" else ("#785327" if status == "medium" else "#8c2828")
        top_color  = "#3498db" if status == "full" else ("#a87336" if status == "medium" else "#b83b3b")
    else: # carpintería
        base_color = "#704820" if status == "full" else ("#785327" if status == "medium" else "#8c2828")
        top_color  = "#a06830" if status == "full" else ("#a87336" if status == "medium" else "#b83b3b")

    if status != "empty":
        return f"""
        <svg width="100" height="100" viewBox="0 0 100 100" style="filter: drop-shadow(0px 8px 12px rgba(0,0,0,0.5));">
            <polygon points="50,15 85,32 50,48 15,32" fill="{top_color}"/>
            <polygon points="15,32 50,48 50,85 15,68" fill="{base_color}"/>
            <polygon points="50,48 85,32 85,68 50,85" fill="{base_color}" opacity="0.8"/>
            <polygon points="45,18 55,23 55,83 45,78" fill="#e2e8f0" opacity="0.6"/>
            <rect x="58" y="52" width="18" height="12" rx="2" fill="#0f172a" opacity="0.7"/>
        </svg>
        """
    else:
        # Caja Vacía con Alerta Parpadeante Vectorial
        return """
        <svg width="100" height="100" viewBox="0 0 100 100" style="filter: drop-shadow(0px 0px 15px rgba(245, 101, 101, 0.6));">
            <polygon points="50,20 85,35 50,50 15,35" fill="#0f0505"/>
            <polygon points="15,35 50,50 15,40" fill="#742a2a"/>
            <polygon points="85,35 50,50 85,40" fill="#9b2c2c"/>
            <polygon points="15,35 50,50 50,85 15,68" fill="#521d1d"/>
            <polygon points="50,50 85,35 85,68 50,85" fill="#742a2a"/>
            <polygon points="50,26 58,41 42,41" fill="#f56565"/>
            <rect x="49.2" y="30" width="1.6" height="6" fill="#1a202c"/>
            <circle cx="50" cy="38" r="1" fill="#1a202c"/>
        </svg>
        """

# ---------------------------------------------------------
# ESTILOS CSS MATE + BANNERS DE ALERTA DE EMERGENCIA
# ---------------------------------------------------------
st.markdown("""
<style>
    .stApp {
        background-color: #0b0d12;
        color: #e2e8f0;
        font-family: 'Inter', system-ui, -apple-system, sans-serif;
    }

    #MainMenu, header, footer {visibility: hidden;}

    /* Botones con animación Burbuja Bounce */
    div.stButton > button {
        background: linear-gradient(135deg, #1e2636 0%, #131822 100%);
        color: #f1f5f9;
        border: 1px solid #2d3748;
        border-radius: 12px;
        padding: 10px 16px;
        font-weight: 800;
        font-size: 13px;
        letter-spacing: 0.5px;
        transition: all 0.2s cubic-bezier(0.175, 0.885, 0.32, 1.275);
        box-shadow: 0 4px 12px rgba(0,0,0,0.4);
        width: 100%;
        cursor: pointer;
        text-transform: uppercase;
    }

    div.stButton > button:hover {
        transform: translateY(-3px) scale(1.02);
        background: linear-gradient(135deg, #313d54 0%, #1e2636 100%);
        border-color: #6366f1;
        color: #ffffff;
        box-shadow: 0 8px 20px rgba(99, 102, 241, 0.35);
    }

    div.stButton > button:active {
        transform: translateY(1px) scale(0.97);
    }

    /* BANNERS DE ALERTA DE EMERGENCIA (30s Countdown) */
    .emergency-banner {
        background: linear-gradient(90deg, #742a2a 0%, #9b2c2c 50%, #742a2a 100%);
        border: 2px solid #f56565;
        border-radius: 14px;
        padding: 14px 20px;
        margin-bottom: 20px;
        display: flex;
        justify-content: space-between;
        align-items: center;
        animation: pulseRed 1s infinite alternate;
        box-shadow: 0 0 25px rgba(245, 101, 101, 0.4);
    }

    @keyframes pulseRed {
        from { box-shadow: 0 0 10px rgba(245, 101, 101, 0.3); }
        to { box-shadow: 0 0 25px rgba(245, 101, 101, 0.8); }
    }

    /* Estantería Industrial */
    .shelf-container {
        background: linear-gradient(180deg, rgba(20, 26, 38, 0.9) 0%, rgba(11, 13, 18, 0.95) 100%);
        border: 1px solid #232d3f;
        border-radius: 16px;
        padding: 20px;
        margin-bottom: 20px;
    }

    .box-slot {
        background: rgba(255,255,255,0.02);
        border: 1px dashed #2d3748;
        border-radius: 14px;
        padding: 14px;
        text-align: center;
        min-height: 230px;
        display: flex;
        flex-direction: column;
        justify-content: space-between;
        align-items: center;
    }

    .hud-stat {
        background: #151a24;
        border: 1px solid #232d3f;
        padding: 12px 18px;
        border-radius: 12px;
        text-align: center;
    }

    .dot-led {
        height: 10px;
        width: 10px;
        border-radius: 50%;
        display: inline-block;
        margin-right: 6px;
    }
    .dot-green { background: #48bb78; box-shadow: 0 0 8px #48bb78; }
    .dot-red { background: #f56565; box-shadow: 0 0 8px #f56565; animation: blink 0.8s infinite; }

    @keyframes blink { 0%, 100% { opacity: 1; } 50% { opacity: 0.2; } }
</style>
""", unsafe_allow_html=True)

# ---------------------------------------------------------
# INICIALIZACIÓN DEL ESTADO DEL JUEGO
# ---------------------------------------------------------
def reset_game():
    st.session_state.game_state = "PLAYING" # MENU, PLAYING, GAMEOVER, WIN
    st.session_state.current_store = "Mecánica"
    st.session_state.global_timer = 300 # 5 minutos (300s)
    st.session_state.start_time = time.time()
    st.session_state.last_tick = time.time()
    st.session_state.active_alert = None # {"store": "", "item_name": "", "deadline": 0}
    st.session_state.fail_reason = ""
    st.session_state.score = 0
    
    # Inventario de las 3 Tiendas
    st.session_state.inventario = {
        "Mecánica": [
            {"id": 101, "nombre": "Filtros de Aceite", "stock": 90, "max": 100, "speed": 3.5},
            {"id": 102, "nombre": "Pastillas de Freno", "stock": 70, "max": 100, "speed": 4.0},
            {"id": 103, "nombre": "Baterías 12V High-Power", "stock": 80, "max": 100, "speed": 2.8},
        ],
        "Tecnología": [
            {"id": 201, "nombre": "Procesadores & Chipsets", "stock": 85, "max": 100, "speed": 4.5},
            {"id": 202, "nombre": "Tarjetas Gráficas RTX", "stock": 60, "max": 100, "speed": 5.0},
            {"id": 203, "nombre": "Monitores Gamer 240Hz", "stock": 75, "max": 100, "speed": 3.2},
        ],
        "Carpintería": [
            {"id": 301, "nombre": "Juegos de Discos Sierra", "stock": 95, "max": 100, "speed": 3.0},
            {"id": 302, "nombre": "Taladros Perforadores", "stock": 65, "max": 100, "speed": 4.2},
            {"id": 303, "nombre": "Cajas de Barniz Mate", "stock": 80, "max": 100, "speed": 3.8},
        ]
    }

if "game_state" not in st.session_state:
    st.session_state.game_state = "MENU"

# ---------------------------------------------------------
# PANTALLA 1: MENÚ PRINCIPAL
# ---------------------------------------------------------
if st.session_state.game_state == "MENU":
    st.markdown("<br><br>", unsafe_allow_html=True)
    c1, c2, c3 = st.columns([1, 2, 1])
    with c2:
        st.markdown("""
        <div style='background: #141822; padding: 35px; border-radius: 20px; border: 1px solid #283245; text-align: center; box-shadow: 0 15px 35px rgba(0,0,0,0.6);'>
            <span style='background:#312e81; color:#c7d2fe; font-size:11px; font-weight:800; padding:4px 10px; border-radius:6px;'>SIMULADOR DE TIEMPO REAL</span>
            <h1 style='color:#ffffff; margin:12px 0 0 0; font-size:32px; letter-spacing:1px;'>REPONEDOR RUSH 3D</h1>
            <p style='color:#94a3b8; font-size:14px; margin-top:8px;'>Mantén abastecidas las 3 tiendas antes de que se agote el tiempo global.</p>
            <hr style='border-color:#263042; margin:20px 0;'>
            <div style='text-align:left; color:#cbd5e1; font-size:13px; line-height:1.7;'>
                • <strong>3 Sectores:</strong> Mecánica, Tecnología y Carpintería.<br>
                • <strong>Desgaste en Vivo:</strong> Los clientes consumen stock en todas las tiendas en simultáneo.<br>
                • <strong>Alertas de Emergencia:</strong> Si una caja llega a 0, tendrás <strong>30 SEGUNDOS DE REPLICA</strong> para ir a esa tienda y reponerla.<br>
                • <strong>Meta:</strong> Sobrevivir los 5 minutos sin que ninguna alerta venza.
            </div>
        </div>
        """, unsafe_allow_html=True)
        st.markdown("<br>", unsafe_allow_html=True)
        if st.button("INICIAR PARTIDA DE REPONEDOR"):
            reset_game()
            st.rerun()

# ---------------------------------------------------------
# PANTALLA 2: GAME OVER O VICTORIA
# ---------------------------------------------------------
elif st.session_state.game_state in ["GAMEOVER", "WIN"]:
    st.markdown("<br><br>", unsafe_allow_html=True)
    c1, c2, c3 = st.columns([1, 2, 1])
    with c2:
        if st.session_state.game_state == "GAMEOVER":
            st.markdown(f"""
            <div style='background: #1c1010; padding: 35px; border-radius: 20px; border: 2px solid #f56565; text-align: center;'>
                <span style='background:#742a2a; color:#fff; font-size:12px; font-weight:900; padding:4px 10px; border-radius:6px;'>GAME OVER</span>
                <h1 style='color:#f56565; margin:10px 0; font-size:30px;'>TE HAS QUEDADO SIN STOCK</h1>
                <p style='color:#feb2b2; font-size:14px;'>{st.session_state.fail_reason}</p>
                <h3 style='color:#fff; margin-top:15px;'>Puntaje Final: {st.session_state.score} pts</h3>
            </div>
            """, unsafe_allow_html=True)
        else:
            st.markdown(f"""
            <div style='background: #0f291e; padding: 35px; border-radius: 20px; border: 2px solid #48bb78; text-align: center;'>
                <span style='background:#1c5436; color:#fff; font-size:12px; font-weight:900; padding:4px 10px; border-radius:6px;'>VICTORIA</span>
                <h1 style='color:#48bb78; margin:10px 0; font-size:30px;'>¡TURNO COMPLETADO CON ÉXITO!</h1>
                <p style='color:#c6f6d5; font-size:14px;'>Has mantenido abastecidas las 3 tiendas durante los 5 minutos.</p>
                <h3 style='color:#fff; margin-top:15px;'>Puntaje Final: {st.session_state.score} pts</h3>
            </div>
            """, unsafe_allow_html=True)

        st.markdown("<br>", unsafe_allow_html=True)
        if st.button("JUGAR DE NUEVO"):
            reset_game()
            st.rerun()

# ---------------------------------------------------------
# PANTALLA 3: BUCLE PRINCIPAL DEL JUEGO (PLAYING)
# ---------------------------------------------------------
else:
    # --- BUCLE DE TIEMPO REAL (TICK GAME LOOP) ---
    now = time.time()
    dt = now - st.session_state.last_tick
    st.session_state.last_tick = now

    # 1. Calcular Desgaste de Stock en las 3 Tiendas
    for store_name, items in st.session_state.inventario.items():
        for item in items:
            # Consumo constante ajustado por velocidad aleatoria corta
            item["stock"] = max(0.0, item["stock"] - (item["speed"] * dt * 1.2))

            # Disparar Alerta de Emergencia si stock llega a 0 y no hay otra activa
            if item["stock"] == 0 and st.session_state.active_alert is None:
                st.session_state.active_alert = {
                    "store": store_name,
                    "item_id": item["id"],
                    "item_name": item["nombre"],
                    "deadline": time.time() + 30.0 # 30 segundos de plazo
                }

    # 2. Verificar Estado de la Alerta Activa
    if st.session_state.active_alert is not None:
        time_left_alert = st.session_state.active_alert["deadline"] - time.time()
        
        # Si la caja con alerta fue reabastecida (>0), limpiar alerta
        alert_store = st.session_state.active_alert["store"]
        alert_id = st.session_state.active_alert["item_id"]
        target_item = next(x for x in st.session_state.inventario[alert_store] if x["id"] == alert_id)
        
        if target_item["stock"] > 0:
            st.session_state.active_alert = None
        elif time_left_alert <= 0:
            # ¡TIEMPO AGOTADO! GAME OVER
            st.session_state.game_state = "GAMEOVER"
            st.session_state.fail_reason = f"No reabasteciste '{st.session_state.active_alert['item_name']}' en {alert_store} dentro de los 30s de réplica."
            st.rerun()

    # 3. Verificar Tiempo Global (5 Minutos)
    elapsed_global = time.time() - st.session_state.start_time
    remaining_global = max(0, st.session_state.global_timer - elapsed_global)
    if remaining_global <= 0:
        st.session_state.game_state = "WIN"
        st.rerun()

    # --- BARRA SUPERIOR HUD (TIEMPO GLOBAL Y PUNTAJE) ---
    mins = int(remaining_global // 60)
    secs = int(remaining_global % 60)

    h1, h2, h3 = st.columns([2, 2, 1])
    with h1:
        st.markdown(f"""
        <div class='hud-stat'>
            <span style='color:#94a3b8; font-size:11px; font-weight:800;'>TIEMPO RESTANTE TURNO</span>
            <div style='font-size:24px; font-weight:900; color:#818cf8;'>{mins:02d}:{secs:02d}</div>
        </div>
        """, unsafe_allow_html=True)
    with h2:
        st.markdown(f"""
        <div class='hud-stat'>
            <span style='color:#94a3b8; font-size:11px; font-weight:800;'>PUNTAJE BODEGA</span>
            <div style='font-size:24px; font-weight:900; color:#48bb78;'>{st.session_state.score} PTS</div>
        </div>
        """, unsafe_allow_html=True)
    with h3:
        if st.button("REINICIAR"):
            reset_game()
            st.rerun()

    st.markdown("<br>", unsafe_allow_html=True)

    # --- BANNER DE ALERTA CRÍTICA (REPLICA 30 SEGUNDOS) ---
    if st.session_state.active_alert is not None:
        t_alert = max(0, int(st.session_state.active_alert["deadline"] - time.time()))
        st.markdown(f"""
        <div class='emergency-banner'>
            <div>
                <span class='dot-led dot-red'></span>
                <strong style='color:#fff; font-size:15px; letter-spacing:0.5px;'>
                    ¡ALERTA URGENTE SIN STOCK EN TIENDA {st.session_state.active_alert['store'].upper()}!
                </strong>
                <div style='color:#fca5a5; font-size:12px; margin-top:2px;'>
                    Caja afectada: {st.session_state.active_alert['item_name']}
                </div>
            </div>
            <div style='text-align:right;'>
                <span style='font-size:11px; color:#feb2b2; font-weight:800;'>TIEMPO RÉPLICA</span>
                <div style='font-size:26px; font-weight:900; color:#fff;'>{t_alert}s</div>
            </div>
        </div>
        """, unsafe_allow_html=True)

    # --- SELECTOR DE TIENDAS / SECTORES ---
    if HAS_OPTION_MENU:
        selected = option_menu(
            menu_title=None,
            options=["Mecánica", "Tecnología", "Carpintería"],
            icons=["tools", "cpu", "hammer"],
            default_index=["Mecánica", "Tecnología", "Carpintería"].index(st.session_state.current_store),
            orientation="horizontal",
            styles={
                "container": {"padding": "0!important", "background-color": "#151a24", "border-radius": "12px"},
                "nav-link": {"font-size": "13px", "text-align": "center", "color": "#94a3b8", "font-weight": "800", "text-transform": "uppercase"},
                "nav-link-selected": {"background-color": "#312e81", "color": "#ffffff", "border-radius": "10px"},
            }
        )
        st.session_state.current_store = selected
    else:
        st.session_state.current_store = st.radio("Selecciona Tienda:", ["Mecánica", "Tecnología", "Carpintería"], horizontal=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # --- ESTANTERÍA DE LA TIENDA ACTUAL ---
    current_items = st.session_state.inventario[st.session_state.current_store]

    st.markdown(f"""
    <div class='shelf-container'>
        <div style='display:flex; justify-content:space-between; align-items:center; margin-bottom:15px; border-bottom:1px solid #232d3f; padding-bottom:10px;'>
            <span style='font-weight:800; color:#f8fafc; font-size:16px; letter-spacing:0.8px;'>
                SECTOR DE ESTANTERÍAS: {st.session_state.current_store.upper()}
            </span>
            <span style='font-size:12px; color:#818cf8; font-weight:700;'>3 RANURAS ACTIVAS</span>
        </div>
    """, unsafe_allow_html=True)

    cols = st.columns(len(current_items))

    for idx, item in enumerate(current_items):
        with cols[idx]:
            # Estado del stock
            st_val = int(item["stock"])
            if st_val == 0:
                status = "empty"
            elif st_val <= 35:
                status = "medium"
            else:
                status = "full"

            box_svg = get_box_svg(status, st.session_state.current_store.lower())

            st.markdown(f"""
            <div class='box-slot'>
                <div style='font-size:11px; font-weight:800; color:#818cf8;'>ID #{item['id']}</div>
                <div style='height:85px; display:flex; align-items:center; justify-content:center;'>
                    {box_svg}
                </div>
                <div style='font-weight:800; font-size:13px; color:#f8fafc;'>{item['nombre']}</div>
                <div style='font-size:12px; color:#94a3b8;'>
                    NIVEL: <strong style='color:{"#f56565" if st_val < 20 else "#48bb78"};'>{st_val}%</strong>
                </div>
            </div>
            """, unsafe_allow_html=True)

            # Botón interactivo de Reposición
            if st.button(f"REPONER (+50%)", key=f"btn_repon_{item['id']}"):
                item["stock"] = min(100.0, item["stock"] + 50.0)
                st.session_state.score += 25
                st.rerun()

    st.markdown("</div>", unsafe_allow_html=True)

    # Rerun automático del bucle de juego cada 0.5 segundos
    time.sleep(0.5)
    st.rerun()
