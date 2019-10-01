FROM node:alpine as builder

WORKDIR /app


COPY ./package.json .

RUN npm install

COPY . .

RUN rm -rf node_modules/sharp

RUN npm install sharp 

RUN npm install -g gatsby-cli 


RUN npm run build

# Serve the built
FROM nginx:alpine

EXPOSE 80

COPY --from=builder /app/build /usr/share/nginx/html