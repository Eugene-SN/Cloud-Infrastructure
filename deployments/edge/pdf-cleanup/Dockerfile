ARG BASE_IMAGE=python@sha256:504679006065cdab9a85e983e269140d3c5a279492395a6863b25b1ffb377f86
FROM ${BASE_IMAGE}
ARG SOURCE_COMMIT=9c9bbb375751f85ca1e6f737504f3e99a68fd3d5
LABEL org.opencontainers.image.revision=${SOURCE_COMMIT}
ENV PDF_CLEANUP_SOURCE_COMMIT=${SOURCE_COMMIT} \
    PDF_CLEANUP_ORIGINALS_DIR=/srv/cloud/technical-documentation/lenovo/originals \
    PYTHONDONTWRITEBYTECODE=1
COPY source /opt/pdf-cleanup/source
COPY runtime-requirements.txt /opt/pdf-cleanup/runtime-requirements.txt
RUN python -m pip install --no-cache-dir -r /opt/pdf-cleanup/runtime-requirements.txt \
    && python -m pip install --no-cache-dir --no-deps /opt/pdf-cleanup/source \
    && python -m pip check
ENTRYPOINT ["pdf-cleanup"]
