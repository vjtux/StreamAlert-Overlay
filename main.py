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
            data = json.loads(message)
            
            if 'type' in data and data['type'] in config.ALERT_TYPES:
                alert_type = data['type']
                alert_message = data.get('message', [{}])[0] if data.get('message') else {}
                
                print(f"🔔 Nueva alerta [{alert_type}]: {alert_message.get('name', 'Anónimo')}")
                
                # Ejecutar en thread separado para no bloquear
                alert_thread = threading.Thread(target=self.show_alert_video)
                alert_thread.daemon = True
                alert_thread.start()
                
        except json.JSONDecodeError:
            pass  # Mensajes de sistema, ignorar
        except Exception as e:
            print(f"❌ Error procesando mensaje: {e}")

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
