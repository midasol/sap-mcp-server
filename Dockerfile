# Multi-stage build for SAP MCP Server
FROM python:3.11-slim as builder

# Set build arguments
ARG BUILD_DATE
ARG VERSION
ARG VCS_REF

# Set labels
LABEL maintainer="SAP MCP Team <sap-mcp@company.com>" \
      org.label-schema.build-date=$BUILD_DATE \
      org.label-schema.name="sap-mcp-server" \
      org.label-schema.description="SAP Gateway MCP Server" \
      org.label-schema.version=$VERSION \
      org.label-schema.vcs-ref=$VCS_REF \
      org.label-schema.vcs-url="https://github.com/company/sap-mcp" \
      org.label-schema.schema-version="1.0"

# Install system dependencies for building
RUN apt-get update && apt-get install -y \
    build-essential \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Set work directory
WORKDIR /app

# Copy requirements first for better caching
COPY requirements.txt .

# Install Python dependencies
RUN pip install --user --no-cache-dir --upgrade pip && \
    pip install --user --no-cache-dir -r requirements.txt

# Production stage
FROM python:3.11-slim

# Install runtime dependencies
RUN apt-get update && apt-get install -y \
    curl \
    ca-certificates \
    && rm -rf /var/lib/apt/lists/* \
    && update-ca-certificates

# Create non-root user
RUN groupadd -r sapmcp && useradd -r -g sapmcp -s /bin/false sapmcp

# Set work directory
WORKDIR /app

# Copy Python dependencies from builder stage
COPY --from=builder /root/.local /home/sapmcp/.local

# Copy application code
COPY src/ .

# Create necessary directories and set permissions
RUN mkdir -p /app/logs /app/data && \
    chown -R sapmcp:sapmcp /app

# Set environment variables
ENV PATH=/home/sapmcp/.local/bin:$PATH \
    PYTHONPATH=/app \
    PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    MCP_PORT=8000 \
    MCP_HOST=0.0.0.0

# Switch to non-root user
USER sapmcp

# Expose port
EXPOSE 8000

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:8000/health || exit 1

# Run the application
CMD ["python", "-m", "sap_mcp.server"]