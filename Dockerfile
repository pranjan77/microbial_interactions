FROM kbase/sdkpython:3.8.0
MAINTAINER KBase Developer

RUN apt-get update
#RUN apt-get -y install  vim

# stupid fix to remove conflict of numpy
RUN rm -rf /miniconda/lib/python3.6/site-packages/numpy*

RUN pip install --upgrade pip
RUN pip install h5py

RUN pip install git+https://github.com/Freiburgermsu/modelseedpy.git@f0ea546a9c953da917c5b28e7ed23f30fe0cda0e
RUN pip install git+https://github.com/Fxe/cobrakbase.git@37029339394e1536217eb88b9f6691fc4dee0e92
#RUN pip install commscores
RUN pip install git+https://github.com/freiburgermsu/commscores.git@dev
RUN pip install pandas

COPY ./ /kb/module
RUN mkdir -p /kb/module/work
RUN chmod -R a+rw /kb/module

WORKDIR /kb/module

RUN make all

ENTRYPOINT [ "./scripts/entrypoint.sh" ]

CMD [ ]
