.PHONY: test serve crawl run setup-env

test: env data
	PATH=env/bin:$(PATH) nosetests -v

serve: env data
	PATH=env/bin:$(PATH) python src/server.py

data: 
	mkdir data

run: serve

crawl: env
	./crawl.sh

env:
	pip install --upgrade -s -E env -r dependencies.txt

setup-env:
	pip install --upgrade -s -E env -r dependencies.txt

clean:
	find . -name "*.pyc" | xargs rm -f
	rm -f data/nuxeoorg.db
	#rm -f test.db test/test.db

superclean: clean
	rm -rf data/* env

push:
	rsync -avz -e ssh src Makefile dependencies.txt crawl.sh \
		nuxeo@styx.nuxeo.com:/var/www/home.nuxeo.org/
