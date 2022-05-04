CATALOG_DATA_CAIDA_PATH = catalog-data-caida/sources/
PUBDB_PAPER= data/pubdb_output__papers.json
PUBDB_MEDIA= data/pubdb_output__presentations.json

SUMMARY_URL = https://users.caida.org/~lpascual/catalog/catalog-dataset-summary.jsonl
SUMMARY_LOCAL_FILE = data/catalog-dataset-summary.jsonl
SUMMARY_FILE = data/_catalog-dataset-summary.jsonl

URL=https://api.catalog.caida.org/v1
IDS_FILE=data/_ids.txt

FRESH_HOURS=23

FRESH_HOUR=
START=`date -r t +%s`
END=`date +%s`
((DIFF=${START}+${END}))


run:clean_placeholders pubdb externallinks caida summary scripts/data-build.py
ifneq ("$(wildcard $(CATALOG_DATA_CAIDA_PATH))","")
		python3 scripts/data-build.py -s ${SUMMARY_FILE}
else
		./scripts/catalog_ids_download.py -O ${IDS_FILE} ${URL}
		python3 scripts/data-build.py -i ${IDS_FILE} -s ${SUMMARY_FILE}
endif

summary:
	python3 scripts/catalog-dataset-summary-download.py -O ${SUMMARY_FILE} -l ${SUMMARY_LOCAL_FILE} ${SUMMARY_URL}

pubdb: scripts/lib/utils.py scripts/pubdb_placeholder.py scripts/pubdb_links.py ${PUBDB_PAPER} ${PUBDB_MEDIA}
	python3 scripts/pubdb_placeholder.py -p ${PUBDB_PAPER} -m ${PUBDB_MEDIA}

externallinks: scripts/externallinks_placeholder.py
	python3 scripts/externallinks_placeholder.py -d data/data-papers.yaml

caida: scripts/caida_placeholder.py scripts/caida_dataset_blanks.py
	@if [ -d ${CATALOG_DATA_CAIDA_PATH} ]; then \
		python3 scripts/caida_placeholder.py -p ${CATALOG_DATA_CAIDA_PATH}; \
	fi; \

# This was used to backfill historic papers and presentations
data/pubdb_links.json:
	python3 scripts/pubdb_links.py

clean: clean_placeholders
	rm -f id_object.json id_id_link.json word_id_score.json ${SUMMARY_FILE} ${IDS_FILE}

clean_placeholders:
	rm -f pubdb
	python3 scripts/remove_placeholders.py
