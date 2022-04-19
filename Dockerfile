FROM python:3

EXPOSE 5000
WORKDIR /app

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY main.py /app

CMD [ "python", "./main.py" ]