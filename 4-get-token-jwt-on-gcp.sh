TOKEN_FILE=/var/run/secrets/azure.jwt
curl -H "Metadata-Flavor: Google" \
  "http://metadata/computeMetadata/v1/instance/service-accounts/default/identity?audience=api://AzureADTokenExchange&format=full" \
  -o "$TOKEN_FILE"