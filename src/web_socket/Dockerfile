FROM node:15.11.0
ENV NODE_ENV=production
WORKDIR /app
ARG CACHEBUST=1
RUN echo "$CACHEBUST"
COPY package*.json ./
RUN npm install --production
COPY . .
EXPOSE 4000
CMD [ "node", "index.js" ]