.PHONY: test serve crawl run setup-env install

test: env data
	PATH=env/bin:$(PATH) nosetests -v

serve: env data
	./ring.sh serve

run: serve

crawl: env data
	./ring.sh crawl

data: 
	mkdir data

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

install:
	python setup.py install


push:
	rsync -avz -e ssh src Makefile *.txt crawl.sh ring.cfg \
		gtll@oss4cloud.org:/var/www/gtll-2.0/
