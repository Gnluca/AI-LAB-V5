FROM pytorch/pytorch:latest

RUN pip install fastapi uvicorn

COPY . /workspace/project

WORKDIR /workspace/project

CMD ["uvicorn","train:app","--host","0.0.0.0","--port","8001"]