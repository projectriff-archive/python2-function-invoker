FROM python:2.7-slim
COPY invoker/* /
RUN  ["pip","install","-r","requirements.txt"]
ENTRYPOINT ["python","./function_invoker.py"]

