# IPCC Climate AI

The Streamlit interface has been replaced with a Next.js/React client and a FastAPI service.

## Local development

Start the API from this directory:

```bash
uvicorn api:app --reload --port 8080
```

Then start the web app:

```bash
cd web
npm install
NEXT_PUBLIC_API_URL=http://localhost:8080 npm run dev
```

## Cloud Run

Deploy the API using `Dockerfile.api`, then deploy `web/Dockerfile` as a separate Cloud Run service with `NEXT_PUBLIC_API_URL` set to the API service URL. Set `ALLOWED_ORIGINS` on the API to the frontend service URL. Both services use the existing Google Cloud environment variables and service account permissions.

## AR7 WG-I document pipeline

The private upload, page-aware chunking, embedding, and BigQuery retrieval
pipeline is documented in [docs/setup.md](docs/setup.md). Do not deploy the PDF
or API routes publicly while they contain confidential First Order Draft data.
