FROM python:3.9-slim as builder
WORKDIR /build

RUN pip install --upgrade pip setuptools wheel

COPY requirements.txt /build/requirements.txt
RUN pip install --prefix=/install --no-cache-dir -r /build/requirements.txt

COPY src /build/src
RUN python -m compileall -q /build/src


FROM python:3.9-slim as runtime
WORKDIR /app

COPY --from=builder /install /usr/local

COPY --from=builder /build/src /app/src

ARG APP_USER=appuser
ARG APP_UID=1000
ARG APP_GID=1000
RUN set -eux; \
	groupadd --gid ${APP_GID} ${APP_USER} || true; \
	useradd --uid ${APP_UID} --gid ${APP_GID} --create-home --shell /bin/false ${APP_USER} || true; \
	mkdir -p /app; chown -R ${APP_USER}:${APP_USER} /app

RUN python -c "import sys, pkgutil; print('Python', sys.version)"

EXPOSE 5000

# Switch to the non-root user
USER ${APP_USER}

CMD ["gunicorn", "--bind", "0.0.0.0:5000", "--workers", "4", "--timeout", "120", "--access-logfile", "-", "--error-logfile", "-", "--log-level", "info", "src.wsgi:app"]