FROM node
WORKDIR /srv/www
COPY package.json .
RUN npm install
COPY src .
EXPOSE 80
CMD ["node", "index.js"]
