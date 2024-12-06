FROM python:3.9-slim


WORKDIR /publish
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .

CMD ["python", "/publish/app.py"]