import streamlit as st
import time

# Intentar cargar streamlit-option-menu para navegación moderna
try:
    from streamlit_option_menu import option_menu
    HAS_OPTION_MENU = True
except ImportError:
    HAS_OPTION_MENU = False

# ---------------------------------------------------------
# CONFIGURACIÓN DE PÁGINA (WIDE + MATE DARK HUD)
# ---------------------------------------------------------
st.set_page_config(
    page_title="AutoStock HUD - Almacén & Repuestos",
    page_icon="🛠️",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# ---------------------------------------------------------
# GENERADORES SVG: CAJAS 3D / CARTOON REALISTAS
# ---------------------------------------------------------
def get_box_svg(status="full"):
    """Genera cajas en perspectiva 3D estilo cartoon en SVG puro con colores mate."""
    if status == "full":
        # Caja Cerrada Verde Mate
        return """
        <svg width="110" height="110" viewBox="0 0 100 100" style="filter: drop-shadow(0px 8px 12px rgba(0,0,0,0.4));">
            <!-- Top Flap -->
            <polygon points="50,15 85,32 50,48 15,32" fill="#38a169"/>
            <polygon points="50,15 85,32 80,30 50,17" fill="#48bb78"/>
            <!-- Left Side -->
            <polygon points="15,32 50,48 50,85 15,68" fill="#22543d"/>
            <!-- Right Side -->
            <polygon points="50,48 85,32 85,68 50,85" fill="#2f855a"/>
            <!-- Sealing Tape -->
            <polygon points="45,18 55,23 55,83 45,78" fill="#cbd5e0" opacity="0.85"/>
            <!-- Badge icon -->
            <rect x="58" y="52" width="20" height="14" rx="3" fill="#1a202c" opacity="0.6"/>
            <circle cx="68" cy="59" r="4" fill="#48bb78"/>
        </svg>
        """
    elif status == "medium":
        # Caja Semi-abierta Café/Ámbar Mate
        return """
        <svg width="110" height="110" viewBox="0 0 100 100" style="filter: drop-shadow(0px 8px 12px rgba(0,0,0,0.4));">
            <!-- Top Interior Dark -->
            <polygon points="50,22 85,35 50,48 15,35" fill="#2d1a04"/>
            <!-- Flaps Open -->
            <polygon points="15,35 35,20 50,28 30,41" fill="#dd6b20"/>
            <polygon points="85,35 65,20 50,28 70,41" fill="#ed8936"/>
            <!-- Left Side -->
            <polygon points="15,35 50,48 50,85 15,68" fill="#744210"/>
            <!-- Right Side -->
            <polygon points="50,48 85,35 85,68 50,85" fill="#975a16"/>
            <!-- Label -->
            <rect x="58" y="55" width="20" height="14" rx="3" fill="#1a202c" opacity="0.6"/>
            <circle cx="68" cy="62" r="4" fill="#ed8936"/>
        </svg>
        """
    else:
        # Caja Vacía Roja Matte con Hueco Oscuro
        return """
        <svg width="110" height="110" viewBox="0 0 100 100" style="filter: drop-shadow(0px 0px 18px rgba(245, 101, 101, 0.4));">
            <!-- Empty Interior Void -->
            <polygon points="50,20 85,35 50,50 15,35" fill="#0f0505"/>
            <!-- Open Flaps Red -->
            <polygon points="15,35 50,50 15,40" fill="#9b2c2c"/>
            <polygon points="85,35 50,50 85,40" fill="#c53030"/>
            <!-- Outer Left -->
            <polygon points="15,35 50,50 50,85 15,68" fill="#742a2a"/>
            <!-- Outer Right -->
            <polygon points="50,50 85,35 85,68 50,85" fill="#9b2c2c"/>
            <!-- Warning sign inside -->
            <text x="50" y="42" font-size="16" text-anchor="middle" fill="#feb2b2" font-weight="900">⚠️</text>
        </svg>
        """

# ---------------------------------------------------------
# ESTILOS CSS CUSTOM (ESTANTERÍAS + ANIMACIONES BURBUJA)
# ---------------------------------------------------------
st.markdown("""
<style>
    /* Estilo Base Mate Oscuro Tipo Taller Gaming HUD */
    .stApp {
        background-color: #0f1217;
        color: #e2e8f0;
        font-family: 'Inter', system-ui, -apple-system, sans-serif;
    }

    #MainMenu, header, footer {visibility: hidden;}

    /* Botones Interactivos con Animación Burbuja Fluid / Bounce */
    div.stButton > button {
        background: linear-gradient(135deg, #1f2633 0%, #171c26 100%);
        color: #f1f5f9;
        border: 1px solid #333d4f;
        border-radius: 14px;
        padding: 10px 18px;
        font-weight: 700;
        font-size: 14px;
        transition: all 0.25s cubic-bezier(0.175, 0.885, 0.32, 1.275);
        box-shadow: 0 4px 12px rgba(0,0,0,0.35);
        width: 100%;
        cursor: pointer;
    }

    div.stButton > button:hover {
        transform: translateY(-4px) scale(1.03);
        background: linear-gradient(135deg, #2b3547 0%, #202736 100%);
        border-color: #6366f1;
        color: #ffffff;
        box-shadow: 0 8px 22px rgba(99, 102, 241, 0.3);
    }

    div.stButton > button:active {
        transform: translateY(1px) scale(0.96);
    }

    /* ESTANTERÍA INDUSTRIAL (Shelf Container) */
    .shelf-container {
        background: linear-gradient(180deg, rgba(23, 28, 38, 0.8) 0%, rgba(15, 18, 23, 0.95) 100%);
        border: 1px solid #232a38;
        border-radius: 18px;
        padding: 20px 22px 5px 22px;
        margin-bottom: 28px;
        box-shadow: 0 10px 30px rgba(0,0,0,0.5);
    }

    .shelf-header {
        display: flex;
        justify-content: space-between;
        align-items: center;
        border-bottom: 2px solid #2a3445;
        padding-bottom: 10px;
        margin-bottom: 18px;
    }

    .shelf-title {
        font-size: 18px;
        font-weight: 800;
        color: #f8fafc;
        letter-spacing: 0.5px;
    }

    /* Tablado / Madera o Metal de la Estantería */
    .shelf-plank {
        background: linear-gradient(180deg, #333c4d 0%, #1c222e 100%);
        height: 14px;
        border-radius: 4px;
        border-bottom: 3px solid #10141b;
        box-shadow: 0 6px 12px rgba(0,0,0,0.6);
        margin-top: 10px;
        margin-bottom: 15px;
    }

    /* Ranura de Caja en la Estantería */
    .box-slot {
        background: rgba(255,255,255,0.02);
        border: 1px dashed #2a3445;
        border-radius: 16px;
        padding: 15px;
        text-align: center;
        transition: all 0.3s ease;
        min-height: 250px;
        display: flex;
        flex-direction: column;
        justify-content: space-between;
        align-items: center;
    }

    .box-slot:hover {
        border-color: #4f46e5;
        background: rgba(99, 102, 241, 0.03);
    }

    /* Alerta Parpadeante de Caja Vacía */
    .alert-empty-badge {
        background: #9b2c2c;
        color: #fff5f5;
        padding: 6px 12px;
        border-radius: 20px;
        font-size: 11px;
        font-weight: 900;
        letter-spacing: 0.8px;
        text-transform: uppercase;
        animation: pulseAlert 1.5s infinite;
        margin-top: 6px;
        border: 1px solid #f56565;
    }

    @keyframes pulseAlert {
        0% { transform: scale(1); box-shadow: 0 0 0 0 rgba(245, 101, 101, 0.7); }
        70% { transform: scale(1.05); box-shadow: 0 0 0 10px rgba(245, 101, 101, 0); }
        100% { transform: scale(1); box-shadow: 0 0 0 0 rgba(245, 101, 101, 0); }
    }

    /* Tarjetas de Métricas Superior */
    .hud-card {
        background: #161b24;
        border-radius: 14px;
        padding: 16px;
        border: 1px solid #232b3a;
        text-align: center;
    }

    .hud-card-val {
        font-size: 28px;
        font-weight: 900;
        margin-top: 4px;
    }
</style>
""", unsafe_allow_html=True)

# ---------------------------------------------------------
# ESTADO DE SESIÓN (DATOS DEL ALMACÉN)
# ---------------------------------------------------------
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if "inventario" not in st.session_state:
    st.session_state.inventario = [
        # Estante 1
        {"id": 101, "nombre": "Filtro Aceite Sintético", "tienda": "AutoPlanet", "estante": "Estantería A - Motor", "stock": 18, "max": 20, "caso_tomado": False},
        {"id": 102, "nombre": "Bujías Iridium IX", "tienda": "Sodimac", "estante": "Estantería A - Motor", "stock": 5, "max": 15, "caso_tomado": False},
        {"id": 103, "nombre": "Correa Distribución Continental", "tienda": "AutoPlanet", "estante": "Estantería A - Motor", "stock": 0, "max": 10, "caso_tomado": False},
        
        # Estante 2
        {"id": 201, "nombre": "Pastillas Freno Cerámicas", "tienda": "Sodimac", "estante": "Estantería B - Frenos & Suspensión", "stock": 0, "max": 12, "caso_tomado": False},
        {"id": 202, "nombre": "Líquido Frenos DOT4 1L", "tienda": "AutoPlanet", "estante": "Estantería B - Frenos & Suspensión", "stock": 12, "max": 15, "caso_tomado": False},
        {"id": 203, "nombre": "Amortiguadores Delanteros Gas", "tienda": "Sodimac", "estante": "Estantería B - Frenos & Suspensión", "stock": 4, "max": 8, "caso_tomado": False},

        # Estante 3
        {"id": 301, "nombre": "Batería 12V 70Ah Bosch", "tienda": "AutoPlanet", "estante": "Estantería C - Eléctrico", "stock": 0, "max": 6, "caso_tomado": False},
        {"id": 302, "nombre": "Alternador 120A Reacondicionado", "tienda": "Sodimac", "estante": "Estantería C - Eléctrico", "stock": 8, "max": 10, "caso_tomado": False},
        {"id": 303, "nombre": "Kit Ampolletas LED H7", "tienda": "AutoPlanet", "estante": "Estantería C - Eléctrico", "stock": 14, "max": 15, "caso_tomado": False},
    ]

if "chat_messages" not in st.session_state:
    st.session_state.chat_messages = [
        {"emisor": "Bosch Repuestos", "texto": "Hola, las baterías 12V ingresan a bodega a las 15:00 hrs."},
        {"emisor": "Tú (Supervisor)", "texto": "Excelente, enviamos la orden en cuanto el sistema registre la falta de stock."}
    ]

# ---------------------------------------------------------
# VISTA 1: LOGIN TIPO HUD MECÁNICO
# ---------------------------------------------------------
if not st.session_state.logged_in:
    st.markdown("<br><br>", unsafe_allow_html=True)
    c_left, c_center, c_right = st.columns([1, 1.8, 1])
    
    with c_center:
        st.markdown("""
        <div style='background: #141822; padding: 35px; border-radius: 22px; border: 1px solid #283245; text-align: center; box-shadow: 0 15px 35px rgba(0,0,0,0.6);'>
            <h1 style='color:#ffffff; margin:0; font-size:28px;'>🛠️ AUTOSTOCK HUD</h1>
            <p style='color:#818cf8; font-weight:600; margin-top:5px;'>Control Taller & Inventario de Repuestos</p>
            <hr style='border-color:#263042; margin: 20px 0;'>
        </div>
        """, unsafe_allow_html=True)
        
        user = st.text_input("Usuario Supervisor", "supervisor_taller")
        pwd = st.text_input("Contraseña / PIN", type="password", value="1234")
        
        if st.button("INICIAR SESIÓN Y ABRIR TALLER ⚡"):
            with st.spinner("Cargando entorno 3D de estanterías..."):
                time.sleep(0.4)
                st.session_state.logged_in = True
                st.rerun()

# ---------------------------------------------------------
# VISTA 2: APLICACIÓN PRINCIPAL (ESTANTERÍAS & CHAT)
# ---------------------------------------------------------
else:
    # Top Bar / Navegación
    col_t1, col_t2 = st.columns([4, 1])
    with col_t1:
        st.markdown("<h2 style='margin:0; color:#fff;'>📦 Taller AutoStock - Visualizador de Estanterías</h2>", unsafe_allow_html=True)
    with col_t2:
        if st.button("🚪 Cerrar Sesión"):
            st.session_state.logged_in = False
            st.rerun()

    st.markdown("<br>", unsafe_allow_html=True)

    # Navegación Limpia con Option Menu
    if HAS_OPTION_MENU:
        selected_tab = option_menu(
            menu_title=None,
            options=["🏬 Estanterías de Almacén", "💬 Chat Proveedores", "📋 Pedidos & Órdenes"],
            icons=["box-seam", "chat-dots", "receipt-cutoff"],
            default_index=0,
            orientation="horizontal",
            styles={
                "container": {"padding": "0!important", "background-color": "#161b24", "border-radius": "14px"},
                "icon": {"color": "#818cf8", "font-size": "16px"},
                "nav-link": {"font-size": "14px", "text-align": "center", "margin": "0px", "color": "#94a3b8", "font-weight": "600"},
                "nav-link-selected": {"background-color": "#312e81", "color": "#ffffff", "border-radius": "12px"},
            }
        )
    else:
        # Fallback si no está instalado option-menu
        selected_tab_raw = st.tabs(["🏬 Estanterías de Almacén", "💬 Chat Proveedores", "📋 Pedidos & Órdenes"])
        selected_tab = "🏬 Estanterías de Almacén"

    # RESUMEN RÁPIDO DE INDICADORES (HUD MATE)
    cajas_llenas = sum(1 for x in st.session_state.inventario if x["stock"] > 8)
    cajas_medias = sum(1 for x in st.session_state.inventario if 0 < x["stock"] <= 8)
    cajas_vacias = sum(1 for x in st.session_state.inventario if x["stock"] == 0)

    st.markdown("<br>", unsafe_allow_html=True)
    m1, m2, m3 = st.columns(3)
    with m1:
        st.markdown(f"""
        <div class='hud-card' style='border-top: 4px solid #48bb78;'>
            <span style='color:#48bb78; font-weight:800; font-size:13px;'>🟩 CAJAS LLENAS</span>
            <div class='hud-card-val' style='color:#48bb78;'>{cajas_llenas}</div>
        </div>
        """, unsafe_allow_html=True)

    with m2:
        st.markdown(f"""
        <div class='hud-card' style='border-top: 4px solid #ed8936;'>
            <span style='color:#ed8936; font-weight:800; font-size:13px;'>🟫 CAJAS MEDIAS</span>
            <div class='hud-card-val' style='color:#ed8936;'>{cajas_medias}</div>
        </div>
        """, unsafe_allow_html=True)

    with m3:
        st.markdown(f"""
        <div class='hud-card' style='border-top: 4px solid #f56565;'>
            <span style='color:#f56565; font-weight:800; font-size:13px;'>🟥 CAJAS VACÍAS (ALERTAS)</span>
            <div class='hud-card-val' style='color:#f56565;'>{cajas_vacias}</div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # ---------------------------------------------------------
    # PESTAÑA 1: VISUALIZADOR DE ESTANTERÍAS HACIA ABAJO
    # ---------------------------------------------------------
    if "Estanterías" in selected_tab:
        # Agrupar items por Estante
        estantes = sorted(list(set(x["estante"] for x in st.session_state.inventario)))

        for estante_nombre in estantes:
            items_estante = [x for x in st.session_state.inventario if x["estante"] == estante_nombre]
            
            # Dibujar Contenedor de la Estantería
            st.markdown(f"""
            <div class='shelf-container'>
                <div class='shelf-header'>
                    <span class='shelf-title'>🧱 {estante_nombre}</span>
                    <span style='font-size:12px; color:#94a3b8; background:#1e2636; padding:4px 10px; border-radius:8px;'>
                        {len(items_estante)} Cajas en Ranura
                    </span>
                </div>
            """, unsafe_allow_html=True)

            # Columnas de Cajas en la Estantería
            cols = st.columns(len(items_estante))

            for idx, item in enumerate(items_estante):
                with cols[idx]:
                    # Determinar Estado
                    if item["stock"] == 0:
                        status = "empty"
                    elif item["stock"] <= 8:
                        status = "medium"
                    else:
                        status = "full"

                    # Render del SVG de la Caja
                    box_html = get_box_svg(status)

                    st.markdown(f"""
                    <div class='box-slot'>
                        <div style='font-size:11px; font-weight:700; color:#818cf8; text-transform:uppercase;'>{item['tienda']}</div>
                        <div style='height: 100px; display:flex; align-items:center; justify-content:center;'>
                            {box_html}
                        </div>
                        <div style='font-weight:700; font-size:13px; color:#f1f5f9; margin-top:6px;'>{item['nombre']}</div>
                        <div style='font-size:12px; color:#94a3b8;'>Stock: <strong style='color:#fff;'>{item['stock']}/{item['max']}</strong></div>
                        { "<div class='alert-empty-badge'>🚨 URGENTE: SIN STOCK</div>" if status == 'empty' else "" }
                    </div>
                    """, unsafe_allow_html=True)

                    # Acciones Interactivas de Supervisor
                    if status == "empty":
                        if not item["caso_tomado"]:
                            if st.button("🙋‍♂️ Tomar Caso", key=f"tomar_{item['id']}"):
                                item["caso_tomado"] = True
                                st.toast(f"Has tomado el caso de: {item['nombre']}", icon="🚨")
                                st.rerun()
                            if st.button("❌ Aceptar / Ignorar", key=f"ignorar_{item['id']}"):
                                st.toast("Caso omitido sin cambios de reabastecimiento.", icon="ℹ️")
                        else:
                            st.markdown("<p style='text-align:center; color:#48bb78; font-size:12px; font-weight:700; margin-top:5px;'>🟢 Caso Asignado a Ti</p>", unsafe_allow_html=True)
                            if st.button("📦 Reabastecer Caja", key=f"reab_{item['id']}"):
                                item["stock"] = item["max"]
                                item["caso_tomado"] = False
                                st.success("¡Caja reabastecida!")
                                st.rerun()

            # Estante Físico (Plank) al fondo
            st.markdown("<div class='shelf-plank'></div></div>", unsafe_allow_html=True)

    # ---------------------------------------------------------
    # PESTAÑA 2: CHAT CON PROVEEDORES
    # ---------------------------------------------------------
    elif "Chat" in selected_tab:
        st.markdown("### 💬 Chat Directo con Proveedores (Sodimac / AutoPlanet / Bosch)")
        
        chat_box = st.container()
        with chat_box:
            for m in st.session_state.chat_messages:
                if "Tú" in m["emisor"]:
                    st.markdown(f"""
                    <div style='background:#1e293b; padding:12px 18px; border-radius:14px 14px 0px 14px; margin:8px 0 8px auto; max-width:70%; text-align:right; border-right:3px solid #6366f1;'>
                        <strong style='color:#818cf8;'>{m['emisor']}</strong>
                        <p style='margin:4px 0 0 0; color:#f8fafc;'>{m['texto']}</p>
                    </div>
                    """, unsafe_allow_html=True)
                else:
                    st.markdown(f"""
                    <div style='background:#161f2e; padding:12px 18px; border-radius:14px 14px 14px 0px; margin:8px 0; max-width:70%; border-left:3px solid #10b981;'>
                        <strong style='color:#34d399;'>{m['emisor']}</strong>
                        <p style='margin:4px 0 0 0; color:#f8fafc;'>{m['texto']}</p>
                    </div>
                    """, unsafe_allow_html=True)

        st.markdown("<br>", unsafe_allow_html=True)
        txt = st.text_input("Escribe tu consulta o pedido al proveedor...", key="input_msg")
        if st.button("Enviar Mensaje 🚀"):
            if txt:
                st.session_state.chat_messages.append({"emisor": "Tú (Supervisor)", "texto": txt})
                st.rerun()

    # ---------------------------------------------------------
    # PESTAÑA 3: PEDIDOS Y ÓRDENAS
    # ---------------------------------------------------------
    else:
        st.markdown("### 📋 Pedidos de Clientes & Compras")
        col_a, col_b = st.columns(2)
        with col_a:
            st.subheader("🛒 Pedidos Recientes de Clientes")
            st.info("• Pedido #8821 - 2x Filtro Aceite (AutoPlanet) - **Completado**")
            st.warning("• Pedido #8822 - 1x Batería 12V (Bosch) - **Esperando Stock**")
        with col_b:
            st.subheader("🚚 Pedidos a Proveedores")
            st.success("• Orden Prov #402 - 10x Correa Distribución (En Camino)")
