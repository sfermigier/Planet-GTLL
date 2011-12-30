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
	rm -rf build data dist Ring.egg-info
	#rm -f test.db test/test.db

superclean: clean
	rm -rf data/* env *.egg

install:
	python setup.py install


push:
	rsync -avz -e ssh ring Makefile *.txt ring.sh ring.cfg \
		gtll@oss4cloud.org:/var/www/gtll-2.0/
