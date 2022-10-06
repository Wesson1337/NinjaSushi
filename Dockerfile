FROM python:3.10

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /NinjaSushi
RUN python -m pip install --upgrade pip
COPY requirements.txt /NinjaSushi/
RUN pip install -r requirements.txt
COPY . /NinjaSushi/

