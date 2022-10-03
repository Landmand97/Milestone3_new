# syntax=docker/dockerfile:1
FROM python:3.8-alpine
WORKDIR /.
COPY . .
RUN pip install -r requirements.txt
CMD ["python", "wsgi.py"]
EXPOSE 3000:3000