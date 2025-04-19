# Je pars d'une image de base 
FROM python:3.13.3-alpine

# Je crée mon répertoire de travail
WORKDIR /code

RUN apk update && apk add postgresql-dev gcc python3-dev musl-dev

# J'installe mes reqirements
COPY ./requirements.txt requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

COPY ./app app
#docker
CMD ["fastapi", "run", "app/main.py", "--port", "80", "--host", "0.0.0.0"]

#docker build -t mon-nom-image .
