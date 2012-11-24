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
    with cd('/home/everbird/product/seer'):
        run('make drop_db')
        run('make create_db')
        run('make init_db')
        run('make fetch_all')
        run('make online')
