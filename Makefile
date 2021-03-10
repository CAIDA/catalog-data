CATALOG_DATA_CAIDA_PATH = catalog-data-caida/sources/
CATALOG_DATA_CAIDA_FILE = data/data_id___caida.json

run:clean_placeholders scripts/data-build.py pubdb externallinks caida 
	python3 scripts/data-build.py

pubdb: scripts/lib/utils.py scripts/pubdb_placeholder.py scripts/pubdb_links.py data/PANDA-Papers-json.pl.json data/PANDA-Presentations-json.pl.json
	python3 scripts/pubdb_placeholder.py

externallinks: scripts/externallinks_placeholder.py
	python3 scripts/externallinks_placeholder.py -d data/data-papers.yaml

caida: scripts/caida_dataset_conversion.py
	@if [ -d ${CATALOG_DATA_CAIDA_PATH} ]; \
		then \
		echo "python3 scripts/caida_dataset_conversion.py -p ${CATALOG_DATA_CAIDA_PATH} -i ${CATALOG_DATA_CAIDA_FILE}"; \
		python3 scripts/caida_dataset_conversion.py -p ${CATALOG_DATA_CAIDA_PATH} -i ${CATALOG_DATA_CAIDA_FILE} ; \
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
	rm -f sources/*/*__pubdb.json id_id_link.json word_id_score.json

clean_placeholders:
	rm -f sources/*/*__pubdb.json
	rm -f sources/*/*__externallinks.json
	rm -f sources/*/*__caida.json
	rm -f sources/*/*___*.json
