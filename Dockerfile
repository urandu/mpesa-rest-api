# Dockerfile

# FROM directive instructing base image to build upon
FROM python:2-onbuild


# COPY startup script into known file location in container
#COPY ./ /usr/src/app



#RUN pip install --no-cache-dir -r /usr/src/app/requirements.txt
# EXPOSE port 8000 to allow communication to/from server
EXPOSE 8000

#RUN ls -la
# CMD specifcies the command to execute to start the server running.
CMD ["./start.sh"]
# done!