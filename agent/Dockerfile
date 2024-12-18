FROM pytorch/pytorch:1.12.1-cuda11.3-cudnn8-runtime

RUN apt-get -y update
RUN install --upgrade transformers
WORKDIR /restapi
COPY  requirements.txt .
RUN pip install --n-cache-dir -r requirements.txt
COPY . /restapi/
RUN chmod a+x *.sh
EXPOSE 8000
