# syntax=docker/dockerfile:1.7

FROM python:3.12.7-slim AS builder

ENV PIP_DISABLE_PIP_VERSION_CHECK=1 \
    PIP_NO_CACHE_DIR=1 \
    PYTHONDONTWRITEBYTECODE=1

WORKDIR /build
RUN pip install --upgrade pip build

COPY pyproject.toml README.md LICENSE ./
COPY src ./src
RUN python -m build --wheel --outdir /dist

FROM python:3.12.7-slim AS runtime

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

RUN useradd --create-home --uid 10001 app
USER app
WORKDIR /home/app

COPY --from=builder /dist/*.whl /tmp/
RUN pip install --user /tmp/*.whl && rm /tmp/*.whl

ENV PATH="/home/app/.local/bin:${PATH}"

ENTRYPOINT ["docsmoke"]
CMD ["--help"]

