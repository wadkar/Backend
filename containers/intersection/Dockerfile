# this dockerfile assumes build context at gocorona

FROM python:3.6

WORKDIR /gocorona

COPY containers/intersection_calculator/requirements.txt /.

COPY cli/ /cli
COPY api/ /api

#alternatively install gocorona cli using requirements.txt
# another prefered way would be to install gocorona as a package in the container

RUN pip install --no-cache-dir -r requirements.txt

