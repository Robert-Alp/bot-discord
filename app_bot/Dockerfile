FROM python:3.13.3-slim

WORKDIR /code_bot

RUN apt-get update && apt-get install -y gcc python3-dev

COPY ./requirements.txt requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

COPY ./bot bot

CMD ["python", "bot/v3.py"]