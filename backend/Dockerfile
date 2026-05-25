FROM python:3.11-slim

# создаём пользователя (не root)
RUN useradd -m appuser

WORKDIR /app

COPY app.py .

# меняем владельца
RUN chown -R appuser:appuser /app

USER appuser

EXPOSE 8080

CMD ["python", "app.py"]



