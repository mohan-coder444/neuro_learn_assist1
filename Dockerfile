# Build Stage
FROM node:20-slim AS build
WORKDIR /app
COPY package.json package-lock.json ./
COPY frontend/package.json ./frontend/
RUN npm install
COPY . .
RUN npm run build --prefix frontend

# Production Stage
FROM node:20-slim
WORKDIR /app
RUN npm install -g serve
COPY --from=build /app/frontend/dist ./dist

# Use the dynamic Railway PORT
ENV PORT=3000
EXPOSE 3000

# We use the shell form of CMD to ensure $PORT is expanded correctly
CMD serve -s dist -l $PORT
