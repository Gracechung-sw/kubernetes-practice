FROM node:10

COPY  . .

RUN npm install

CMD ["node", "src/red-app.js"]