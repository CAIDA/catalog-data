CATALOG_DATA_CAIDA_PATH = catalog-data-caida/sources/
PUBDB_PAPER= data/pubdb_output__papers.json
PUBDB_MEDIA= data/pubdb_output__presentations.json

REDIRECTS_FILE=data/redirects.csv

SUMMARY_URL = https://users.caida.org/~dataadm/catalog/catalog-dataset-summary.jsonl
SUMMARY_BACKUP_FILE = data/catalog-dataset-summary-backup.jsonl
SUMMARY_FILE = data/catalog-dataset-summary.jsonl

URL=https://api.catalog.caida.org/v2/graphql
IDS_FILE=data/_ids.txt

FRESH_HOURS=23

FRESH_HOUR=
START=`date -r t +%s`
END=`date +%s`
((DIFF=${START}+${END}))


###### DAta Schema files
DATA_SCHEMA_DATASETS=data/data-schema-datasets.tsv
DATA_SCHEMA_DATASETS_SRC=~/Downloads/Data\ Schema\ for\ CAIDA\ Datasets\ -\ Sheet1.tsv 
DATA_SCHEMA_CATEGORIES=data/data-schema-categories.tsv
DATA_SCHEMA_CATEGORIES_SRC=~/Downloads/Categories\ used\ in\ Schema\ for\ CAIDA\'s\ Datasets\ -\ Sheet1.tsv

#########

DATA_BUILD_OPTS=-s ${SUMMARY_FILE} -r ${REDIRECTS_FILE} -c ${DATA_SCHEMA_CATEGORIES} -d ${DATA_SCHEMA_DATASETS}

run:clean_placeholders pubdb external caida summary build suggestions

fast:
	make DATA_BUILD_OPTS="-D ${DATA_BUILD_OPTS}" run

human:readable
read:readable
readable:
	make DATA_BUILD_OPTS="-R ${DATA_BUILD_OPTS}" fast

data: build
build:
		if [ -f ${DATA_SCHEMA_DATASETS_SRC} ]; then \
			mv ${DATA_SCHEMA_DATASETS_SRC} ${DATA_SCHEMA_DATASETS} ; \
		fi
		if [ -f ${DATA_SCHEMA_CATEGORIES_SRC} ]; then \
			mv ${DATA_SCHEMA_CATEGORIES_SRC} ${DATA_SCHEMA_CATEGORIES} ; \
		fi
		echo "scripts/data-build.py ${DATA_BUILD_OPTS}"
ifneq ("$(wildcard $(CATALOG_DATA_CAIDA_PATH))","")
		python3 scripts/data-build.py ${DATA_BUILD_OPTS}
else
		./scripts/catalog-ids-download.py -O ${IDS_FILE} ${URL}
		python3 scripts/data-build.py ${DATA_BUILD_OPTS} -i ${IDS_FILE} 
endif

summary:
	python3 scripts/catalog-dataset-summary-download.py -O ${SUMMARY_FILE} -b ${SUMMARY_BACKUP_FILE} ${SUMMARY_URL}

pubdb: scripts/lib/utils.py scripts/pubdb_placeholder.py scripts/pubdb_links.py ${PUBDB_PAPER} ${PUBDB_MEDIA}
	python3 scripts/pubdb_placeholder.py -p ${PUBDB_PAPER} -m ${PUBDB_MEDIA}

external: scripts/externallinks_placeholder.py
	python3 scripts/externallinks_placeholder.py -d data/data-papers.yaml

caida: scripts/caida_placeholder.py scripts/caida_dataset_blanks.py
	@if [ -d ${CATALOG_DATA_CAIDA_PATH} ]; then \
		python3 scripts/caida_placeholder.py -p ${CATALOG_DATA_CAIDA_PATH}; \
	fi; \

suggestions: suggestions.json
suggestions.json: scripts/suggestions.py data/suggestions.json
	scripts/suggestions.py -o $@ data/suggestions.json

# This was used to backfill historic papers and presentations
data/pubdb_links.json:
	python3 scripts/pubdb_links.py



clean: clean_placeholders
	rm -f id_object.json id_id_link.json word_id_score.json category_id_depth.json ${SUMMARY_FILE} ${IDS_FILE} \
		suggestions.json category_id_score.json

clean_placeholders:
	rm -f pubdb
	python3 scripts/remove_placeholders.py
