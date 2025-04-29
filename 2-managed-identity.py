#!/usr/bin/env python3
import os
from azure.identity import ManagedIdentityCredential, get_bearer_token_provider
import azure.cognitiveservices.speech as speechsdk

#
# Azure AI services
#
# Use Azure AI services resource instead of "Speech" single-service resource
AZURE_AI_SERVICE_REGION="japaneast"


#
# Managed Identity
# !!!! Only work on Azure Environment due to IMDS !!!!
#
# Ref: https://learn.microsoft.com/en-us/azure/service-connector/how-to-integrate-cognitive-services?tabs=python#user-assigned-managed-identity
AZURE_AI_SERVICE_CLIENTID = "dada16e3-7e3e-4608-b435-4ff8d4b67e98"
cred_cognitiveservices = ManagedIdentityCredential(client_id=AZURE_AI_SERVICE_CLIENTID)

token_provider = get_bearer_token_provider(
    cred_cognitiveservices, "https://cognitiveservices.azure.com/.default"
)

access_token = token_provider()

#
# Azure Speech
#
# Assign Cognitive Services User role to Managed Identity
# https://learn.microsoft.com/en-us/azure/ai-services/speech-service/role-based-access-control
#
# -----------------------------
# Example: Text-to-Speech (TTS)
# -----------------------------

speech_config = speechsdk.SpeechConfig(
    auth_token=access_token,
    region=AZURE_AI_SERVICE_REGION
)

# Optional: set voice & output format
speech_config.speech_synthesis_voice_name = "en-US-JennyNeural"

# Use default speaker on local machine
audio_config = speechsdk.audio.AudioOutputConfig(use_default_speaker=True)

synthesizer = speechsdk.SpeechSynthesizer(speech_config=speech_config, audio_config=audio_config)

print("Synthesizing... (this will play through system speaker)")
result = synthesizer.speak_text_async("Hello from Azure Speech using Managed Identity.").get()

if result.reason == speechsdk.ResultReason.SynthesizingAudioCompleted:
    print(" ===== Speech synthesis succeeded =====")
else:
    print(" ===== Speech synthesis failed =====:", result.reason)
