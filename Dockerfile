FROM python:3.10.9-slim

# ## allows for log messages to be immediately dumped to the stream instead of being buffered
# ENV PYTHONUNBUFFERED=1

COPY ./src ./app/src
COPY ./ml ./app/ml
COPY ./alembic ./app/alembic
# Copying multiple files into `/app/`
COPY ./requirements.txt ./.env ./entrypoint.sh /app/

WORKDIR /app
RUN chmod +x entrypoint.sh


RUN python3 -m venv /opt/venv && /opt/venv/bin/python -m pip install --no-cache-dir -r requirements.txt

# for Open-CV
RUN apt-get update && apt-get install -y --no-install-recommends \
    libgl1-mesa-glx \
    libglib2.0-0 && \
    rm -rf /var/lib/apt/lists/*

# Minimize image size 
RUN (apt-get autoremove -y; \
    apt-get autoclean -y) 

EXPOSE 8000
CMD [ "./entrypoint.sh" ]
