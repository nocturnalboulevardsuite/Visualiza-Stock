import streamlit as st

# Configuración de página optimizada para vista móvil y escritorio
st.set_page_config(
    page_title="AutoStock Pro - Taller & Repuestos", 
    layout="wide",
    initial_sidebar_state="collapsed"
)

# --- CSS PERSONALIZADO (Estética Mate + Animaciones) ---
st.markdown("""
<style>
    /* Estilo General Mate */
    .stApp {
        background-color: #121418;
        color: #e2e8f0;
        font-family: 'Segoe UI', Roboto, sans-serif;
    }

    /* Ocultar elementos nativos de Streamlit para video */
    #MainMenu, header, footer {visibility: hidden;}

    /* Botones Interactivos Estilo Burbuja */
    div.stButton > button {
        background: #252a34;
        color: #ffffff;
        border: 1px solid #3a4150;
        border-radius: 14px;
        padding: 12px 24px;
        font-weight: 700;
        font-size: 15px;
        letter-spacing: 0.5px;
        transition: all 0.3s cubic-bezier(0.175, 0.885, 0.32, 1.275);
        box-shadow: 0 4px 10px rgba(0,0,0,0.3);
        width: 100%;
    }

    div.stButton > button:hover {
        transform: scale(1.05) translateY(-3px);
        background: #323946;
        border-color: #6366f1;
        box-shadow: 0 8px 20px rgba(99, 102, 241, 0.25);
    }

    div.stButton > button:active {
        transform: scale(0.95);
    }

    /* Contadores y Métricas Superiores */
    .metric-card {
        background: #1c2029;
        border-radius: 16px;
        padding: 15px;
        text-align: center;
        border: 1px solid #2d3444;
        box-shadow: 0 4px 12px rgba(0,0,0,0.2);
    }
    .metric-count {
        font-size: 28px;
        font-weight: bold;
        margin-top: 5px;
    }

    /* Tarjetas de Cajas de Repuestos */
    .stock-box {
        border-radius: 16px;
        padding: 20px;
        margin-top: 10px;
        margin-bottom: 15px;
        color: #ffffff;
        box-shadow: 0 6px 15px rgba(0,0,0,0.3);
        transition: transform 0.2s ease, box-shadow 0.2s ease;
    }
    .stock-box:hover {
        transform: translateY(-4px);
    }

    /* Estilos por Estado */
    .box-full {
        background: linear-gradient(145deg, #235432, #1c4328);
        border-left: 8px solid #48bb78;
    }
    .box-medium {
        background: linear-gradient(145deg, #6e4822, #58391b);
        border-left: 8px solid #ed8936;
    }
    .box-empty {
        background: linear-gradient(145deg, #6b1d1d, #521616);
        border-left: 8px solid #f56565;
        animation: pulse-border 2s infinite;
    }

    /* Animación de Pulso para Repuestos Sin Stock */
    @keyframes pulse-border {
        0% { box-shadow: 0 0 0 0 rgba(245, 101, 101, 0.5); }
        70% { box-shadow: 0 0 0 12px rgba(245, 101, 101, 0); }
        100% { box-shadow: 0 0 0 0 rgba(245, 101, 101, 0); }
    }

    .badge-urgent {
        background-color: #e53e3e;
        color: white;
        padding: 6px 12px;
        border-radius: 20px;
        font-size: 12px;
        font-weight: 800;
        text-transform: uppercase;
        display: inline-block;
        margin-top: 8px;
        letter-spacing: 1px;
    }

    /* Chat de Proveedores */
    .chat-bubble-user {
        background: #2b3245;
        padding: 10px 15px;
        border-radius: 12px 12px 0px 12px;
        margin: 5px 0;
        text-align: right;
    }
    .chat-bubble-vendor {
        background: #1e293b;
        padding: 10px 15px;
        border-radius: 12px 12px 12px 0px;
        margin: 5px 0;
        border-left: 3px solid #6366f1;
    }
</style>
""", unsafe_allow_html=True)

