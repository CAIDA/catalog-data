CATALOG_DATA_CAIDA_PATH = catalog-data-caida/sources/
CATALOG_DATA_CAIDA_FILE = data/data_id__caida.json
PUBDB_PAPER= data/pubdb_output__papers.json
PUBDB_MEDIA= data/pubdb_output__presentations.json

SUMMARY_TEMP = catalog-dataset-summary.jsonl
SUMMARY_URL = https://users.caida.org/~lpascual/catalog/catalog-dataset-summary.jsonl
SUMMARY_OPT = data/catalog-dataset-summary.jsonl

run:clean_placeholders pubdb externallinks caida build 

build:
	rm -f ${SUMMARY_TEMP}
	wget -O "${SUMMARY_TEMP}" "${SUMMARY_URL}"
	@if [ -f ${SUMMARY_TEMP} ]; then SUMMARY_OPT=${SUMMARY_TEMP}; fi
	python3 scripts/data-build.py -s ${SUMMARY_OPT}

pubdb: scripts/lib/utils.py scripts/pubdb_placeholder.py scripts/pubdb_links.py ${PUBDB_PAPER} ${PUBDB_MEDIA}
	python3 scripts/pubdb_placeholder.py -p ${PUBDB_PAPER} -m ${PUBDB_MEDIA}

externallinks: scripts/externallinks_placeholder.py
	python3 scripts/externallinks_placeholder.py -d data/data-papers.yaml

caida: scripts/caida_placeholder.py scripts/caida_dataset_blanks.py
	@if [ -d ${CATALOG_DATA_CAIDA_PATH} ]; \
		then \
		echo "python3 scripts/caida_placeholder.py -p ${CATALOG_DATA_CAIDA_PATH} -i ${CATALOG_DATA_CAIDA_FILE}"; \
		python3 scripts/caida_placeholder.py -p ${CATALOG_DATA_CAIDA_PATH} -i ${CATALOG_DATA_CAIDA_FILE} ; \
	fi; \

	@if [ ! -d ${CATALOG_DATA_CAIDA_PATH} ]; \
		then \
		echo "python3 scripts/caida_dataset_blanks.py -i ${CATALOG_DATA_CAIDA_FILE}"; \
		python3 scripts/caida_dataset_blanks.py -i ${CATALOG_DATA_CAIDA_FILE} ; \
	fi; \

# This was used to backfill historic papers and presentations
data/pubdb_links.json:
	python3 scripts/pubdb_links.py

clean: clean_placeholders
	rm -f id_id_link.json word_id_score.json

clean_placeholders:
	rm -f pubdb
	python3 scripts/remove_placeholders.py
