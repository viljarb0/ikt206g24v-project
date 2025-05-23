# Use official Python image
FROM python:3.11

# Set working directory
WORKDIR /exam

# Copy project files
COPY . .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Expose port
EXPOSE 5000

# Run Gunicorn server
#CMD ["gunicorn", "-w", "4", "-b", "0.0.0.0:5000", "app:app"]
CMD ["./entrypoint"]
