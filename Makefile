run:pubdb
	python3 scripts/data-build.py

force:pubdb
	python3 scripts/data-build.py -f 

pubdb: scripts/pubdb_placeholder.py scripts/pubdb_links.py data/PANDA-Papers-json.pl.json data/PANDA-Presentations-json.pl.json
	python3 scripts/pubdb_placeholder.py
	python3 scripts/pubdb_links.py
	touch pubdb

links:

clean:
	rm pubdb sources/*/*__pubdb.json id_id_link.json word_score_id.json