# --- ESTADO DE SESIÓN (LOGIN & DATOS) ---
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if "repuestos" not in st.session_state:
    st.session_state.repuestos = [
        {"id": 1, "nombre": "Filtro de Aceite Alto Rendimiento", "tienda": "AutoPlanet", "stock": 15, "max": 20, "estado": "full"},
        {"id": 2, "nombre": "Pastillas de Freno Cerámicas", "tienda": "Sodimac", "stock": 4, "max": 15, "estado": "medium"},
        {"id": 3, "nombre": "Amortiguador Delantero Gas", "tienda": "AutoPlanet", "stock": 0, "max": 10, "estado": "empty", "caso_tomado": False},
        {"id": 4, "nombre": "Kit Distribución / Correa", "tienda": "Sodimac", "stock": 8, "max": 12, "estado": "full"},
        {"id": 5, "nombre": "Batería 12V 70Ah", "tienda": "AutoPlanet", "stock": 0, "max": 8, "estado": "empty", "caso_tomado": False},
    ]

if "chat_messages" not in st.session_state:
    st.session_state.chat_messages = [
        {"emisor": "Proveedor Bosch", "texto": "Hola, confirmamos el envío de las 10 baterías para mañana."},
        {"emisor": "Tú", "texto": "Perfecto, quedo atento al número de seguimiento."}
    ]

