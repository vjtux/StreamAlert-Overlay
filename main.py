import websocket
import json
import time
import threading
from obswebsocket import obsws, requests as obsrequests
import config

class StreamAlerts:
    def __init__(self):
        # Conexión a OBS
        self.obs_ws = obsws(
            config.OBS_HOST, 
            config.OBS_PORT, 
            config.OBS_PASSWORD
        )
        
        try:
            self.obs_ws.connect()
            print("✅ Conectado a OBS WebSocket")
            print(f"📺 Controlando fuente: {config.VIDEO_SOURCE_NAME}")
        except Exception as e:
            print(f"❌ Error conectando a OBS: {e}")
            return

    def show_alert_video(self):
        """Muestra el video overlay y luego lo oculta"""
        try:
            # Mostrar el video (hacer visible la fuente)
            self.obs_ws.call(obsrequests.SetSourceRender(
                config.VIDEO_SOURCE_NAME, 
                True
            ))
            print(f"🎬 Mostrando video overlay: {config.VIDEO_SOURCE_NAME}")
            
            # Si se especificó un archivo de video, cargarlo
            if config.VIDEO_FILE_PATH:
                self.obs_ws.call(obsrequests.SetSourceSettings(
                    config.VIDEO_SOURCE_NAME,
                    {"local_file": config.VIDEO_FILE_PATH}
                ))
            
            # Reproducir el video desde el inicio
            self.obs_ws.call(obsrequests.RestartMedia(config.VIDEO_SOURCE_NAME))
            
            # Esperar la duración configurada
            time.sleep(config.ALERT_DURATION)
            
            # Ocultar el video (hacer invisible la fuente)
            self.obs_ws.call(obsrequests.SetSourceRender(
                config.VIDEO_SOURCE_NAME, 
                False
            ))
            print(f"📺 Ocultando video overlay: {config.VIDEO_SOURCE_NAME}")
            
        except Exception as e:
            print(f"❌ Error controlando video: {e}")

    def on_message(self, ws, message):
        """Maneja los mensajes recibidos de StreamLabs"""
        try:
            # Debug: mostrar mensajes recibidos (opcional)
            # print(f"📥 Mensaje recibido: {message}")
            #if config.DEBUG_MODE:
            #    print(f"📥 Raw message: {message}")

            data = json.loads(message)
        
            # Verificar que sea un diccionario válido
            if not isinstance(data, dict):
                return
            
            # Verificar si es un mensaje de sistema (ping, etc.)
            if 'type' not in data:
                return
            
            # Procesar alertas
            if data['type'] in config.ALERT_TYPES:
                alert_type = data['type']
            
                # Extraer información del usuario
                username = "Anónimo"
            
                # Diferentes formatos de mensaje de StreamLabs
                if 'message' in data and isinstance(data['message'], list) and len(data['message']) > 0:
                    msg_data = data['message'][0]
                    if isinstance(msg_data, dict):
                        username = msg_data.get('name') or msg_data.get('username') or msg_data.get('displayName') or "Anónimo"
                elif 'event' in data and isinstance(data['event'], dict):
                    username = data['event'].get('name') or data['event'].get('username') or "Anónimo"
            
                print(f"🔔 Nueva alerta [{alert_type}]: {username}")
            
                # Ejecutar en thread separado
                alert_thread = threading.Thread(target=self.show_alert_video)
                alert_thread.daemon = True
                alert_thread.start()
            
        except json.JSONDecodeError:
            # Mensajes de sistema WebSocket, ignorar
            pass
        except Exception as e:
            print(f"❌ Error procesando mensaje: {e}")
            #print(f"📝 Mensaje completo: {message}")  # Descomentar para debug

    def on_error(self, ws, error):
        print(f"❌ Error de WebSocket: {error}")

    def on_close(self, ws, close_status_code, close_msg):
        print("🔌 Conexión cerrada")

    def on_open(self, ws):
        print("✅ Conectado a StreamLabs Socket API")

    def start(self):
        """Inicia la conexión a StreamLabs"""
        socket_url = f"wss://sockets.streamlabs.com/socket.io/?token={config.STREAMLABS_TOKEN}&transport=websocket"
        
        ws = websocket.WebSocketApp(
            socket_url,
            on_open=self.on_open,
            on_message=self.on_message,
            on_error=self.on_error,
            on_close=self.on_close
        )
        
        print("🚀 Iniciando escucha de alertas...")
        print("💡 El video se mostrará como overlay sobre cualquier escena actual")
        ws.run_forever()

if __name__ == "__main__":
    alerts = StreamAlerts()
    try:
        alerts.start()
    except KeyboardInterrupt:
        print("\n👋 Script detenido por el usuario")
