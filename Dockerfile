FROM ubuntu:20.04

RUN apt-get update -y
RUN apt-get install -y python3
RUN apt-get install -y python3-pip

COPY . /movies_wishlist
WORKDIR /movies_wishlist

RUN pip install -r requirements.txt

EXPOSE 5000

CMD ["python3", "-u", "wsgi.py"]