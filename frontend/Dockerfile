# syntax=docker/dockerfile:1
FROM node:20

ENV NODE_ENV=development \
    NG_CLI_ANALYTICS=false

WORKDIR /app

COPY telcox-dashboard/package*.json ./
RUN npm install

COPY telcox-dashboard/ ./

EXPOSE 4200

CMD ["npm", "run", "start", "--", "--host", "0.0.0.0", "--port", "4200"]
