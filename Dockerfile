FROM python:3.10.9-slim

# ## allows for log messages to be immediately dumped to the stream instead of being buffered
# ENV PYTHONUNBUFFERED=1

COPY ./src ./app/src
# Copying multiple files into `/app/`
COPY ./requirements.txt ./.env ./entrypoint.sh /app/

WORKDIR /app
RUN chmod +x entrypoint.sh


RUN python3 -m venv /opt/venv && /opt/venv/bin/python -m pip install -r requirements.txt

EXPOSE 8000
CMD [ "./entrypoint.sh" ]
