FROM public.ecr.aws/amazonlinux/amazonlinux:2

ENV PATH=/usr/local/bin:$PATH \
    LC_ALL=C.UTF-8 \
    LANG=C.UTF-8 \
    PYTHONDONTWRITEBYTECODE=1

EXPOSE 8000
WORKDIR /srv
COPY . /srv

RUN amazon-linux-extras enable python3.8 -y \
    && yum install -y \
           which \
           python38 \
           postgresql-devel \
           python38-devel \
           gcc \
    && python3.8 -m pip install pip --upgrade \
    && ln -s /usr/local/bin/pip3 /usr/bin/pip3 \
    && ln -s /usr/bin/pydoc3.8 /usr/local/bin/pydoc \
    && ln -s /usr/bin/python3.8 /usr/local/bin/python \
    && ln -s /usr/bin/python3.8-config /usr/local/bin/python-config \
    && yum -y clean all --enablerepo='*'

RUN pip3 install pipenv
RUN PIPENV_VENV_IN_PROJECT=1 pipenv --python 3.8 install --deploy

ENV PATH="/.venv/bin:$PATH" \
    DB_USER=postgres \
    DB_PASS=supersecret \
    DB_HOST=postgres \
    DB_PORT=5432 \
    DB_DB=postgres

CMD ["pipenv", "run", "python", "./app.py"]
