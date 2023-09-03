FROM python:3.11-bullseye
WORKDIR /workspace

ENV PYTHONPATH /workspace:${PYTHONPATH}
ENV PATH /root/.local/bin:$PATH
ENV LD_LIBRARY_PATH /workspace/instantclient:${LD_LIBRARY_PATH}

RUN apt-get update && \
    apt-get upgrade -y && \ 
    apt-get install -y --no-install-recommends \
        poppler-utils && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

COPY pyproject.toml poetry.lock ./

RUN pip install --upgrade pip

RUN curl -sSL https://install.python-poetry.org | python - && \
    poetry config virtualenvs.create false && \
    poetry install

COPY src/ src/

CMD ["python", "-m", "src.main"]

