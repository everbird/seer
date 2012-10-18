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
        run('/home/everbird/.virtualenvs/seer/bin/supervisorctl restart web')
    puts('Updated')
