FROM kbase/sdkpython:3.8.0
MAINTAINER KBase Developer

RUN apt-get update
#RUN apt-get -y install  vim

# stupid fix to remove conflict of numpy
RUN rm -rf /miniconda/lib/python3.6/site-packages/numpy*

RUN pip install --upgrade pip
RUN pip install h5py
#RUN pip install numpy --python-version 3.8.10 --only-binary=:all: --dry-run

RUN pip install git+https://github.com/Freiburgermsu/modelseedpy.git@f0ea546a9c953da917c5b28e7ed23f30fe0cda0e
RUN pip install git+https://github.com/Fxe/cobrakbase.git@37029339394e1536217eb88b9f6691fc4dee0e92
#RUN pip install commscores

RUN apt-get -y install wget
RUN mkdir -p /msdb/Biochemistry && wget https://raw.githubusercontent.com/ModelSEED/ModelSEEDDatabase/master/Biochemistry/compounds.tsv -P /msdb/Biochemistry/
RUN mkdir -p /msdb/Biochemistry && wget https://raw.githubusercontent.com/ModelSEED/ModelSEEDDatabase/master/Biochemistry/reactions.tsv -P /msdb/Biochemistry/
RUN mkdir -p /msdb/Biochemistry && wget https://raw.githubusercontent.com/ModelSEED/ModelSEEDDatabase/master/Biochemistry/reactions.json -P /msdb/Biochemistry/
RUN mkdir -p /msdb/Biochemistry && wget https://raw.githubusercontent.com/ModelSEED/ModelSEEDDatabase/master/Biochemistry/compounds.json -P /msdb/Biochemistry/


RUN mkdir -p /msdb/Biochemistry/Aliases && wget https://raw.githubusercontent.com/ModelSEED/ModelSEEDDatabase/master/Biochemistry/Aliases/Unique_ModelSEED_Compound_Aliases.txt -P /msdb/Biochemistry/Aliases
RUN mkdir -p /msdb/Biochemistry/Aliases && wget https://raw.githubusercontent.com/ModelSEED/ModelSEEDDatabase/master/Biochemistry/Aliases/Unique_ModelSEED_Reaction_Aliases.txt -P /msdb/Biochemistry/Aliases
RUN mkdir -p /msdb/Biochemistry/Structures && wget https://raw.githubusercontent.com/ModelSEED/ModelSEEDDatabase/master/Biochemistry/Structures/Unique_ModelSEED_Structures.txt -P /msdb/Biochemistry/Structures
RUN mkdir -p /msdb/Biochemistry/Aliases && wget https://raw.githubusercontent.com/ModelSEED/ModelSEEDDatabase/master/Biochemistry/Aliases/Unique_ModelSEED_Compound_Names.txt -P /msdb/Biochemistry/Aliases
RUN mkdir -p /msdb/Biochemistry/Aliases && wget https://raw.githubusercontent.com/ModelSEED/ModelSEEDDatabase/master/Biochemistry/Aliases/Unique_ModelSEED_Reaction_Names.txt -P /msdb/Biochemistry/Aliases
RUN mkdir -p /msdb/Biochemistry/Aliases && wget https://raw.githubusercontent.com/ModelSEED/ModelSEEDDatabase/master/Biochemistry/Aliases/Unique_ModelSEED_Reaction_ECs.txt -P /msdb/Biochemistry/Aliases


Run touch new5
RUN pip install git+https://github.com/freiburgermsu/commscores.git@dev
RUN pip install pandas

#RUN git clone https://github.com/ModelSEED/ModelSEEDDatabase /msdb

RUN cp -r /opt/conda3/lib/python3.8/site-packages/modelseedpy/community /opt/conda3/lib/python3.8/site-packages/commscores/
RUN rm -rf /opt/conda3/lib/python3.8/site-packages/modelseedpy_freiburgermsu && cp -R  /opt/conda3/lib/python3.8/site-packages/modelseedpy/ /opt/conda3/lib/python3.8/site-packages/modelseedpy_freiburgermsu


COPY ./ /kb/module
RUN mkdir -p /kb/module/work
RUN chmod -R a+rw /kb/module

WORKDIR /kb/module

RUN make all

ENTRYPOINT [ "./scripts/entrypoint.sh" ]

CMD [ ]
