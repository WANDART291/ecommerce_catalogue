# 1. Start with a lightweight Python Linux image
FROM python:3.11-slim

# 2. Set environment variables to keep Python clean
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# 3. Set the working directory inside the container
WORKDIR /app

# 4. Install system dependencies (needed for Postgres)
RUN apt-get update \
    && apt-get install -y gcc libpq-dev \
    && apt-get clean

# 5. Install Python dependencies
COPY requirements.txt /app/
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

# 6. Copy the rest of the project code
COPY . /app/

# 7. Default command (we will override this in docker-compose, but good to have)
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]