ARG BASE_IMAGE=python:3.14
FROM ${BASE_IMAGE}
ARG SOURCE_COMMIT
LABEL org.opencontainers.image.revision=${SOURCE_COMMIT}
ENV PDF_CLEANUP_SOURCE_COMMIT=${SOURCE_COMMIT} \
    PDF_CLEANUP_ORIGINALS_DIR=/srv/cloud/technical-documentation/lenovo/originals \
    PYTHONDONTWRITEBYTECODE=1
COPY source /opt/pdf-cleanup/source
RUN python -m pip install --no-cache-dir /opt/pdf-cleanup/source 'pypdf[crypto,fonts]' \
    && python -m pip check
ENTRYPOINT ["pdf-cleanup"]
