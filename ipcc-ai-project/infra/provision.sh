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
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

for command in gcloud bq; do
  if ! command -v "${command}" >/dev/null 2>&1; then
    echo "Required command not found: ${command}" >&2
    exit 1
  fi
done

gcloud projects describe "${PROJECT_ID}" >/dev/null
gcloud config set project "${PROJECT_ID}" >/dev/null

gcloud services enable \
  aiplatform.googleapis.com \
  artifactregistry.googleapis.com \
  bigquery.googleapis.com \
  cloudbuild.googleapis.com \
  iam.googleapis.com \
  run.googleapis.com \
  storage.googleapis.com

if ! gcloud storage buckets describe "gs://${BUCKET_NAME}" >/dev/null 2>&1; then
  gcloud storage buckets create "gs://${BUCKET_NAME}" \
    --location="${REGION}" \
    --uniform-bucket-level-access
fi

if ! bq --project_id="${PROJECT_ID}" show "${PROJECT_ID}:${DATASET_ID}" >/dev/null 2>&1; then
  bq --project_id="${PROJECT_ID}" \
    --location="${REGION}" \
    mk --dataset "${PROJECT_ID}:${DATASET_ID}"
fi

if ! bq --project_id="${PROJECT_ID}" show "${PROJECT_ID}:${DATASET_ID}.${DOCUMENTS_TABLE}" >/dev/null 2>&1; then
  bq --project_id="${PROJECT_ID}" mk --table \
    "${PROJECT_ID}:${DATASET_ID}.${DOCUMENTS_TABLE}" \
    "${SCRIPT_DIR}/schemas/documents.json"
fi

if ! bq --project_id="${PROJECT_ID}" show "${PROJECT_ID}:${DATASET_ID}.${EMBEDDINGS_TABLE}" >/dev/null 2>&1; then
  bq --project_id="${PROJECT_ID}" mk --table \
    "${PROJECT_ID}:${DATASET_ID}.${EMBEDDINGS_TABLE}" \
    "${SCRIPT_DIR}/schemas/embeddings.json"
fi

if ! gcloud artifacts repositories describe "${REPOSITORY}" \
  --location="${REGION}" >/dev/null 2>&1; then
  gcloud artifacts repositories create "${REPOSITORY}" \
    --repository-format=docker \
    --location="${REGION}" \
    --description="IPCC Climate AI container images"
fi

if ! gcloud iam service-accounts describe "${SERVICE_ACCOUNT_EMAIL}" >/dev/null 2>&1; then
  gcloud iam service-accounts create "${SERVICE_ACCOUNT_NAME}" \
    --display-name="IPCC Climate AI runtime"
fi

for role in \
  roles/aiplatform.user \
  roles/bigquery.dataEditor \
  roles/bigquery.jobUser \
  roles/artifactregistry.reader; do
  gcloud projects add-iam-policy-binding "${PROJECT_ID}" \
    --member="serviceAccount:${SERVICE_ACCOUNT_EMAIL}" \
    --role="${role}" \
    --condition=None \
    --quiet >/dev/null
done

gcloud storage buckets add-iam-policy-binding "gs://${BUCKET_NAME}" \
  --member="serviceAccount:${SERVICE_ACCOUNT_EMAIL}" \
  --role=roles/storage.objectViewer \
  --quiet >/dev/null

echo "Provisioning complete."
echo "Project: ${PROJECT_ID}"
echo "Region: ${REGION}"
echo "Bucket: gs://${BUCKET_NAME}"
echo "Dataset: ${PROJECT_ID}:${DATASET_ID}"
echo "Artifact Registry: ${REGION}-docker.pkg.dev/${PROJECT_ID}/${REPOSITORY}"
echo "Runtime service account: ${SERVICE_ACCOUNT_EMAIL}"
