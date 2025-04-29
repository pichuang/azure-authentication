#!/usr/bin/env python3
import os
import azure.cognitiveservices.speech as speechsdk

#
# Azure AI services
#
# Use Azure AI services resource instead of "Speech" single-service resource
AZURE_AI_SERVICE_REGION="japaneast"

#
# Connection String
#
# https://learn.microsoft.com/en-us/azure/service-connector/how-to-integrate-cognitive-services?tabs=dotnet#connection-string

#XXX Hard code
AZURE_AI_SERVICE_KEY=""

if AZURE_AI_SERVICE_KEY is None:
    raise ValueError("AZURE_AI_SERVICE_KEY is not set")

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
    subscription=AZURE_AI_SERVICE_KEY,
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
