# StreamAlert Overlay

🎨 **Overlay de video para alertas de StreamLabs - Muestra videos personalizados sobre cualquier escena de OBS**

## 🌟 Características
- Muestra videos como overlay sin cambiar de escena
- Compatible con alertas de follow, subs, donaciones
- Funciona con cualquier escena activa
- Se combina perfectamente con alertas existentes de StreamLabs

## 🛠️ Requisitos
- OBS con WebSocket plugin
- Token de StreamLabs Socket API
- Python 3.7+

## 🚀 Instalación
- Requerimientos:
    obs-websocket-py==1.0
    requests==2.31.0
    websocket-client==1.6.1
  
- Instalación de dependencias:
    en windows en el powershell:
      "pip install websocket-client requests obs-websocket-py"
  
- ESTRUCTURA DE ARCHIVOS RECOMENDADA:
```
stream_alerts/
├── main.py              # Tu script principal
├── config.py            # Configuración (tokens, escenas)
├── requirements.txt     # Dependencias
└── videos/              # Carpeta para videos (opcional) 
```
- Ejecutar el Script:
    "python main.py"
  
## ⚙️ CONFIGURACIÓN EN OBS: 
Activar WebSocket: 
    1. OBS → Herramientas → WebSocket Server Settings
    2. Marca "Enable WebSocket server"
    3. Puerto: 4444
    4. Establece una contraseña segura
Crear escenas: 
  1. "Principal" - Tu escena normal
  2. "AlertaVideo" - Escena con tu video de alerta

## 🎯 CONFIGURACIÓN FINAL:
- En config.py, reemplaza:
```python
STREAMLABS_TOKEN = "tu_token_real_aqui"
OBS_PASSWORD = "tu_contraseña_real"
ALERT_SCENE = "AlertaVideo"
NORMAL_SCENE = "Principal"
```       
## ❤️ Agradecimientos
Script desarrollado con IA Qwen3-coder https://chat.qwen.ai/ y la ayuda de VjTuX - ¡Gracias por la colaboración!
