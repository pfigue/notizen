# Container

Using [this](https://hub.docker.com/r/library/elasticsearch/) with:

  docker pull elasticsearch

Running it with:

  sudo docker run -p 127.0.0.1:9200:9200 -v "~/.config/notizen/esdata":/usr/share/elasticsearch/data -it elasticsearch:latest

with permanent storage in `~/.config/notizen/esdata`.

