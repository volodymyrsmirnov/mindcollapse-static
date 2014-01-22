PYTHON_BIN := virtualenv/bin/python 

freeze:
	$(PYTHON_BIN) manage.py freeze

deploy: freeze
	cd build/
	git add .
	git commit -m "regenerated"
	git push
	ssh root@mindcollapse.com "su www-data -c \"cd /home/www/mindcollapse.com; git pull\""
