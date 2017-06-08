# Dockerfile

# FROM directive instructing base image to build upon
FROM python:3-onbuild


# COPY startup script into known file location in container
#COPY ./ /usr/src/app



WORKDIR /app

COPY ./ /app


RUN pip install -r /app/requirements.txt
ONBUILD RUN chmod +x start.sh

#RUN pip install --no-cache-dir -r /usr/src/app/requirements.txt
# EXPOSE port 8000 to allow communication to/from server
EXPOSE 8000

#RUN ls -la
# CMD specifcies the command to execute to start the server running.
CMD ["./start.sh"]
# done!