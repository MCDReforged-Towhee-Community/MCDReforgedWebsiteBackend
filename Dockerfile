FROM python:3.11

WORKDIR /MCDReforgedWebsiteBackend
COPY . /MCDReforgedWebsiteBackend

RUN pip install -r requirements.txt

EXPOSE 5000

CMD ["flask", "run", "--host=0.0.0.0"]
