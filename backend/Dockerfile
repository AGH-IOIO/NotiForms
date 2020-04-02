# Base image
FROM archlinux:latest as base
RUN pacman -Sy python3 python-pip --noconfirm
WORKDIR /app
COPY . .
RUN pip install -r requirements.txt
WORKDIR /app/app

# Developement container
FROM base as dev

ARG FLASK_HOST=0.0.0.0
ARG FLASK_PORT=80

ENV FLASK_HOST=${FLASK_HOST}
ENV FLASK_PORT=${FLASK_PORT}
ENV FLASK_DEBUG y

EXPOSE ${FLASK_PORT}

COPY --from=base /app /app

ENTRYPOINT ["python3"]
CMD ["app.py"]
