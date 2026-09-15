#!/usr/bin/env bash
set -euo pipefail

PROJECT_ID="${PROJECT_ID:-ctoteam}"
REGION="${REGION:-asia-south1}"
BUCKET_NAME="${BUCKET_NAME:-${PROJECT_ID}-ipcc-srcities}"
DATASET_ID="${DATASET_ID:-climate_ai}"
DOCUMENTS_TABLE="${DOCUMENTS_TABLE:-documents}"
EMBEDDINGS_TABLE="${EMBEDDINGS_TABLE:-embeddings}"
REPOSITORY="${REPOSITORY:-ipcc-ai}"
SERVICE_ACCOUNT_NAME="${SERVICE_ACCOUNT_NAME:-ipcc-ai-runtime}"
SERVICE_ACCOUNT_EMAIL="${SERVICE_ACCOUNT_NAME}@${PROJECT_ID}.iam.gserviceaccount.com"
API_SERVICE="${API_SERVICE:-ipcc-ai-api}"
WEB_SERVICE="${WEB_SERVICE:-ipcc-ai-web}"
GEMINI_MODEL="${GEMINI_MODEL:-gemini-2.5-flash}"
EMBEDDING_MODEL="${EMBEDDING_MODEL:-text-embedding-005}"
API_IMAGE="${REGION}-docker.pkg.dev/${PROJECT_ID}/${REPOSITORY}/api:latest"
WEB_IMAGE="${REGION}-docker.pkg.dev/${PROJECT_ID}/${REPOSITORY}/web:latest"
REPO_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"

gcloud projects describe "${PROJECT_ID}" >/dev/null

gcloud builds submit "${REPO_ROOT}" \
  --project="${PROJECT_ID}" \
  --config="${REPO_ROOT}/infra/cloudbuild.api.yaml" \
  --substitutions="_IMAGE=${API_IMAGE}"

gcloud run deploy "${API_SERVICE}" \
  --project="${PROJECT_ID}" \
  --region="${REGION}" \
  --image="${API_IMAGE}" \
  --service-account="${SERVICE_ACCOUNT_EMAIL}" \
  --allow-unauthenticated \
  --set-env-vars="PROJECT_ID=${PROJECT_ID},LOCATION=${REGION},DATASET_ID=${DATASET_ID},DOCUMENTS_TABLE=${DOCUMENTS_TABLE},EMBEDDINGS_TABLE=${EMBEDDINGS_TABLE},BUCKET_NAME=${BUCKET_NAME},GEMINI_MODEL=${GEMINI_MODEL},EMBEDDING_MODEL=${EMBEDDING_MODEL},TOP_K=5,EMBEDDING_BATCH_SIZE=25" \
  --memory=1Gi \
  --timeout=300

API_URL="$(gcloud run services describe "${API_SERVICE}" \
  --project="${PROJECT_ID}" \
  --region="${REGION}" \
  --format='value(status.url)')"

gcloud builds submit "${REPO_ROOT}/web" \
  --project="${PROJECT_ID}" \
  --config="${REPO_ROOT}/infra/cloudbuild.web.yaml" \
  --substitutions="_IMAGE=${WEB_IMAGE},_API_URL=${API_URL}"

gcloud run deploy "${WEB_SERVICE}" \
  --project="${PROJECT_ID}" \
  --region="${REGION}" \
  --image="${WEB_IMAGE}" \
  --allow-unauthenticated \
  --memory=512Mi

WEB_URL="$(gcloud run services describe "${WEB_SERVICE}" \
  --project="${PROJECT_ID}" \
  --region="${REGION}" \
  --format='value(status.url)')"

gcloud run services update "${API_SERVICE}" \
  --project="${PROJECT_ID}" \
  --region="${REGION}" \
  --update-env-vars="ALLOWED_ORIGINS=${WEB_URL}" >/dev/null

echo "Deployment complete."
echo "Web: ${WEB_URL}"
echo "API: ${API_URL}"
