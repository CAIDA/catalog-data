run:pubdb caida
	python3 scripts/data-build.py

pubdb: scripts/lib/utils.py scripts/pubdb_placeholder.py scripts/pubdb_links.py data/PANDA-Papers-json.pl.json data/PANDA-Presentations-json.pl.json
	python3 scripts/pubdb_placeholder.py
	touch pubdb

caida: scripts/caida_dataset_conversion.py
	python3 scripts/caida_dataset_conversion.py -p ../catalog-data-caida/sources/

# This was used to backfill historic papers and presentations
data/pubdb_links.json:
	python3 scripts/pubdb_links.py

clean:
	rm pubdb sources/*/*__pubdb.json id_id_link.json word_id_score.json
	rm sources/*/*__caida.json
