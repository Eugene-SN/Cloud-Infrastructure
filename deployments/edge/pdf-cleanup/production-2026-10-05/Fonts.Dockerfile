ARG RUNTIME_IMAGE=edge/pdf-cleanup:8257cb36be78
FROM ${RUNTIME_IMAGE}
ARG SOURCE_COMMIT
LABEL org.opencontainers.image.revision=${SOURCE_COMMIT}
ENV PDF_CLEANUP_SOURCE_COMMIT=${SOURCE_COMMIT}
COPY source /opt/pdf-cleanup/source
ARG PYPDF_VERSION=6.19.0
RUN python -m pip install --no-cache-dir "pypdf[fonts]==${PYPDF_VERSION}" && python -m pip install --no-cache-dir --no-deps --force-reinstall /opt/pdf-cleanup/source && python -m pip check
