FROM ubuntu AS build

RUN apt-get update
RUN apt-get install -qq gcc cmake
RUN apt-get install -qq liblmdb-dev
RUN apt-get install -qq mc

WORKDIR /app
COPY . ./

RUN mkdir build && cd /app/build && cmake .. && make all
RUN cd /app/build/dist/bin && mkdir testdb

RUN chmod +x /app/build/dist/bin/iprangertest
WORKDIR /app/build/dist/bin
RUN ./iprangertest

RUN chmod +x /app/startup.sh
ENTRYPOINT ["/app/startup.sh"]