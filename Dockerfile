FROM kennethreitz/pipenv
ENV PORT '80'
COPY . /app
CMD python3 app.py
EXPOSE 80

