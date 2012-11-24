from fabric.api import hosts, run, cd, prefix
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

def vrun(cmd, env='seer'):
    remote_cmd = "/bin/bash -l -c 'source /usr/bin/virtualenvwrapper.sh" \
        + " && workon " + env \
        + " && " + cmd + "'"
    run(remote_cmd)

@hosts('rainbow')
def rebuild():
    puts('Rebuild database...')
    vrun("make drop_db_immeditely")
    vrun("make create_db")
    vrun('make init_db')
    vrun('make fetch_all')
    vrun('make online')
