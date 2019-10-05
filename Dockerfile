FROM node:12 as build-vuejs
WORKDIR /frontend
COPY package.json yarn.lock /frontend/
COPY babel.config.js /frontend/
COPY client /frontend/client
RUN yarn --dev && yarn build

FROM kennethreitz/pipenv
COPY . /app
COPY --from=build-vuejs /frontend/client/dist /app/client/dist
ENTRYPOINT ["/app/bin/docker-entrypoint"]
CMD ["server"]
