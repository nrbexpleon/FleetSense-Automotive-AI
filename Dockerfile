FROM python:3.12-slim
WORKDIR /app
COPY pyproject.toml README.md ./
COPY src ./src
RUN pip install --no-cache-dir .
USER 65532:65532
EXPOSE 8080
ENTRYPOINT ["fleetsense"]
CMD ["serve", "--host", "0.0.0.0", "--port", "8080"]
