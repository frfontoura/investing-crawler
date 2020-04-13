FROM python:3.7.3
WORKDIR /usr/app

RUN pip install --upgrade pip
RUN pip install scrapy
RUN pip install schedule

COPY . .

CMD ["python", "main.py"]