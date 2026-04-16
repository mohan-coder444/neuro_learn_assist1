# Stage 1: Build
FROM node:20-slim AS build
WORKDIR /app
COPY package.json package-lock.json ./
COPY frontend/package.json ./frontend/
RUN npm install
COPY . .
RUN npm run build --prefix frontend

# Stage 2: Serve with Nginx
FROM nginx:alpine
WORKDIR /usr/share/nginx/html

# Copy built files
COPY --from=build /app/frontend/dist .

# Copy nginx template
COPY nginx.conf /etc/nginx/conf.d/config.template

# Default port to 80 if PORT is not set (e.g., local testing)
ENV PORT=80

# Use envsubst to replace ${PORT} in the template and start nginx
CMD ["/bin/sh", "-c", "envsubst '${PORT}' < /etc/nginx/conf.d/config.template > /etc/nginx/conf.d/default.conf && nginx -g 'daemon off;'"]
