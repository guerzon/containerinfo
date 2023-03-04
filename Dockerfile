FROM python:3.10-slim

RUN useradd appuser

WORKDIR /app

COPY . .
RUN chmod +x ./boot.sh

RUN pip install -r requirements.txt

RUN chown -R appuser:appuser /app

USER appuser
EXPOSE 5000
ENV FLASK_APP containerinfo.py
ENTRYPOINT ["./boot.sh"]
