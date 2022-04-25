FROM python:3

EXPOSE 5000
WORKDIR /app

COPY requirements.txt  /app
RUN python -m pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt

COPY . .
#ENTRYPOINT [ "/bin/bash", "entrypoint.sh" ]
CMD python main.py
