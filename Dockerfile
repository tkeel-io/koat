FROM python:3.9.12

ENV PIPENV_DOTENV_LOCATION=/src/.dev.env
COPY . /src
WORKDIR /src


RUN pip install pipenv \
    && pipenv install \
    && rm -rf /var/lib/apt/lists/ \
    && apt-get autoremove -y && apt-get autoclean -y



CMD ["pipenv run test"]
