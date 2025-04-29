#!/usr/bin/env python3
import os
from azure.identity import WorkloadIdentityCredential, get_bearer_token_provider
import azure.cognitiveservices.speech as speechsdk

#
# Managed Identity only support Cognitive Services multi-service resource
# - Decision
# - Language
# - Speech
# - Vision
# - Document Intelligence
# - Metrics Advisor
#
# Not support Azure OpenAI
#

#
# Azure AI services
#
# Use Azure AI services resource instead of "Speech" single-service resource
AZURE_AI_SERVICE_REGION="japaneast"


#
# Workload Identity
#
AZURE_TENANT_ID="60c041af-d3e5-4152-a034-e8e449c34ab4"
AZURE_FEDERATED_TOKEN_FILE="4-TOKEN_FILE.jwt"

AZURE_AI_SERVICE_CLIENTID = "dada16e3-7e3e-4608-b435-4ff8d4b67e98"
cred_cognitiveservices = WorkloadIdentityCredential(
    tenant_id=AZURE_TENANT_ID,
    client_id=AZURE_AI_SERVICE_CLIENTID,
    token_file=AZURE_FEDERATED_TOKEN_FILE)

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
