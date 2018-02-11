FROM django:onbuild

WORKDIR /usr/src/app
COPY codes/ .

EXPOSE 8000
CMD ["python", "-u", "manage.py", "migrate"]
