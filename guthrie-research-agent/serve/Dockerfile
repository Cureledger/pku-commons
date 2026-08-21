FROM python:3.11-slim

WORKDIR /app

# retrieval brain + web layer
COPY serve/requirements.txt ./requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

COPY kernel.py ./kernel.py
COPY serve/serve.py ./serve.py

# The ~40MB retrieval index (chunks.sqlite + embeddings.npy + bm25.pkl) is NOT
# in git. It is rebuilt from public sources by .github/workflows/build-index.yml
# and published as the `index-latest` GitHub Release asset; pull it in at build
# time. Run that workflow ONCE (Actions -> "Build PKU index" -> Run workflow)
# before the first deploy, or this step 404s. Override INDEX_URL to pin a build.
ARG INDEX_URL=https://github.com/Cureledger/pku-commons/releases/download/index-latest/pku_index.tar.gz
RUN python -c "import urllib.request; urllib.request.urlretrieve('$INDEX_URL', '/tmp/idx.tgz')" \
    && tar xzf /tmp/idx.tgz -C /app \
    && rm /tmp/idx.tgz \
    && test -f /app/pku_index/chunks.sqlite \
    && test -f /app/pku_index/embeddings.npy \
    && test -f /app/pku_index/bm25.pkl \
    && test -f /app/pku_index/meta.json

# bake the MiniLM weights into the image so first request is fast + offline
ENV HF_HUB_DISABLE_XET=1 HF_XET_DISABLE=1 TOKENIZERS_PARALLELISM=false \
    GUTHRIE_INDEX_DIR=/app/pku_index
RUN python -c "from sentence_transformers import SentenceTransformer; \
    SentenceTransformer('sentence-transformers/all-MiniLM-L6-v2', device='cpu')"

EXPOSE 8000
# ANTHROPIC_API_KEY is supplied at runtime (Railway secret), never baked in.
# Railway sets $PORT and railway.toml's startCommand binds uvicorn to it; this
# CMD is the local/default fallback for `docker run`.
CMD ["uvicorn", "serve:app", "--host", "0.0.0.0", "--port", "8000"]
