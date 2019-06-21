import virtualenv
import os
import sys
import time
import subprocess
from modules import general_functions as gf

virtual_env_dir_name = 'venv'

venv_dir = os.path.join(os.path.expanduser(os.getcwd()), virtual_env_dir_name)

virtualenv.create_environment(venv_dir)

activate_this = venv_dir + "/bin/activate_this.py"

exec(open(activate_this).read(), {'__file__': activate_this})

command ='pip install -r requirements.txt'

os.system(command)

env_file = str(os.getcwd()) + '/dev.env'

os.environ['env_file'] = env_file

gf.export_env_var(env_file)

compose_file = str(os.getcwd()) + '/DockerCompose/dev1.yml'

command ='docker-compose -f ' + compose_file + ' up -d'

os.system(command)

time.sleep(60)

os.environ['DB_HOST'] = 'localhost'

controller_path = str(os.getcwd()) + '/controller/manage.py'

bdsd_path = str(os.getcwd()) + '/BinanceDataStorageDaemon/main.py'

command = 'python ' + controller_path + ' makemigrations'
os.system(command)

command = 'python ' + controller_path + ' migrate --noinput'
os.system(command)

if (os.environ['controller_create_superuser'] == 'true'):

    create_super_user_cmd = '''import os
from django.contrib.auth import get_user_model
User = get_user_model()
if (not User.objects.filter(username=os.environ.get('controller_SUPERUSER_NAME')).exists()):
    User.objects.create_superuser(os.environ.get('controller_SUPERUSER_NAME'), os.environ.get('controller_SUPERUSER_MAIL'), os.environ.get('controller_SUPERUSER_PASS'))
else:
    pass'''

    subprocess.Popen([sys.executable, controller_path, 'shell', '-c', create_super_user_cmd], stdout=None)

controller_server = str(os.environ['controller_HOST']) + ':' + str(os.environ['controller_PORT'])

controller_pid = subprocess.Popen([sys.executable, controller_path, 'runserver', controller_server], stdout=None)

bdsd_pid = subprocess.Popen([sys.executable, bdsd_path], stdout=None)

msg = '''
controller_pid..: ''' + str(controller_pid.pid) + '''
bdsd_pid........: ''' + str(bdsd_pid.pid) + '''

'''
print(msg)