PYTHON_BIN := python 

freeze:
	$(PYTHON_BIN) manage.py freeze

deploy:
	ssh root@mindcollapse.com "su www-data -c \"cd /home/www/mindcollapse.com; git pull\""
