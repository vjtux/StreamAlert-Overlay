# Configuración de StreamLabs
STREAMLABS_TOKEN = "TU_TOKEN_AQUI"

# Configuración de OBS WebSocket
OBS_HOST = "localhost"
OBS_PORT = 4444
OBS_PASSWORD = "TU_CONTRASEÑA"

# Nombre de la fuente de video en OBS (debe existir en todas tus escenas)
VIDEO_SOURCE_NAME = "AlertaVideoOverlay"

# Duración de la alerta (en segundos) - ajusta según tu video
ALERT_DURATION = 10

# Tipos de alertas a manejar
ALERT_TYPES = ["follow", "subscription", "donation", "host"]

# Ruta al video (opcional, si quieres cambiar el video)
VIDEO_FILE_PATH = ""  # Dejar vacío si ya está configurado en OBS
