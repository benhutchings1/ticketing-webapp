FROM node:12-alpine AS build

WORKDIR /frontend
COPY package*.json ./
RUN npm install
COPY . .
ENV REACT_APP_ROUTE_URL=$REACT_APP_ROUTE_URL
RUN npm run build
EXPOSE 3000
CMD ["npm", "start"]