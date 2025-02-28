FROM python:3.11-alpine
RUN pip3 install requests influxdb_client python-environ
ADD collector.py /root/
CMD ["python3", "/root/collector.py"]
