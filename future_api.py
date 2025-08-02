"""
StreamLabs API v2.0 Integration
Este archivo se usará cuando aprueben tu aplicación
"""

import requests
import websocket
import json
import time
import threading
from obswebsocket import obsws, requests as obsrequests
import config

class StreamLabsAPIv2:
    def __init__(self, access_token):
        self.access_token = access_token
        self.base_url = "https://streamlabs.com/api/v2.0"
        self.socket_url = "wss://sockets.streamlabs.com/socket.io/"
        
    def get_headers(self):
        """Headers para autenticación Bearer"""
        return {
            "Authorization": f"Bearer {self.access_token}",
            "Content-Type": "application/json"
        }
    
    def test_connection(self):
        """Testear conexión con la API v2.0"""
        try:
            response = requests.get(
                f"{self.base_url}/user",
                headers=self.get_headers()
            )
            response.raise_for_status()
            return response.json()
        except Exception as e:
            print(f"❌ Error en conexión API v2.0: {e}")
            return None
    
    def connect_websocket(self):
        """Conexión WebSocket con Bearer Token"""
        # En la nueva versión, el token va en headers, no en query params
        headers = {
            "Authorization": f"Bearer {self.access_token}"
        }
        
        # La URL del WebSocket cambiará
        socket_url = f"wss://sockets.streamlabs.com/socket.io/"
        
        return socket_url, headers

class FutureStreamAlerts:
    def __init__(self, access_token):
        self.api = StreamLabsAPIv2(access_token)
        self.obs_ws = None
        self.connect_to_obs()
        
    def connect_to_obs(self):
        """Conectar a OBS WebSocket"""
        try:
            self.obs_ws = obsws(
                config.OBS_HOST, 
                config.OBS_PORT, 
                config.OBS_PASSWORD
            )
            self.obs_ws.connect()
            print("✅ Conectado a OBS WebSocket")
        except Exception as e:
            print(f"❌ Error conectando a OBS: {e}")
            self.obs_ws = None

    def show_alert_video(self):
        """Mostrar video overlay"""
        if not self.obs_ws:
            return
            
        try:
            # Mostrar video
            self.obs_ws.call(obsrequests.SetSourceRender(
                config.VIDEO_SOURCE_NAME, True
            ))
            
            # Reiniciar video
            try:
                self.obs_ws.call(obsrequests.RestartMedia(config.VIDEO_SOURCE_NAME))
            except:
                pass
            
            time.sleep(config.ALERT_DURATION)
            
            # Ocultar video
            self.obs_ws.call(obsrequests.SetSourceRender(
                config.VIDEO_SOURCE_NAME, False
            ))
            
        except Exception as e:
            print(f"❌ Error con video: {e}")

    def on_websocket_message(self, ws, message):
        """Manejar mensajes WebSocket v2.0"""
        try:
            # Procesar mensajes con nueva estructura
            if message.startswith('42'):
                json_part = message[2:]
                data = json.loads(json_part)
                
                if isinstance(data, list) and len(data) > 0:
                    event_data = data[1] if len(data) > 1 else data[0]
                    
                    if isinstance(event_data, dict) and 'type' in event_data:
                        if event_data['type'] in config.ALERT_TYPES:
                            self.process_alert(event_data)
                            
        except Exception as e:
            print(f"❌ Error procesando mensaje v2.0: {e}")

    def process_alert(self, event_data):
        """Procesar alerta con nueva estructura"""
        alert_type = event_data['type']
        username = self.extract_username(event_data)
        
        print(f"🔔 Nueva alerta [{alert_type}]: {username}")
        
        alert_thread = threading.Thread(target=self.show_alert_video)
        alert_thread.daemon = True
        alert_thread.start()

    def extract_username(self, event_data):
        """Extraer nombre de usuario"""
        username = "Anónimo"
        
        if 'message' in event_data and isinstance(event_data['message'], list):
            if len(event_data['message']) > 0:
                msg = event_data['message'][0]
                if isinstance(msg, dict):
                    username = msg.get('name') or msg.get('username') or "Anónimo"
        elif 'event' in event_data:
            event_info = event_data['event']
            if isinstance(event_info, dict):
                username = event_info.get('name') or event_info.get('username') or "Anónimo"
                
        return username

# Función para cuando te aprueben la app
def start_future_version(access_token):
    """Iniciar versión con API v2.0"""
    alerts = FutureStreamAlerts(access_token)
    
    # Testear conexión primero
    if alerts.api.test_connection():
        print("✅ API v2.0 funcionando correctamente")
        # Aquí iría la lógica de WebSocket con nueva autenticación
    else:
        print("❌ Error con API v2.0 - verifica tu access_token")