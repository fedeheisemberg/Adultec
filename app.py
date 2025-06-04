import streamlit as st
import time
from PIL import Image
import base64
import random

# Configuración de la página
st.set_page_config(
    page_title="AdulTec - Aprendizaje digital para adultos mayores",
    page_icon="👵👴",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Función para cambiar entre tema claro y oscuro
def toggle_theme():
    current_theme = st.session_state.get("theme", "light")
    if current_theme == "light":
        st.session_state.theme = "dark"
    else:
        st.session_state.theme = "light"
    st.experimental_rerun()

# Función para mostrar mensaje de bienvenida personalizado
def mostrar_bienvenida(nombre):
    if nombre:
        return f"¡Bienvenido/a, {nombre}! 😊"
    return "¡Bienvenido/a a AdulTec! 😊"

# Función para crear tarjetas de cursos
def crear_tarjeta_curso(titulo, descripcion, imagen, progreso=0, es_premium=False):
    with st.container():
        col1, col2 = st.columns([1, 3])
        with col1:
            st.image(imagen, width=150)
        with col2:
            if es_premium:
                st.markdown(f"### {titulo} 🌟")
                st.markdown("*Curso Premium*")
            else:
                st.markdown(f"### {titulo}")
            st.write(descripcion)
            
            # Barra de progreso
            if progreso > 0:
                st.progress(progreso)
                st.write(f"Progreso: {int(progreso*100)}% completado")
            
            ver_curso = st.button("Entrar al curso", key=f"btn_{titulo}")
            if ver_curso:
                st.session_state.pagina = "curso"
                st.session_state.curso_actual = titulo
                st.experimental_rerun()

# Aplicar CSS personalizado según el tema
def aplicar_css():
    tema = st.session_state.get("theme", "light")
    
    if tema == "dark":
        background_color = "#0E1117"
        text_color = "#FAFAFA"
        secondary_bg = "#262730"
        accent_color = "#1F77B4"
        button_color = "#1F77B4"
        card_bg = "#1E1E1E"
    else:
        background_color = "#FFFFFF"
        text_color = "#31333F"
        secondary_bg = "#F0F2F6"
        accent_color = "#0A84FF"
        button_color = "#0A84FF"
        card_bg = "#FFFFFF"

    
    css = f"""
    <style>
        .main {{
            background-color: {background_color};
            color: {text_color};
        }}
        .stButton button {{
            background-color: {button_color};
            color: {'white' if tema == 'light' else 'white'};
            border-radius: 20px;
            padding: 12px 24px;
            font-size: 18px;
            font-weight: bold;
            width: 100%;
            border: none;
        }}
        .stProgress > div > div > div {{
            background-color: {accent_color};
        }}
        .curso-tarjeta {{
            background-color: {card_bg};
            padding: 20px;
            border-radius: 10px;
            margin-bottom: 20px;
            box-shadow: 0 4px 8px rgba(0,0,0,0.1);
        }}
        .container {{
            background-color: {secondary_bg};
            padding: 20px;
            border-radius: 10px;
            margin-bottom: 15px;
        }}
        h1, h2, h3 {{
            color: {text_color};
        }}
        .footer {{
            text-align: center;
            margin-top: 30px;
            padding: 10px;
            font-size: 14px;
            color: gray;
        }}
        .stRadio label {{
            font-size: 20px;
        }}
        .quiz-option {{
            background-color: {secondary_bg};
            padding: 15px;
            border-radius: 10px;
            margin: 10px 0;
            cursor: pointer;
            transition: all 0.3s;
        }}
        .quiz-option:hover {{
            background-color: {accent_color};
            color: white;
        }}
        .stTabs [data-baseweb="tab-list"] {{
            font-size: 20px;
        }}
        .faq-question {{
            background-color: {secondary_bg};
            padding: 15px;
            border-radius: 8px;
            margin-bottom: 10px;
            cursor: pointer;
        }}
        .feature-card {{
            background-color: {secondary_bg};
            padding: 15px;
            border-radius: 10px;
            text-align: center;
            height: 100%;
        }}
        .icon-large {{
            font-size: 48px;
        }}
        .ayuda-btn {{
            position: fixed;
            bottom: 20px;
            right: 20px;
            width: 60px;
            height: 60px;
            background-color: #25D366;
            color: white;
            border-radius: 50%;
            display: flex;
            justify-content: center;
            align-items: center;
            font-size: 30px;
            box-shadow: 0 4px 8px rgba(0,0,0,0.2);
            z-index: 9999;
        }}
    </style>
    """
    st.markdown(css, unsafe_allow_html=True)
    
    # Botón flotante de WhatsApp
    whatsapp_html = """
    <a href="https://wa.me/5491100000000?text=Hola,%20necesito%20ayuda%20con%20AdulTec" target="_blank">
        <div class="ayuda-btn">💬</div>
    </a>
    """
    st.markdown(whatsapp_html, unsafe_allow_html=True)

# Inicializar variables de sesión
if "pagina" not in st.session_state:
    st.session_state.pagina = "inicio"
if "theme" not in st.session_state:
    st.session_state.theme = "light"
if "usuario_logueado" not in st.session_state:
    st.session_state.usuario_logueado = False
if "nombre_usuario" not in st.session_state:
    st.session_state.nombre_usuario = ""
if "respuestas_correctas" not in st.session_state:
    st.session_state.respuestas_correctas = 0
if "pregunta_actual" not in st.session_state:
    st.session_state.pregunta_actual = 0
if "modulo_actual" not in st.session_state:
    st.session_state.modulo_actual = 1
if "mostrar_resultado" not in st.session_state:
    st.session_state.mostrar_resultado = False

# Aplicar CSS según el tema
aplicar_css()

# Contenido del curso básico de Internet
curso_internet = {
    "titulo": "¿Qué es Internet y cómo usarlo de forma segura?",
    "modulos": [
        {
            "titulo": "Módulo 1: Fundamentos de Internet",
            "contenido": """
            # Módulo 1: Fundamentos de Internet
            
            ## ¿Qué es Internet?
            
            Internet es una red mundial de computadoras conectadas entre sí que permite compartir información y comunicarse.
            
            Piense en Internet como una gran biblioteca donde puede:
            - Buscar información sobre cualquier tema
            - Comunicarse con familiares y amigos
            - Realizar trámites y pagos
            - Ver fotos, videos y escuchar música
            
            ## ¿Cómo nos conectamos a Internet?
            
            Para conectarnos a Internet necesitamos:
            1. Un dispositivo (computadora, celular o tablet)
            2. Una conexión a Internet (WiFi o datos móviles)
            3. Un navegador web (como Chrome, Firefox o Edge)
            
            ## Actividad práctica:
            Identifique en su dispositivo el ícono del navegador web y practique cómo abrirlo.
            
            ## Video explicativo:
            """,
            "video": "https://www.youtube.com/embed/JrF33N9zTCU",
            "quiz": [
                {
                    "pregunta": "¿Qué es Internet?",
                    "opciones": [
                        "Un programa para computadoras",
                        "Una red mundial de computadoras conectadas",
                        "Una compañía de telefonía",
                        "Un tipo de teléfono moderno"
                    ],
                    "respuesta_correcta": 1
                },
                {
                    "pregunta": "¿Qué necesitamos para conectarnos a Internet?",
                    "opciones": [
                        "Solo un teléfono celular",
                        "Una computadora y un televisor",
                        "Un dispositivo, una conexión y un navegador web",
                        "Una radio y una antena"
                    ],
                    "respuesta_correcta": 2
                },
                {
                    "pregunta": "¿Cuál de estos es un navegador web?",
                    "opciones": [
                        "WhatsApp",
                        "Chrome",
                        "Word",
                        "Calculadora"
                    ],
                    "respuesta_correcta": 1
                }
            ]
        },
        {
            "titulo": "Módulo 2: Navegación básica y búsqueda",
            "contenido": """
            # Módulo 2: Navegación básica y búsqueda
            
            ## Conociendo el navegador web
            
            El navegador web es la ventana que nos permite acceder a Internet. Sus partes principales son:
            
            - Barra de direcciones: donde escribimos la dirección de la página web
            - Botones de navegación: para ir hacia adelante, atrás o recargar la página
            - Pestañas: para abrir varias páginas a la vez
            
            ## Cómo buscar información
            
            Para buscar información en Internet:
            1. Abra su navegador
            2. Escriba "www.google.com" en la barra de direcciones
            3. En el cuadro de búsqueda, escriba lo que desea encontrar
            4. Presione "Enter" o haga clic en la lupa
            5. Revise los resultados y haga clic en los que le interesen
            
            ## Consejos para búsquedas efectivas:
            - Use palabras clave específicas
            - Sea breve pero descriptivo
            - Pruebe diferentes palabras si no encuentra lo que busca
            
            ## Video explicativo:
            """,
            "video": "https://www.youtube.com/embed/uy_zQAFx_gQ",
            "quiz": [
                {
                    "pregunta": "¿Dónde escribimos la dirección de una página web?",
                    "opciones": [
                        "En el teclado",
                        "En la barra de direcciones del navegador",
                        "En un mensaje de WhatsApp",
                        "En un papel"
                    ],
                    "respuesta_correcta": 1
                },
                {
                    "pregunta": "¿Cuál es un motor de búsqueda popular?",
                    "opciones": [
                        "Facebook",
                        "Microsoft Word",
                        "Google",
                        "WhatsApp"
                    ],
                    "respuesta_correcta": 2
                },
                {
                    "pregunta": "¿Qué debemos hacer para buscar información efectivamente?",
                    "opciones": [
                        "Escribir oraciones muy largas y detalladas",
                        "Usar palabras clave específicas",
                        "Usar solo mayúsculas",
                        "Buscar solo imágenes"
                    ],
                    "respuesta_correcta": 1
                }
            ]
        },
        {
            "titulo": "Módulo 3: Comunicación en línea",
            "contenido": """
            # Módulo 3: Comunicación en línea
            
            ## Correo electrónico (Email)
            
            El correo electrónico es como una carta digital que permite enviar y recibir mensajes instantáneamente.
            
            Partes de un correo electrónico:
            - Dirección de correo: similar a su@ejemplo.com
            - Asunto: breve descripción del contenido del mensaje
            - Cuerpo del mensaje: el contenido principal
            - Archivos adjuntos: fotos, documentos u otros archivos
            
            ## Videollamadas
            
            Las videollamadas permiten ver y hablar con sus seres queridos a distancia:
            - WhatsApp: ideal para llamadas desde el celular
            - Zoom: útil para reuniones grupales
            - Google Meet: fácil de usar desde el navegador
            
            ## Redes sociales
            
            Las redes sociales son plataformas para conectarse con amigos y familiares:
            - Facebook: la más popular entre adultos mayores
            - Instagram: para compartir fotos y videos
            - Twitter: para mensajes cortos e información actualizada
            
            ## Video explicativo:
            """,
            "video": "https://www.youtube.com/embed/Ak6ywKvv3vw",
            "quiz": [
                {
                    "pregunta": "¿Qué es un correo electrónico?",
                    "opciones": [
                        "Un mensaje de texto",
                        "Una carta digital",
                        "Una llamada telefónica",
                        "Una reunión virtual"
                    ],
                    "respuesta_correcta": 1
                },
                {
                    "pregunta": "¿Qué aplicación es útil para hacer videollamadas?",
                    "opciones": [
                        "Microsoft Word",
                        "Calculadora",
                        "WhatsApp",
                        "Bloc de notas"
                    ],
                    "respuesta_correcta": 2
                },
                {
                    "pregunta": "¿Cuál es la red social más popular entre adultos mayores?",
                    "opciones": [
                        "Facebook",
                        "TikTok",
                        "Snapchat",
                        "LinkedIn"
                    ],
                    "respuesta_correcta": 0
                }
            ]
        },
        {
            "titulo": "Módulo 4: Seguridad en Internet",
            "contenido": """
            # Módulo 4: Seguridad en Internet
            
            ## Contraseñas seguras
            
            Una contraseña segura es su primera línea de defensa:
            - Use al menos 8 caracteres
            - Combine letras mayúsculas, minúsculas, números y símbolos
            - Evite información personal (fechas de nacimiento, nombres)
            - Use contraseñas diferentes para cada servicio
            
            ## Identificando estafas comunes
            
            Esté atento a estas señales de posibles estafas:
            - Ofertas demasiado buenas para ser verdad
            - Mensajes con errores ortográficos o gramaticales
            - Solicitudes urgentes de dinero o información personal
            - Remitentes desconocidos
            
            ## Consejos de seguridad
            
            Para navegar de forma segura:
            - No comparta datos personales ni bancarios en sitios no confiables
            - Cierre sesión cuando termine de usar un servicio
            - Mantenga su dispositivo actualizado
            - Instale únicamente aplicaciones oficiales
            
            ## Video explicativo:
            """,
            "video": "https://www.youtube.com/embed/PSrKw2R1B9A",
            "quiz": [
                {
                    "pregunta": "¿Qué característica debe tener una contraseña segura?",
                    "opciones": [
                        "Ser corta y fácil de recordar",
                        "Contener solo números",
                        "Combinar letras, números y símbolos",
                        "Ser igual para todas sus cuentas"
                    ],
                    "respuesta_correcta": 2
                },
                {
                    "pregunta": "¿Cuál es una señal de posible estafa?",
                    "opciones": [
                        "Un mensaje de un familiar conocido",
                        "Una oferta demasiado buena para ser verdad",
                        "Un correo de su banco con su logo oficial",
                        "Una factura de un servicio que usted usa"
                    ],
                    "respuesta_correcta": 1
                },
                {
                    "pregunta": "¿Qué debe hacer cuando termina de usar un servicio en línea?",
                    "opciones": [
                        "Apagar el dispositivo inmediatamente",
                        "Guardar la contraseña en un papel",
                        "Cerrar sesión",
                        "Dejar la sesión abierta para la próxima vez"
                    ],
                    "respuesta_correcta": 2
                }
            ]
        }
    ]
}

# Definir otros cursos disponibles
otros_cursos = [
    {
        "titulo": "Usando WhatsApp como un experto",
        "descripcion": "Aprenda a comunicarse con sus seres queridos, enviar fotos, crear grupos y hacer videollamadas.",
        "imagen": "https://play-lh.googleusercontent.com/bYtqbOcTYOlgc6gqZ2rwb8lptHuwlNE75zYJu6Bn076-hTmvd96HH-6v7S0YUAAJXoJN=w240-h480-rw",
        "progreso": 0.3,
        "es_premium": False
    },
    {
        "titulo": "Cómo usar su teléfono inteligente",
        "descripcion": "Domine las funciones básicas y avanzadas de su smartphone para sacarle el máximo provecho.",
        "imagen": "https://cdn.thewirecutter.com/wp-content/media/2024/04/budgetandroidphones-2048px-1013.jpg",
        "progreso": 0,
        "es_premium": True
    },
    {
        "titulo": "Trámites online: ANSES, AFIP y más",
        "descripcion": "Aprenda a realizar gestiones gubernamentales desde la comodidad de su hogar.",
        "imagen": "https://vocescriticas-s2.cdn.net.ar/st2i1700/2023/03/vocescriticas/images/40/22/402237_5bc5677f9fa4f1a4b20da3481d403eee1397974df248c2dc047420f9b79744d0/lg.jpg",
        "progreso": 0,
        "es_premium": True
    },
    {
        "titulo": "Proteja su privacidad en línea",
        "descripcion": "Consejos y herramientas para navegar de forma segura y proteger sus datos personales.",
        "imagen": "https://www.segurilatam.com/wp-content/uploads/sites/5/2022/12/robo-de-informacion.jpg",
        "progreso": 0.1,
        "es_premium": False
    }
]

# Funciones para la navegación
def ir_a_inicio():
    st.session_state.pagina = "inicio"
    st.experimental_rerun()

def ir_a_mis_cursos():
    st.session_state.pagina = "mis_cursos"
    st.experimental_rerun()

def ir_a_comunidad():
    st.session_state.pagina = "comunidad"
    st.experimental_rerun()

def ir_a_planes():
    st.session_state.pagina = "planes"
    st.experimental_rerun()

def ir_a_login():
    st.session_state.pagina = "login"
    st.experimental_rerun()

def ir_a_registro():
    st.session_state.pagina = "registro"
    st.experimental_rerun()

def ir_a_curso():
    st.session_state.pagina = "curso"
    st.experimental_rerun()

def verificar_login(usuario, contraseña):
    # En un MVP simulamos la autenticación
    if usuario and contraseña:
        st.session_state.usuario_logueado = True
        st.session_state.nombre_usuario = usuario
        ir_a_inicio()
    else:
        st.error("Por favor, complete todos los campos.")

def cerrar_sesion():
    st.session_state.usuario_logueado = False
    st.session_state.nombre_usuario = ""
    ir_a_inicio()

def evaluar_respuesta(respuesta, respuesta_correcta):
    if respuesta == respuesta_correcta:
        st.session_state.respuestas_correctas += 1
        return True
    return False

def siguiente_pregunta():
    if st.session_state.pregunta_actual < len(curso_internet["modulos"][st.session_state.modulo_actual - 1]["quiz"]) - 1:
        st.session_state.pregunta_actual += 1
    else:
        st.session_state.mostrar_resultado = True

def reiniciar_quiz():
    st.session_state.respuestas_correctas = 0
    st.session_state.pregunta_actual = 0
    st.session_state.mostrar_resultado = False

def siguiente_modulo():
    if st.session_state.modulo_actual < len(curso_internet["modulos"]):
        st.session_state.modulo_actual += 1
        reiniciar_quiz()
    else:
        st.success("¡Felicidades! Ha completado todo el curso.")

def modulo_anterior():
    if st.session_state.modulo_actual > 1:
        st.session_state.modulo_actual -= 1
        reiniciar_quiz()

# Barra lateral para navegación
with st.sidebar:
    st.image("logo.png", width=200)
    st.markdown("## AdulTec")
    st.write("La experiencia de toda una vida, ahora también en digital")
    
    # Botón para cambiar tema
    tema_actual = "🌙 Modo oscuro" if st.session_state.theme == "light" else "☀️ Modo claro"
    if st.button(tema_actual):
        toggle_theme()
    
    st.markdown("---")
    
    # Menú de navegación
    if st.button("🏠 Inicio"):
        ir_a_inicio()
    
    if st.button("📚 Mis cursos"):
        ir_a_mis_cursos()
    
    if st.button("👥 Comunidad"):
        ir_a_comunidad()
    
    if st.button("💰 Planes y precios"):
        ir_a_planes()
    
    st.markdown("---")
    
    # Estado de sesión
    if st.session_state.usuario_logueado:
        st.write(f"👤 Usuario: {st.session_state.nombre_usuario}")
        if st.button("Cerrar sesión"):
            cerrar_sesion()
    else:
        if st.button("✅ Iniciar sesión"):
            ir_a_login()
        if st.button("📝 Registrarse"):
            ir_a_registro()

# Páginas de la aplicación
if st.session_state.pagina == "inicio":
    st.markdown(f"# {mostrar_bienvenida(st.session_state.nombre_usuario)}")
    
    st.markdown("""
    ### La academia online de habilidades digitales pensada para adultos mayores
    
    En AdulTec creemos que nunca es tarde para aprender. Nuestra plataforma está diseñada específicamente para adultos mayores que desean adquirir o mejorar sus habilidades tecnológicas.
    """)
    
    # Características principales
    st.markdown("## ¿Por qué elegir AdulTec?")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("""
        <div class="feature-card">
            <div class="icon-large">👴👵</div>
            <h3>Diseñado para usted</h3>
            <p>Interfaz simple y accesible con letras grandes y colores contrastantes.</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class="feature-card">
            <div class="icon-large">🤝</div>
            <h3>Apoyo constante</h3>
            <p>Tutores especializados y una comunidad amigable para resolver sus dudas.</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown("""
        <div class="feature-card">
            <div class="icon-large">🎯</div>
            <h3>Contenido práctico</h3>
            <p>Aprenda exactamente lo que necesita para su día a día digital.</p>
        </div>
        """, unsafe_allow_html=True)
    
    # Curso destacado
    st.markdown("## Curso recomendado para empezar")
    
    crear_tarjeta_curso(
        "¿Qué es Internet y cómo usarlo de forma segura?",
        "Curso básico para entender qué es Internet, cómo navegar de forma segura y proteger su información personal.",
        "https://cdn-icons-png.flaticon.com/512/5054/5054674.png"
    )
    
    # Testimonios
    st.markdown("## Lo que dicen nuestros estudiantes")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        <div class="container">
            <p>"Gracias a AdulTec ahora puedo hacer videollamadas con mis nietos sin pedir ayuda. Las explicaciones son claras y los profesores muy pacientes."</p>
            <p><strong>- María, 72 años</strong></p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class="container">
            <p>"Nunca pensé que podría usar un smartphone con tanta facilidad. Los cursos son excelentes y el ritmo perfecto para mí."</p>
            <p><strong>- Jorge, 68 años</strong></p>
        </div>
        """, unsafe_allow_html=True)
    
    # Llamada a la acción
    st.markdown("## ¿Listo para comenzar?")
    
    col1, col2 = st.columns(2)
    
    with col1:
        if st.button("📚 Ver todos los cursos"):
            ir_a_mis_cursos()
    
    with col2:
        if st.button("💰 Conocer nuestros planes"):
            ir_a_planes()
    
    # Pie de página
    st.markdown("""
    <div class="footer">
        AdulTec © 2025 - La experiencia de toda una vida, ahora también en digital
    </div>
    """, unsafe_allow_html=True)

elif st.session_state.pagina == "mis_cursos":
    st.markdown("# Mis cursos")
    
    # Curso principal con progreso completo
    st.markdown("## Curso en progreso")
    crear_tarjeta_curso(
        curso_internet["titulo"],
        "Curso básico para entender qué es Internet, cómo navegar de forma segura y proteger su información personal.",
        "https://cdn-icons-png.flaticon.com/512/5054/5054674.png",
        0.5
    )
    
    # Otros cursos disponibles
    st.markdown("## Otros cursos disponibles")
    
    for curso in otros_cursos:
        crear_tarjeta_curso(
            curso["titulo"],
            curso["descripcion"],
            curso["imagen"],
            curso["progreso"],
            curso["es_premium"]
        )

elif st.session_state.pagina == "comunidad":
    st.markdown("# Comunidad de AdulTec")
    
    st.markdown("""
    Bienvenido/a a nuestra comunidad de aprendizaje. Aquí puede hacer preguntas, compartir experiencias y conectarse con otros estudiantes.
    """)
    
    # Opciones de la comunidad
    tab1, tab2, tab3 = st.tabs(["📋 Preguntas frecuentes", "❓ Hacer una pregunta", "👥 Foro de estudiantes"])
    
    with tab1:
        st.markdown("## Preguntas frecuentes")
        
        with st.expander("¿Cómo puedo cambiar mi contraseña?"):
            st.write("""
            Para cambiar su contraseña, siga estos pasos:
            1. Haga clic en su nombre de usuario en la esquina superior derecha
            2. Seleccione "Mi perfil"
            3. Haga clic en "Cambiar contraseña"
            4. Siga las instrucciones en pantalla
            """)
        
        with st.expander("¿Cómo accedo a mis cursos?"):
            st.write("""
            Puede acceder a sus cursos de dos formas:
            1. Haciendo clic en "Mis cursos" en el menú lateral
            2. Desde la página de inicio, en la sección "Curso en progreso"
            """)
        
        with st.expander("¿Los cursos tienen caducidad?"):
            st.write("""
            No, una vez que se inscribe en un curso, tiene acceso de por vida. Puede avanzar a su propio ritmo y revisar el contenido cuantas veces quiera.
            """)
        
        with st.expander("¿Cómo obtengo ayuda si tengo problemas técnicos?"):
            st.write("""
            Puede obtener ayuda de varias formas:
            1. Use el botón verde de WhatsApp que aparece en la esquina inferior derecha
            2. Envíe un correo a ayuda@adultec.com
            3. Llame al 0800-ADULTEC (0800-2385832)
            
            Nuestro equipo de soporte está disponible de lunes a viernes de 9:00 a 18:00 hs.
            """)
    
    with tab2:
        st.markdown("## Haga su pregunta")
        
        st.write("Complete el formulario a continuación y le responderemos en un plazo máximo de 24 horas.")
        
        categoria = st.selectbox(
            "Categoría de la consulta:",
            ["Seleccione una categoría", "Problemas técnicos", "Contenido de los cursos", "Facturación y pagos", "Otros"]
        )
        
        titulo = st.text_input("Título de su pregunta:", placeholder="Ej: No puedo acceder al curso de WhatsApp")
        
        detalle = st.text_area(
            "Describa su consulta en detalle:",
            height=150,
            placeholder="Por favor, describa su problema o pregunta con el mayor detalle posible. Cuanta más información nos brinde, mejor podremos ayudarle."
        )
        
        if st.button("Enviar consulta"):
            if categoria != "Seleccione una categoría" and titulo and detalle:
                st.success("¡Su consulta ha sido enviada con éxito! Le responderemos pronto.")
            else:
                st.error("Por favor, complete todos los campos.")
    
    with tab3:
        st.markdown("## Foro de estudiantes")
        
        # Simulación de conversaciones en el foro
        conversaciones = [
            {
                "autor": "Marta G.",
                "fecha": "Ayer",
                "titulo": "¿Cómo guardo una foto de WhatsApp en mi galería?",
                "respuestas": 3,
                "ultimo_mensaje": "Hace 2 horas"
            },
            {
                "autor": "Roberto P.",
                "fecha": "Hace 3 días",
                "titulo": "Recomendación de teclado con letras más grandes",
                "respuestas": 7,
                "ultimo_mensaje": "Hoy"
            },
            {
                "autor": "Carmen L.",
                "fecha": "Hace 1 semana",
                "titulo": "Problema para hacer compras en Mercado Libre",
                "respuestas": 5,
                "ultimo_mensaje": "Hace 2 días"
            }
        ]
        
        # Filtros
        col1, col2 = st.columns(2)
        with col1:
            filtro = st.selectbox("Ordenar por:", ["Más recientes", "Más comentados", "Sin respuesta"])
        with col2:
            busqueda = st.text_input("Buscar:", placeholder="Escriba palabras clave...")
        
        # Mostrar conversaciones
        for i, conv in enumerate(conversaciones):
            st.markdown(f"""
            <div class="container">
                <h3>{conv['titulo']}</h3>
                <p>Iniciado por {conv['autor']} • {conv['fecha']} • {conv['respuestas']} respuestas • Última actividad: {conv['ultimo_mensaje']}</p>
                <button>Ver conversación</button>
            </div>
            """, unsafe_allow_html=True)
        
        # Botón para crear nuevo tema
        if st.button("Crear nuevo tema"):
            st.info("Función en desarrollo. Estará disponible próximamente.")

elif st.session_state.pagina == "planes":
    st.markdown("# Planes y precios")
    
    st.markdown("""
    Elija el plan que mejor se adapte a sus necesidades. Todos nuestros planes incluyen acceso a la comunidad de apoyo y contenido actualizado regularmente.
    """)
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("""
        <div class="container">
            <h3>Plan Básico</h3>
            <h2>Gratis</h2>
            <ul>
                <li>Acceso a 2 cursos básicos</li>
                <li>Comunidad de apoyo</li>
                <li>Quizzes y evaluaciones</li>
                <li>Contenido con publicidad</li>
            </ul>
            <button>Comenzar ahora</button>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class="container">
            <h3>Plan Estándar</h3>
            <h2>$15.000 /mes</h2>
            <p><small>O $150.000 /año (ahorra 2 meses)</small></p>
            <ul>
                <li>Acceso a todos los cursos</li>
                <li>Sin publicidad</li>
                <li>Tutorías grupales semanales</li>
                <li>Certificados de finalización</li>
            </ul>
            <button>Suscribirse</button>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown("""
        <div class="container">
            <h3>Plan Premium</h3>
            <h2>$28.000 /mes</h2>
            <p><small>O $280.000 /año (ahorra 2 meses)</small></p>
            <ul>
                <li>Todo lo del plan Estándar</li>
                <li>2 tutorías personalizadas al mes</li>
                <li>Soporte técnico prioritario</li>
                <li>Configuración inicial remota</li>
            </ul>
            <button>Suscribirse</button>
        </div>
        """, unsafe_allow_html=True)
    
    # Descuentos especiales
    st.markdown("## Descuentos especiales")
    
    st.markdown("""
    <div class="container">
        <h3>Descuentos para jubilados</h3>
        <p>Presentando su carnet de jubilado o pensionado, obtenga un 20% de descuento en cualquier plan.</p>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("""
    <div class="container">
        <h3>Plan familiar</h3>
        <p>Comparta su suscripción con hasta 3 miembros de su familia y ahorre un 30% del valor total.</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Preguntas frecuentes sobre planes
    st.markdown("## Preguntas frecuentes sobre planes")
    
    with st.expander("¿Puedo cancelar mi suscripción en cualquier momento?"):
        st.write("Sí, puede cancelar su suscripción cuando lo desee. No hay permanencia mínima ni penalizaciones por cancelación anticipada.")
    
    with st.expander("¿Qué métodos de pago aceptan?"):
        st.write("Aceptamos tarjetas de crédito y débito (Visa, MasterCard, American Express), transferencia bancaria y Mercado Pago.")
    
    with st.expander("¿Ofrecen períodos de prueba?"):
        st.write("Sí, ofrecemos 7 días de prueba gratuita en los planes Estándar y Premium para que pueda evaluar si el servicio se adapta a sus necesidades.")
    
    with st.expander("¿Hay becas disponibles?"):
        st.write("Sí, contamos con un programa de becas para personas con bajos recursos. Puede solicitar más información escribiendo a becas@adultec.com.")

elif st.session_state.pagina == "login":
    st.markdown("# Iniciar sesión")
    
    st.markdown("""
    Complete los siguientes campos para acceder a su cuenta. Si aún no tiene una cuenta, puede registrarse haciendo clic en "Registrarse" en el menú lateral.
    """)
    
    with st.form("formulario_login"):
        usuario = st.text_input("Correo electrónico o nombre de usuario:", placeholder="ejemplo@gmail.com")
        contraseña = st.text_input("Contraseña:", type="password")
        recordar = st.checkbox("Recordar mi usuario")
        
        col1, col2 = st.columns(2)
        with col1:
            enviar = st.form_submit_button("Iniciar sesión")
        with col2:
            st.markdown("[¿Olvidó su contraseña?](#)")
        
        if enviar:
            verificar_login(usuario, contraseña)

elif st.session_state.pagina == "registro":
    st.markdown("# Crear una cuenta")
    
    st.markdown("""
    Complete el siguiente formulario para registrarse en AdulTec. Los campos marcados con * son obligatorios.
    """)
    
    with st.form("formulario_registro"):
        col1, col2 = st.columns(2)
        
        with col1:
            nombre = st.text_input("Nombre*:", placeholder="Juan")
        
        with col2:
            apellido = st.text_input("Apellido*:", placeholder="Pérez")
        
        email = st.text_input("Correo electrónico*:", placeholder="ejemplo@gmail.com")
        
        col1, col2 = st.columns(2)
        
        with col1:
            contraseña = st.text_input("Contraseña*:", type="password")
        
        with col2:
            confirmar_contraseña = st.text_input("Confirmar contraseña*:", type="password")
        
        fecha_nacimiento = st.date_input("Fecha de nacimiento:")
        
        acepto_terminos = st.checkbox("Acepto los términos y condiciones*")
        recibir_novedades = st.checkbox("Deseo recibir novedades y promociones por correo electrónico")
        
        enviar = st.form_submit_button("Registrarse")
        
        if enviar:
            if nombre and apellido and email and contraseña and confirmar_contraseña and acepto_terminos:
                if contraseña == confirmar_contraseña:
                    st.success("¡Registro exitoso! Ahora puede iniciar sesión con sus credenciales.")
                    st.session_state.nombre_usuario = nombre
                    time.sleep(2)
                    ir_a_login()
                else:
                    st.error("Las contraseñas no coinciden. Por favor, inténtelo nuevamente.")
            else:
                st.error("Por favor, complete todos los campos obligatorios.")

elif st.session_state.pagina == "curso":
    # Obtener el módulo actual
    modulo = curso_internet["modulos"][st.session_state.modulo_actual - 1]
    
    # Barra de navegación del curso
    col1, col2, col3 = st.columns([1, 3, 1])
    with col1:
        if st.session_state.modulo_actual > 1:
            if st.button("« Módulo anterior"):
                modulo_anterior()
    with col2:
        st.markdown(f"# {curso_internet['titulo']}")
    with col3:
        if st.session_state.modulo_actual < len(curso_internet["modulos"]):
            if st.button("Módulo siguiente »"):
                siguiente_modulo()
    
    # Progreso del curso
    progreso_curso = st.session_state.modulo_actual / len(curso_internet["modulos"])
    st.progress(progreso_curso)
    st.write(f"Progreso del curso: {int(progreso_curso*100)}% ({st.session_state.modulo_actual} de {len(curso_internet['modulos'])} módulos)")
    
    # Pestañas del módulo actual
    tab1, tab2 = st.tabs(["📚 Contenido", "🎯 Evaluación"])
    
    with tab1:
        # Contenido del módulo
        st.markdown(modulo["contenido"])
        
        # Video del módulo (embebido de YouTube)
        st.markdown(f"""
        <div style="display: flex; justify-content: center; margin: 30px 0;">
            <iframe width="560" height="315" src="{modulo['video']}" title="YouTube video player" frameborder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture" allowfullscreen></iframe>
        </div>
        """, unsafe_allow_html=True)
        
        # Botón para ir a la evaluación
        if st.button("Ir a la evaluación"):
            st.session_state.mostrar_resultado = False
            st.session_state.pregunta_actual = 0
            st.session_state.respuestas_correctas = 0
    
    with tab2:
        # Evaluación del módulo
        st.markdown(f"## Evaluación del {modulo['titulo']}")
        
        if not st.session_state.mostrar_resultado:
            # Mostrar pregunta actual
            pregunta_actual = modulo["quiz"][st.session_state.pregunta_actual]
            st.markdown(f"### Pregunta {st.session_state.pregunta_actual + 1} de {len(modulo['quiz'])}")
            st.markdown(f"**{pregunta_actual['pregunta']}**")
            
            # Opciones de respuesta
            respuesta = st.radio(
                "Seleccione la respuesta correcta:",
                pregunta_actual["opciones"],
                key=f"quiz_{st.session_state.modulo_actual}_{st.session_state.pregunta_actual}"
            )
            
            if st.button("Comprobar respuesta"):
                indice_respuesta = pregunta_actual["opciones"].index(respuesta)
                if evaluar_respuesta(indice_respuesta, pregunta_actual["respuesta_correcta"]):
                    st.success("¡Respuesta correcta! 👏")
                else:
                    st.error(f"Respuesta incorrecta. La respuesta correcta era: {pregunta_actual['opciones'][pregunta_actual['respuesta_correcta']]}")
                
                if st.button("Siguiente pregunta"):
                    siguiente_pregunta()
                    st.experimental_rerun()
        else:
            # Mostrar resultados del quiz
            st.markdown("### Resultados de la evaluación")
            st.write(f"Ha respondido correctamente {st.session_state.respuestas_correctas} de {len(modulo['quiz'])} preguntas.")
            
            # Calcular porcentaje de aciertos
            porcentaje = (st.session_state.respuestas_correctas / len(modulo['quiz'])) * 100
            
            if porcentaje >= 70:
                st.success(f"¡Felicitaciones! Ha aprobado con un {porcentaje:.0f}% de aciertos.")
                if st.session_state.modulo_actual < len(curso_internet["modulos"]):
                    if st.button("Continuar al siguiente módulo"):
                        siguiente_modulo()
                else:
                    st.balloons()
                    st.success("¡Felicitaciones! Ha completado todo el curso.")
            else:
                st.warning(f"Ha obtenido un {porcentaje:.0f}% de aciertos. Necesita al menos 70% para aprobar.")
                if st.button("Intentar nuevamente"):
                    reiniciar_quiz()
                    st.experimental_rerun()
            
            # Opción para repasar el contenido
            if st.button("Repasar el contenido"):
                st.session_state.mostrar_resultado = False
                st.experimental_rerun()

# Footer y botón de WhatsApp en todas las páginas
st.markdown("""
<div class="footer">
    AdulTec © 2025 - La experiencia de toda una vida, ahora también en digital
</div>
""", unsafe_allow_html=True)