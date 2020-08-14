run:pubdb
	python3 scripts/data-build.py

pubdb: data/PANDA-Papers-json.pl.json data/PANDA-Presentations-json.pl.json
	python3 scripts/pubdb_placeholder.py
	touch pubdb

clean:
	rm pubdb sources/*/*__pubdb.json id_id_link.json word_score_id.json
