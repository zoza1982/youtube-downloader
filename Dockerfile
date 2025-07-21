# Use Python slim image for smaller size
FROM python:3.11-slim

# Install system dependencies including ffmpeg
RUN apt-get update && apt-get install -y \
    ffmpeg \
    git \
    && rm -rf /var/lib/apt/lists/*

# Set working directory
WORKDIR /app

# Copy requirements first for better caching
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the entire project
COPY . .

# Install the package
RUN pip install --no-cache-dir -e .

# Create downloads directory
RUN mkdir -p /downloads

# Set downloads as default volume
VOLUME ["/downloads"]

# Create a non-root user to run the application
RUN useradd -m -u 1000 ytduser && \
    chown -R ytduser:ytduser /app /downloads

# Switch to non-root user
USER ytduser

# Copy entrypoint script
COPY --chown=ytduser:ytduser docker-entrypoint.sh /usr/local/bin/
RUN chmod +x /usr/local/bin/docker-entrypoint.sh

# Set default working directory for commands
WORKDIR /downloads

# Use custom entrypoint for better UX
ENTRYPOINT ["/usr/local/bin/docker-entrypoint.sh"]

# Default to no command (will show interactive prompt)
CMD []