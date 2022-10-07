FROM python:3.10

WORKDIR /NinjaSushi

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

RUN apt-get update \
    && apt-get install netcat -y
RUN apt-get upgrade -y

RUN python -m pip install --upgrade pip
COPY requirements.txt /NinjaSushi/
RUN pip install -r requirements.txt

COPY . /NinjaSushi/

RUN sed -i 's/\r$//g' /NinjaSushi/entrypoint.sh
RUN chmod +x /NinjaSushi/entrypoint.sh

ENTRYPOINT ["sh", "/NinjaSushi/entrypoint.sh"]

