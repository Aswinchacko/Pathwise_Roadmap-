FROM node:20-alpine

LABEL maintainer="PathWise Team"
LABEL description="Resources Service"

# Set working directory
WORKDIR /app

# Install curl for healthcheck
RUN apk add --no-cache curl

# Copy package files
COPY package*.json ./

# Install dependencies (production only)
RUN npm ci --only=production

# Copy source code
COPY . .

# Expose port
EXPOSE 8001

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
  CMD curl -f http://localhost:8001/health || exit 1

# Run the application
CMD ["node", "server.js"]

