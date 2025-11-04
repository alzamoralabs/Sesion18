from elevenlabs.client import ElevenLabs
from elevenlabs.conversational_ai.conversation import Conversation, ClientTools
from elevenlabs.conversational_ai.default_audio_interface import DefaultAudioInterface
import os
from dotenv import load_dotenv

load_dotenv()
api_key = os.getenv("ELEVENLABS_API_KEY")
agent_id = os.getenv("ELEVENLABS_AGENT_ID")

client = ElevenLabs(api_key=api_key)

# Create audio interface for real-time audio input/output
audio_interface = DefaultAudioInterface()

# Create conversation
conversation = Conversation(
    client=client,
    agent_id=agent_id,
    requires_auth=True, #Asegurarse que esto este siempre en True ya que enfuerza el API KEY. Si esta en Falso se lo salta ah!
    audio_interface=audio_interface,
)

# Start the conversation
conversation.start_session()

while(1):
    respuesta = input("Ingresa X para Colgar>")
    if respuesta.lower() == "x":
      # The conversation runs in background until you call:
      conversation.end_session()
      exit()