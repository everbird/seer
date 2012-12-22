.PHONY: help

help:
	@echo targets: version, clean, clean_pyc, clean_tmp, startweb, stopweb, restartweb, tail, tail_error, tail_all, xtail, shell

version:
	@./manage.py version

clean: clean_pyc clean_tmp
	@#@find -regex ".*\.\(pyc\|swp\|un\~\)" | xargs rm -rf

clean_pyc:
	@find `pwd` -name '*.pyc' -type f -delete

clean_tmp:
	@find `pwd` \( -name '*.swp' -o -name '*.un~' \) -type f -delete

startweb:
	@#sudo nginx -c /home/everbird/workspace/seer/nginx.conf
	@#gunicorn -c gunicorn_config.py app:app >> `./manage.py var_dir`/log/gunicorn-output-8100.log 2>&1 &
	@#gunicorn -c gunicorn_config.py deploy:application
	supervisorctl start web

stopweb:
	@#kill -QUIT `cat /home/everbird/var/8100/run/gunicorn-8100.pid` || echo -n " not running"
	@#sudo kill -QUIT `cat /home/everbird/var/8100/run/nginx-8100.pid` || echo -n " not running"
	supervisorctl stop web

restartweb:
	supervisorctl restart web
r: restartweb

status:
	supervisorctl status

tail:
	tail -n 0 -F `./manage.py var_dir`/log/seer-output-8100.log -F `./manage.py var_dir`/log/gunicorn-error-8100.log

tail_error:
	tail -n 0 -F `./manage.py var_dir`/log/*error*

tail_all:
	tail -n 0 -F `./manage.py var_dir`/log/*

xtail:
	xtail `./manage.py var_dir`/log/

shell:
	@./manage.py shell

build_var:
	@./manage.py build_var

connect_db:
	mysql -useer -pburning -Dseer_d

create_db:
	@./manage.py create_all

drop_db:
	@./manage.py drop_all

drop_db_immeditely:
	@./manage.py drop_all_immeditely

init_db:
	@./manage.py init_db

fetch_all:
	@./manage.py fetch_all

online:
	@./manage.py online

nosy:
	nosy -c tests/nosy.cfg

unittest:
	nosetests -s tests

mapping:
	@./manage.py mapping

apply:
	@./manage.py apply

douban_top:
	@./manage.py douban_top

update_douban:
	@./manage.py update_douban

requirements:
	pip install -r ./requirements.txt
