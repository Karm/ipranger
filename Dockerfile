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

RUN rm -rf ./testdb && mkdir ./testdb
RUN chmod +x /app/build/dist/bin/iprangercli

#RUN ./iprangercli /app/testing/IPRanger/test0/dataset0v4_small.txt  -c 
#RUN ./iprangercli /app/testing/IPRanger/test0/dataset0v6_small.txt  -c 
#RUN ./iprangercli /app/testing/IPRanger/test0/test0v4_small.txt  -t 
#RUN ./iprangercli /app/testing/IPRanger/test0/test0v6_small.txt  -t 

RUN ./iprangercli /app/testing/IPRanger/test2/dataset2v4_small.txt  -c 
RUN ./iprangercli /app/testing/IPRanger/test2/dataset2v6_small.txt  -c 
RUN ./iprangercli /app/testing/IPRanger/test2/test2v4_small.txt  -t 
RUN ./iprangercli /app/testing/IPRanger/test2/test2v6_small.txt  -t 

RUN chmod +x /app/startup.sh
ENTRYPOINT ["/app/startup.sh"]
