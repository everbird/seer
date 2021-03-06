from fabric.api import hosts, run, cd
from fabric.operations import local
from fabric.utils import puts

@hosts('rainbow')
def host_type():
    run('uname -s')

@hosts('rainbow')
def update():
    puts('Update seer...')
    with cd('/home/everbird/product/seer'):
        run('git pull')
        run('/home/everbird/.virtualenvs/product-seer/bin/pip install -r requirements.txt')
        vrun('python gen.py product')
        vrun('make create_db')
        run('/home/everbird/.virtualenvs/product-seer/bin/supervisorctl restart web')
    puts('Updated')

def vrun(cmd, env='product-seer'):
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

@hosts('rainbow')
def mapping():
    puts('Upgrade mapping...')
    vrun("make mapping")

@hosts('rainbow')
def apply():
    puts('Upgrade mapping...')
    vrun("make apply")

@hosts('rainbow')
def restart():
    puts('Restarting ...')
    vrun("make restart")

@hosts('rainbow')
def douban_top():
    puts('Updating douban top250 infomation...')
    vrun('make douban_top')

@hosts('rainbow')
def update_douban():
    puts('Updating mapped douban infomation...')
    vrun('make update_douban')

@hosts('rainbow')
def package():
    puts('Start packaging ...')
    vrun('make package')

@hosts('rainbow')
def gen():
    puts('Generating config files...')
    vrun('make gen_product')

@hosts('rainbow')
def dumpdata():
    puts('Dumping date from remote...')
    vrun('make dump')
    local('scp rainbow:/home/everbird/var/8100/data/backup-file.sql /home/everbird/var/8000/data/')
    local('make import_dump')
