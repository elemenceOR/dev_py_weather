FROM python:3.9 AS builder

WORKDIR /app

# Install dependencies
COPY requirments.txt .
RUN pip install --no-cache-dir -r requirments.txt -t /dependencies

RUN pip install gunicorn -t /dependencies

# Second stage: Create final runtime container
FROM python:3.9

WORKDIR /app

# Copy installed dependencies from the builder stage
COPY --from=builder /dependencies /usr/local/lib/python3.9/site-packages

# Copy application files
COPY app/ ./app/
COPY wsgi.py .

# Create and switch to non-root user
RUN useradd -m appuser
USER appuser

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    FLASK_APP=wsgi.py \
    FLASK_ENV=production

EXPOSE 8080

# Start the application
CMD ["python", "-m", "gunicorn", "--bind", "0.0.0.0:8000", "wsgi:app"]