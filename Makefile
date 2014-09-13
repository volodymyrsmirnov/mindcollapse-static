PYTHON_BIN := python 

freeze:
	$(PYTHON_BIN) manage.py freeze

deploy:
	cd build/
	git add .
	git commit -m "regenerated"
	ssh root@mindcollapse.com "su www-data -c \"cd /home/www/mindcollapse.com; git pull\""
