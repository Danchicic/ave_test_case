FROM python:3.13-slim
RUN pip install uv

WORKDIR /app
COPY pyproject.toml /app/

RUN uv sync

COPY src /app/src/

EXPOSE 8000

CMD ["uv", "run", "src/main.py"]

