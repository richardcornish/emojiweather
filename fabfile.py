from fabric import task

from django.utils.termcolors import colorize

# 1. Local: chmod 400 ~/.ssh/aws.pem
# 2. Local: ssh-add ~/.ssh/aws.pem OR ~/.ssh/config: Append to Host: IdentityFile ~/.ssh/aws.pem
# 3. Local: Edit hosts, repo_name, pythonpath (if necessary)
# 4. Remote: Copy .env to to {code_dir}/.env:


hosts = [{
    'host': 'ec2-3-89-247-193.compute-1.amazonaws.com',
    'user': 'ubuntu',
}]

repo_name = 'emojiweather'

pythonpath = f'{repo_name}/'

service_name = repo_name

code_dir = f'/home/ubuntu/{repo_name}/'


@task
def update(c):
    print(colorize('\nUpdating code...', fg='white'))
    c.run(f'cd {code_dir} && git pull origin master')


@task
def install(c):
    print(colorize('\nInstalling dependencies...', fg='white'))
    c.run(f'cd {code_dir} && source env/bin/activate && pip install -r requirements.txt')


@task
def migrate(c):
    print(colorize('\nMigrating database...', fg='white'))
    c.inline_ssh_env = True
    c.run(f'source {code_dir}.env && cd {code_dir} && source env/bin/activate && python {pythonpath}manage.py migrate --noinput', env={'DEBUG': '$DEBUG', 'DATABASE_PASSWORD': '$DATABASE_PASSWORD'})


@task
def collect(c):
    print(colorize('\nCopying static files...', fg='white'))
    c.run(f'cd {code_dir} && source env/bin/activate && python {pythonpath}manage.py collectstatic --noinput')


@task
def clear(c):
    print(colorize('\nDeleting sessions...', fg='white'))
    c.inline_ssh_env = True
    c.run(f'source {code_dir}.env && cd {code_dir} && source env/bin/activate && python {pythonpath}manage.py clearsessions', env={'DEBUG': '$DEBUG', 'DATABASE_PASSWORD': '$DATABASE_PASSWORD'})


@task
def restart(c):
    print(colorize('\nRestarting web server...\n', fg='white'))
    c.run(f'sudo systemctl restart {service_name}')
    c.run(f'sudo systemctl status {service_name}')
    print('')
    c.run('sudo systemctl restart nginx')
    c.run('sudo systemctl status nginx')


@task(hosts=hosts)
def deploy(c):
    print(colorize('\nStarting deploy... \U0001F44C', fg='green'))
    try:
        update(c)
        install(c)
        migrate(c)
        collect(c)
        # clear(c)
        restart(c)
        print(colorize('\nDeploy succeeded \U0001F389', fg='green'))
    except:
        print(colorize('\nDeploy failed \u274C', fg='red'))
