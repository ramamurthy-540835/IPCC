# IPCC Climate AI

IPCC Climate AI is a retrieval-augmented application for exploring IPCC
reports. A FastAPI backend uses BigQuery vector search, Vertex AI embeddings,
Gemini, and documents stored in Cloud Storage. A Next.js frontend provides the
user interface.

## Local development

Copy the required configuration into your environment:

```bash
export PROJECT_ID=your-project-id
export LOCATION=us-central1
export DATASET_ID=climate_ai
export DOCUMENTS_TABLE=documents
export EMBEDDINGS_TABLE=embeddings
export BUCKET_NAME=your-unique-bucket-name
export GEMINI_MODEL=gemini-2.5-flash
export EMBEDDING_MODEL=text-embedding-005
```

Start the API:

```bash
python -m pip install -r requirements.api.txt
uvicorn api:app --reload --port 8080
```

Start the web app in another terminal:

```bash
cd web
npm install
NEXT_PUBLIC_API_URL=http://localhost:8080 npm run dev
```

## Google Cloud deployment

The scripts in `infra/` provision Cloud Storage, BigQuery, Artifact Registry,
a dedicated runtime service account, and deploy both Cloud Run services.

```bash
PROJECT_ID=ctoteam REGION=asia-south1 ./infra/provision.sh
PROJECT_ID=ctoteam REGION=asia-south1 ./infra/deploy.sh
```

The bucket defaults to `${PROJECT_ID}-ipcc-srcities`. Override
`BUCKET_NAME` if that globally unique name is already taken.
