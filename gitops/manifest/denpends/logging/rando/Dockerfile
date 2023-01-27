FROM mhart/alpine-node:12

WORKDIR /app

ADD index.js index.js
ADD package.json package.json
ADD package-lock.json package-lock.json
ADD yarn.lock yarn.lock
ADD README.md README.md
ADD config/default.yaml config/default.yaml
ADD config/custom-environment-variables.yaml config/custom-environment-variables.yaml
RUN yarn

ENTRYPOINT ["yarn", "run", "start"]