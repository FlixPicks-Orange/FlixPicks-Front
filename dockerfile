FROM python:3
WORKDIR /home/Docker/front
COPY requirements.txt ./
RUN python -m pip install -r requirements.txt
COPY . .
EXPOSE 2000
CMD ["python", "-u", "./app.py"]
