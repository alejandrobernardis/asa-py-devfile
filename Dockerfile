FROM registry.redhat.io/rhel9/python-311:1-41 AS base
ARG UID=1001
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PYTHONHASHSEED=random \
    PIP_DEFAULT_TIMEOUT=100 \
    PIP_DISABLE_PIP_VERSION_CHECK=on

USER 0
COPY --chown=${UID}:0 . .

USER ${UID}
RUN python -m pip install --upgrade --no-cache-dir poetry \
  && poetry export --no-interaction --no-ansi \
    --format requirements.txt --output ./requirements.txt \
  && pip wheel --no-cache-dir --wheel-dir ./wheels -r ./requirements.txt


FROM quay.io/sclorg/python-311-minimal-el8 AS image
ARG UID=1001
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PYTHONHASHSEED=random \
    PIP_DEFAULT_TIMEOUT=100 \
    PIP_DISABLE_PIP_VERSION_CHECK=on

USER 0
COPY --chown=${UID}:0 --from=base /opt/app-root/src/src .
COPY --chown=${UID}:0 --from=base /opt/app-root/src/wheels ../wheels

USER ${UID}
RUN pip install --no-cache ../wheels/* && rm -fr ../wheels

CMD ["python", "-m", "service"]
