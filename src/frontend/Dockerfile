FROM node:14.16.0 as build-stage
WORKDIR /app
ARG CACHEBUST=1
RUN echo "$CACHEBUST"
COPY package*.json ./
RUN npm install
COPY . .
RUN npm run build

FROM nginx:latest as production-stage
RUN mkdir /app
RUN mkdir /app/screensaver
COPY --from=build-stage /app/dist /app
COPY --from=build-stage /app/screensaver /app/screensaver
COPY nginx.conf /etc/nginx/nginx.conf
EXPOSE 80