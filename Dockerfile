# Use an official Python runtime as a parent image
FROM alpine:3.19

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Set working directory
WORKDIR /app

RUN apk update && apk add --no-cache \
    python3 \
    py3-pip


# Install dependencies
RUN python -m venv venv

COPY requirements.txt /app/
RUN  . venv/bin/activate && pip install -r requirements.txt

# Copy project files
COPY . /app/

# Expose port 8000
EXPOSE 8000

# Run migrations and start the Django development server
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
