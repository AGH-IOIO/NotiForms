# Base image
FROM archlinux:latest as base
RUN pacman -Sy python3 python-pip --noconfirm
WORKDIR /app
COPY . .
RUN pip install -r requirements.txt

# Developement image
FROM base as dev
ENV FLASK_DEBUG=y
EXPOSE 8080
COPY --from=base /app /app
ENTRYPOINT ["python3"]
CMD ["setup.py"]
