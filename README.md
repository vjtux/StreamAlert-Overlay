## 🚧 Estado del proyecto
⚠️ **En espera de aprobación de StreamLabs**
StreamLabs actualizó su API el 2024 y requiere aprobación de aplicaciones.
Este proyecto estará completamente funcional una vez aprobado.

✅ **Funcionalidad preparada**
- Código compatible con nueva API v2.0
- Sistema de autenticación Bearer
- WebSockets mejorados

### Versión actual (esperando aprobación):
- Usa el archivo `future_api.py` preparado
- Compatible con autenticación Bearer
- WebSockets con nueva estructura

### Cuando aprueben tu app:
1. Reemplaza tu `STREAMLABS_TOKEN` por el `ACCESS_TOKEN`
2. Usa la autenticación Bearer
3. El sistema funcionará automáticamente

### Archivos preparados:
- `future_api.py` - Integración con API v2.0
- `main.py` - Versión actual (mientras esperas)
_________________________________________

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
    - obs-websocket-py==1.0
    - requests==2.31.0
    - websocket-client==1.6.1
  
- Instalación de dependencias:
    en windows en el powershell:
  ```bash
      pip install websocket-client requests obs-websocket-py
  ```
- Instalación de dependencias por medio del archivo `requirements.txt`
  ```bash
  pip install -r requirements.txt
  ```
  
- ESTRUCTURA DE ARCHIVOS RECOMENDADA:
```
stream_alerts/
├── main.py              # Tu script principal
├── config.py            # Configuración (tokens, escenas)
├── future_api.py        # ✨ NUEVO ARCHIVO PARA LA VERSIÓN FUTURA
├── requirements.txt     # Dependencias
└── videos/              # Carpeta para videos (opcional) 
```
- Ejecutar el Script:
```bash
  python main.py
```
## ⚙️ CONFIGURACIÓN EN OBS: 
1. Crear la fuente de video overlay: 
    1. En tu escena principal (y en todas las que uses):
    2. Click en "+" → "Fuente de medios"
    3. Nombre: "AlertaVideoOverlay" (mismo que en config.py)
    4. Configura tu video:
       - Selecciona tu archivo de video
       - Marca "Reiniciar reproducción al activar"
       - Ajusta posición y tamaño

2. Configurar el overlay:
   - Posición: Donde quieras que aparezca el video
   - Tamaño: Ajusta según tu diseño
   - Filtros: Puedes añadir efectos como borde, sombra, etc.

3. Importante:
   - La fuente debe estar oculta por defecto (desmarcada la casilla de visibilidad)
   - El script se encargará de mostrar/ocultar automáticamente

## 🎨 TIPS PARA EL VIDEO OVERLAY:
Formato recomendado:
- MP4 con codec H.264
- Resolución: 1920x1080 o menor
- Duración: 8-15 segundos (ajusta ALERT_DURATION)

Estilo recomendado:
- Fondo transparente o con efecto de entrada/salida
- Animación de aparición suave
- Coordinado con el estilo de tus alertas de StreamLabs
    
## 🚀 VENTAJAS DE ESTE MÉTODO: 
    ✅ No cambia de escena - mantiene el flujo natural
    ✅ Funciona en cualquier escena que tenga la fuente
    ✅ Se combina con las alertas existentes de StreamLabs
    ✅ Más profesional - sin cortes de escena
     
     
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
