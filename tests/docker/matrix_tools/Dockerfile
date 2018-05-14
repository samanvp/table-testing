FROM ubuntu:18.04

RUN apt-get update \
 && apt-get install -y python3-pip

RUN pip3 install h5py \
                 feather-format \
                 loompy \
                 pyarrow \
                 scanpy
