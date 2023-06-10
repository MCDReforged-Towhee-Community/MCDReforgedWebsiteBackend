FROM python:3.11

WORKDIR /MCDReforgedWebsiteBackend
COPY . /MCDReforgedWebsiteBackend

RUN pip install -r requirements.txt

EXPOST 5000

CMD ["python", "main.py"]
