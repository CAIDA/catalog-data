CATALOG_DATA_CAIDA_PATH = catalog-data-caida/sources/
PUBDB_PAPER= data/pubdb_output__papers.json
PUBDB_MEDIA= data/pubdb_output__presentations.json

SUMMARY_DATA_FILE = data/catalog-dataset-summary.jsonl
SUMMARY_URL = https://users.caida.org/~lpascual/catalog/catalog-dataset-summary.jsonl
SUMMARY_TEMP = _catalog-dataset-summary.jsonl
SUMMARY_FILE = catalog-dataset-summary.jsonl

URL=https://api.catalog.caida.org/v1
IDS_FILE=data/ids.txt

START=`date -r t +%s`
END=`date +%s`
((DIFF=${START}+${END}))


run:clean_placeholders pubdb externallinks caida summary scripts/data-build.py
	echo "$(wildcard ${CATALOG_DATA_CAIDA_PATH})"
ifneq ("$(wildcard $(CATALOG_DATA_CAIDA_PATH))","")
		python3 scripts/data-build.py -s ${SUMMARY_FILE}
else
		./scripts/catalog_ids_download.py -O ${IDS_FILE} ${URL}
		python3 scripts/data-build.py -i ${IDS_FILE} -s ${SUMMARY_FILE}
endif

summary:
	@ # remove the file if it older then 1 day
	@ if [ -f ${SUMMARY_FILE} ]; then \
		find "${SUMMARY_FILE}" -type f -mtime +1d -delete ; \
	fi

	@ # if the file doesn't exist download it 
	@ if [ ! -f ${SUMMARY_FILE} ]; then \
		cp "${SUMMARY_DATA_FILE}" "${SUMMARY_FILE}"; \
		wget -O "${SUMMARY_TEMP}" "${SUMMARY_URL}"; \
	fi

	@ # If the file was successfully downloaded, use it
	@if [ -f ${SUMMARY_TEMP} ]; then \
		mv ${SUMMARY_TEMP} ${SUMMARY_FILE}; \
		touch "${SUMMARY_FILE}"; \
	fi


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
	rm -f id_object.json id_id_link.json word_id_score.json ${SUMMARY_FILE}

clean_placeholders:
	rm -f pubdb
	python3 scripts/remove_placeholders.py
