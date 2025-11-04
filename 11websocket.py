import os
from dotenv import load_dotenv
import websockets
import json
import base64

load_dotenv()

ELEVENLABS_API_KEY = os.getenv("ELEVENLABS_API_KEY")

voice_id = 'Xb7hH8MSUJpSbSDYk0k2'

# For use cases where latency is important, we recommend using the 'eleven_flash_v2_5' model.
model_id = 'eleven_flash_v2_5'

async def text_to_speech_ws_streaming(voice_id, model_id):
    uri = f"wss://api.elevenlabs.io/v1/text-to-speech/{voice_id}/stream-input?model_id={model_id}"

    async with websockets.connect(uri) as websocket:
        await websocket.send(json.dumps({
            "text": " ",
            "voice_settings": {"stability": 0.5, "similarity_boost": 0.8, "use_speaker_boost": False},
            "generation_config": {
                "chunk_length_schedule": [120, 160, 250, 290]
            },
            "xi_api_key": ELEVENLABS_API_KEY,
        }))

        text = """El Caballero Carmelo, con su plumaje brillante y su espíritu indomable,
        representa la nobleza que trasciende la lucha. En medio del bullicio de la arena y
        los gritos del público, su figura se alza como símbolo de dignidad, coraje y resistencia.
        Aunque envejecido y lejos de sus días de gloria, su última batalla no es solo contra otro gallo,
        sino contra el olvido, demostrando que la verdadera grandeza no se mide por la victoria,
        sino por la forma en que se enfrenta el destino.
        Su historia nos recuerda que el honor vive en cada acto de valentía,
        incluso cuando el mundo parece haberlo olvidado.
        """
        await websocket.send(json.dumps({"text": text}))

        ## Send empty string to indicate the end of the text sequence which will close the WebSocket connection
        await websocket.send(json.dumps({"text": ""}))

        # Add listen task to submit the audio chunks to the write_to_local function
        listen_task = asyncio.create_task(write_to_local(listen(websocket)))

        await listen_task

import asyncio

async def write_to_local(audio_stream):
    """Write the audio encoded in base64 string to a local mp3 file."""

    with open(f'./audio/output_test.mp3', "wb") as f:
        async for chunk in audio_stream:
            if chunk:
                f.write(chunk)

async def listen(websocket):
    """Listen to the websocket for audio data and stream it."""
    print("listening...")
    while True:
        try:
            message = await websocket.recv()
            data = json.loads(message)
            if data.get("audio"):
                yield base64.b64decode(data["audio"])
            elif data.get('isFinal'):
                break

        except websockets.exceptions.ConnectionClosed:
            print("Connection closed")
            break

asyncio.run(text_to_speech_ws_streaming(voice_id, model_id))