from fabric.api import hosts, run, cd
from fabric.utils import puts

@hosts('rainbow')
def host_type():
    run('uname -s')

@hosts('rainbow')
def update():
    puts('Update seer...')
    with cd('/home/everbird/product/seer'):
        run('git pull')
        run('/home/everbird/.virtualenvs/seer/bin/pip install -r requirements.txt')
        run('/home/everbird/.virtualenvs/seer/bin/supervisorctl restart web')
    puts('Updated')

@hosts('rainbow')
def rebuild():
    puts('Rebuild database...')
    run('cd /home/everbird/product/seer'
            ' && make drop_db_immeditely'
            ' && make create_db'
            ' && make init_db'
            ' && make fetch_all'
            ' && make online')