# --- VISTA 1: LOGIN INTERACTIVO ---
if not st.session_state.logged_in:
    st.markdown("<h2 style='text-align: center; color: #f8fafc;'>🛠️ AUTOSTOCK HUD LOGIN</h2>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: center; color: #94a3b8;'>Plataforma de Supervisión de Repuestos</p>", unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.markdown("<br>", unsafe_allow_html=True)
        usuario = st.text_input("Usuario / Supervisor", "admin_taller")
        password = st.text_input("Contraseña", type="password", value="••••••••")
        
        if st.button("INGRESAR AL DASHBOARD ⚡"):
            st.session_state.logged_in = True
            st.rerun()

# --- VISTA 2: INTERFAZ PRINCIPAL ---
else:
    # Encabezado
    col_title, col_logout = st.columns([4, 1])
    with col_title:
        st.markdown("<h2 style='margin:0; color:#ffffff;'>📦 Control de Stock & Repuestos</h2>", unsafe_allow_html=True)
    with col_logout:
        if st.button("Cerrar Sesión"):
            st.session_state.logged_in = False
            st.rerun()

    st.markdown("---")

    # Contadores Superiores (Filtros e Indicadores)
    cant_full = sum(1 for r in st.session_state.repuestos if r["stock"] > 8)
    cant_medium = sum(1 for r in st.session_state.repuestos if 0 < r["stock"] <= 8)
    cant_empty = sum(1 for r in st.session_state.repuestos if r["stock"] == 0)

    col_f, col_m, col_e = st.columns(3)
    with col_f:
        st.markdown(f"""
            <div class='metric-card' style='border-top: 4px solid #48bb78;'>
                <span style='color:#48bb78; font-weight:bold;'>🟩 CAJAS LLENAS</span>
                <div class='metric-count' style='color:#48bb78;'>{cant_full}</div>
            </div>
        """, unsafe_allow_html=True)

    with col_m:
        st.markdown(f"""
            <div class='metric-card' style='border-top: 4px solid #ed8936;'>
                <span style='color:#ed8936; font-weight:bold;'>🟫 CAJAS MEDIAS</span>
                <div class='metric-count' style='color:#ed8936;'>{cant_medium}</div>
            </div>
        """, unsafe_allow_html=True)

    with col_e:
        st.markdown(f"""
            <div class='metric-card' style='border-top: 4px solid #f56565;'>
                <span style='color:#f56565; font-weight:bold;'>🟥 CAJAS VACÍAS</span>
                <div class='metric-count' style='color:#f56565;'>{cant_empty}</div>
            </div>
        """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # Pestañas Principales
    tab_stock, tab_proveedores, tab_pedidos = st.tabs(["📦 Repuestos en Inventario", "💬 Chat Proveedores", "📋 Gestión de Pedidos"])

    # TAB 1: STOCK Y ACCIONES DE SUPERVISOR
    with tab_stock:
        st.markdown("### Estado del Inventario en Tiempo Real")
        
        for item in st.session_state.repuestos:
            # Clasificación de clase CSS según stock
            if item["stock"] == 0:
                css_class = "box-empty"
                status_text = "📭 CAJA VACÍA"
            elif item["stock"] <= 8:
                css_class = "box-medium"
                status_text = "📦 CAJA MEDIA"
            else:
                css_class = "box-full"
                status_text = "📦 CAJA LLENA"

            # Render de la tarjeta visual
            c1, c2 = st.columns([3, 1.2])
            with c1:
                st.markdown(f"""
                    <div class='stock-box {css_class}'>
                        <div style='display:flex; justify-content:space-between; align-items:center;'>
                            <h4 style='margin:0;'>{item['nombre']}</h4>
                            <span style='font-size:12px; background:rgba(0,0,0,0.4); padding:4px 8px; border-radius:6px;'>{item['tienda']}</span>
                        </div>
                        <p style='margin: 8px 0 0 0;'>Estado: <strong>{status_text}</strong> ({item['stock']}/{item['max']} unidades)</p>
                        { "<span class='badge-urgent'>⚠️ URGENTE SIN STOCK</span>" if item['stock'] == 0 else "" }
                    </div>
                """, unsafe_allow_html=True)
            
            with c2:
                st.markdown("<br>", unsafe_allow_html=True)
                if item["stock"] == 0:
                    if not item.get("caso_tomado", False):
                        if st.button(f"Tomar Caso #{item['id']}", key=f"btn_tomar_{item['id']}"):
                            item["caso_tomado"] = True
                            st.success("¡Caso asignado!")
                            st.rerun()
                    else:
                        st.info("🟢 Caso tomado por supervisor")
                        if st.button(f"Aceptar / Solicitar #{item['id']}", key=f"btn_ok_{item['id']}"):
                            item["stock"] = item["max"]
                            item["caso_tomado"] = False
                            st.success("Pedido realizado y stock reabastecido.")
                            st.rerun()
                else:
                    st.button(f"Ver Detalle #{item['id']}", key=f"btn_det_{item['id']}")

    # TAB 2: CHAT CON PROVEEDORES
    with tab_proveedores:
        st.markdown("### Chat Directo con Proveedores (Bosch / Sodimac / AutoPlanet)")
        
        chat_container = st.container()
        with chat_container:
            for msg in st.session_state.chat_messages:
                if msg["emisor"] == "Tú":
                    st.markdown(f"<div class='chat-bubble-user'><strong>{msg['emisor']}:</strong> {msg['texto']}</div>", unsafe_allow_html=True)
                else:
                    st.markdown(f"<div class='chat-bubble-vendor'><strong>{msg['emisor']}:</strong> {msg['texto']}</div>", unsafe_allow_html=True)

        st.markdown("<br>", unsafe_allow_html=True)
        nuevo_mensaje = st.text_input("Escribe un mensaje al proveedor...", key="input_chat")
        if st.button("Enviar Mensaje 🚀"):
            if nuevo_mensaje:
                st.session_state.chat_messages.append({"emisor": "Tú", "texto": nuevo_mensaje})
                st.rerun()

    # TAB 3: PEDIDOS Y TRANSACCIONES
    with tab_pedidos:
        st.markdown("### Movimientos y Órdenes de Compras")
        col_p1, col_p2 = st.columns(2)
        with col_p1:
            st.subheader("🛒 Pedidos de Clientes")
            st.write("• Orden #1042 - 2x Filtros de Aceite (Completado)")
            st.write("• Orden #1043 - 1x Batería 12V (Pendiente de Stock)")
        with col_p2:
            st.subheader("🚚 Compras a Proveedores")
            st.write("• Pedido Prov-889 - 10x Amortiguadores (En camino)")
            st.write("• Pedido Prov-890 - 20x Pastillas Freno (Procesando)")
