FROM kbase/sdkpython:3.8.0
MAINTAINER KBase Developer



RUN apt-get update
RUN apt-get -y install  vim

# stupid fix to remove conflict of numpy
RUN rm -rf /miniconda/lib/python3.6/site-packages/numpy*

RUN pip install --upgrade pip

RUN pip install git+https://github.com/Fxe/cobrakbase.git@76c53a3448e8f86460af285ec87eb98372b8ae2b
RUN pip install git+https://github.com/freiburgermsu/ModelSEEDpy.git@276a92a63d99eb06dcea35cd2211ed1177ba302a






COPY ./ /kb/module
RUN mkdir -p /kb/module/work
RUN chmod -R a+rw /kb/module

WORKDIR /kb/module

RUN make all

ENTRYPOINT [ "./scripts/entrypoint.sh" ]

CMD [ ]
