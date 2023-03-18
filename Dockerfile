FROM python:3.11
WORKDIR /app
COPY requirements.txt ./
RUN pip3 install -r requirements.txt
COPY setup.py ./
COPY ./api_template ./api_template
RUN pip3 install .
CMD gunicorn api_template.main:app -w 4 -k uvicorn.workers.UvicornWorker -b 0.0.0.0:80
