FROM python:3.8-slim
WORKDIR orariServer
COPY . .
RUN pip install -r requirements.txt
EXPOSE 8080
CMD ["python3", "app.py"]
