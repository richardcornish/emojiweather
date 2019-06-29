from fabric import task

from django.utils.termcolors import colorize

# 1. Local: ssh-add ~/.ssh/aws.pem
# 2. Local: Edit hosts, repo_name, pythonpath (if necessary)
# 3. Remote: Copy .env to to {code_dir}/.env:
# 4. Remote: Add to ~/.bashrc: source ~/{repo_name}/.env


hosts = [{
    'host': 'ec2-3-89-247-193.compute-1.amazonaws.com',
    'user': 'ubuntu',
}]

repo_name = 'emojiweather'

pythonpath = repo_name

service_name = repo_name

code_dir = f'/home/ubuntu/{repo_name}'


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
    c.run(f'cd {code_dir} && source env/bin/activate && python {pythonpath}/manage.py migrate --noinput')


@task
def collect(c):
    print(colorize('\nCopying static files...', fg='white'))
    c.run(f'cd {code_dir} && source env/bin/activate && python {pythonpath}/manage.py collectstatic --noinput --verbosity 1')


@task
def clear(c):
    print(colorize('\nDeleting old sessions...', fg='white'))
    c.run(f'cd {code_dir} && source env/bin/activate && python {pythonpath}/manage.py clearsessions --verbosity 1')


@task
def restart(c):
    print(colorize('\nRestarting web server...', fg='white'))
    c.run(f'sudo systemctl restart {service_name}')
    c.run(f'sudo systemctl status {service_name}')
    c.run('sudo systemctl restart nginx')
    c.run('sudo systemctl status nginx')


@task(hosts=hosts)
def deploy(c):
    print(colorize('\nStarting deploy... 👌', fg='green'))
    try:
        update(c)
        install(c)
        migrate(c)
        collect(c)
        # clear(c)
        restart(c)
        print(colorize('\nDeploy succeeded 🎉', fg='green'))
    except:
        print(colorize('\nDeploy failed ❌', fg='red'))