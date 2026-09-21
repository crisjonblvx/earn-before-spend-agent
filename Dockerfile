FROM python:3.12-slim
WORKDIR /app
COPY *.py ./
USER nobody
EXPOSE 8000
CMD ["python", "judge_demo.py"]
