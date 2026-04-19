FROM ubuntu:24.04
 
RUN apt-get update && apt-get install -y \
    nginx openssl tcpdump curl nano \
    && rm -rf /var/lib/apt/lists/*
 
EXPOSE 80 443
CMD ["bash"]
