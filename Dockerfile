FROM kbase/sdkpython:3.8.0
MAINTAINER KBase Developer
RUN apt-get update -y
RUN apt-get -y install  vim wget
RUN pip install --upgrade pip
RUN pip install numpy==1.24.4 h5py==3.10.0 pandas==2.0.3

RUN pip install git+https://github.com/Freiburgermsu/modelseedpy.git@f0ea546a9c953da917c5b28e7ed23f30fe0cda0e
RUN pip install git+https://github.com/Fxe/cobrakbase.git@37029339394e1536217eb88b9f6691fc4dee0e92

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



RUN pip install git+https://github.com/freiburgermsu/commscores.git@e921a529d2144560882d6d2c9028401f4254b899
RUN pip install pandas

RUN cp -r /opt/conda3/lib/python3.8/site-packages/modelseedpy/community /opt/conda3/lib/python3.8/site-packages/commscores/
RUN rm -rf /opt/conda3/lib/python3.8/site-packages/modelseedpy_freiburgermsu && cp -R  /opt/conda3/lib/python3.8/site-packages/modelseedpy/ /opt/conda3/lib/python3.8/site-packages/modelseedpy_freiburgermsu

RUN touch new
RUN pip uninstall -y cobrakbase
RUN pip install git+https://github.com/cshenry/cobrakbase.git@525409070d11fc1efd8fe5daf9069fd519d563c2






COPY ./ /kb/module
RUN mkdir -p /kb/module/work
RUN chmod -R a+rw /kb/module
WORKDIR /kb/module
RUN make all
ENTRYPOINT [ "./scripts/entrypoint.sh" ]
CMD [ ]
