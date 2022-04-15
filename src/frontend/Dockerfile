FROM node:14.16.0 as build-stage
WORKDIR /app
RUN curl -f https://get.pnpm.io/v6.16.js | node - add --global pnpm
ARG CACHEBUST=1
RUN echo "$CACHEBUST"
COPY package.json pnpm-lock.yaml ./
RUN pnpm install --frozen-lockfile --prod
COPY . .
RUN pnpm build

FROM nginx:latest as production-stage
RUN mkdir /app
RUN mkdir /app/screensaver
COPY --from=build-stage /app/dist /app
COPY --from=build-stage /app/screensaver /app/screensaver
COPY nginx.conf /etc/nginx/nginx.conf
EXPOSE 80