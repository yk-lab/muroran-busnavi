# build
FROM node:11 as build-env
COPY . /app
WORKDIR /app
RUN yarn && yarn webpack

FROM kennethreitz/pipenv
ENV PORT '80'
COPY --from=build-env /app/pages /app/pages
COPY --from=build-env /app/static/dist /app/static/dist
COPY --from=build-env /app/static/font /app/static/font
COPY --from=build-env /app/static/img /app/static/img
COPY --from=build-env /app/templates /app/templates
COPY --from=build-env /app/*.py /app/
COPY --from=build-env /app/Pipfile* /app/
CMD python3 app.py
EXPOSE 80
