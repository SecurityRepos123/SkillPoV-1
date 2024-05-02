From python:3.11

RUN apt-get update
RUN apt-get upgrade -y

RUN pip install openai==0.28
RUN pip install spacy
RUN python -m spacy download en_core_web_sm

COPY ./code /src/

WORKDIR /src
RUN chmod +x /src/main.sh
ENTRYPOINT ["/src/main.sh"]
