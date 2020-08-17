run:pubdb
	python3 scripts/data-build.py

force:pubdb
	python3 scripts/data-build.py -f 

pubdb: scripts/data-build.py scripts/lib/utils.py data/PANDA-Papers-json.pl.json data/PANDA-Presentations-json.pl.json
	python3 scripts/pubdb_placeholder.py
	touch pubdb

links:
	./scripts/pubdb_links.py

clean:
	rm pubdb sources/*/*__pubdb.json id_id_link.json word_score_id.json
