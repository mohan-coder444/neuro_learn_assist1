# Stage 1: Build
FROM node:20-slim AS build
WORKDIR /app

# Copy root and workspace configs
COPY package.json package-lock.json ./
COPY frontend/package.json ./frontend/

# Install dependencies for the whole workspace
RUN npm install

# Copy all source files
COPY . .

# Build the frontend
RUN npm run build --prefix frontend

# Stage 2: Serve with Nginx
FROM nginx:alpine
WORKDIR /usr/share/nginx/html

# Copy built files from the build stage
# Note: Vite builds to 'frontend/dist' in our setup
COPY --from=build /app/frontend/dist .

# Copy custom nginx configuration
COPY nginx.conf /etc/nginx/conf.d/default.conf

# Expose the default Nginx port
EXPOSE 80

# The Nginx start command is default
CMD ["nginx", "-g", "daemon off;"]
