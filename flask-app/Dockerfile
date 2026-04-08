FROM python:3.11-slim

# Why slim? Reduces image size significantly.
# Only includes minimal OS packages needed to run Python.

WORKDIR /app

# Copy requirements first — Docker layer caching means if requirements
# don't change, this layer is reused on rebuild (faster builds)
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY app.py .

EXPOSE 5000

# Use exec form (JSON array) — this makes PID 1 be Python, not a shell.
# Signals like SIGTERM reach Python directly → cleaner shutdowns.
CMD ["python", "app.py"]
