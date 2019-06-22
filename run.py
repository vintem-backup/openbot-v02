import virtualenv
import os
import sys
import time
import subprocess
import shutil
from modules import general_functions as gf

'''Usage: python run.py <op>

<op>
====

    dev0        -- Run postgreSQL database and pgadmin containers.

    dev1        -- Same as dev0 plus: Export environment variables, install and activate python 
                    virtual environment, install all project's dependencies, adjust some environment
                    variables. In the end, run the BinanceDataStorageDaemon/main.py, make django 
                    migrations, migrate and run the djnago runserver of the controller.

    staging1    -- Build and run postgreSQL database, pgadmin, controler and binance storage data 
                    containers

    staging2    -- Same as staging1, but instead to build, all containers images are from 
                    container registry service.
    
    delivery1   -- Build the containers` images (no latest) and push them to specific container 
                    registry service.

    delivery2   -- Build the containers` LATEST images and push them to specific container 
                    registry service.

    aws         -- Run the production cluster on a AWS, from remote container`s images.


'''

mode = str(sys.argv[1])

if ( mode == 'aws' ):

    env_file = '/efs/.env'

else:

    env_file = str(os.getcwd()) + '/dev/dev.env'

os.environ['env_file'] = env_file

export_status = gf.export_env_var(env_file)

if (export_status == 'done'):

    virtual_env_dir_name = 'venv'

    venv_dir = os.path.join(os.path.expanduser(os.getcwd()), virtual_env_dir_name)

    virtualenv.create_environment(venv_dir)

    activate_this = venv_dir + "/bin/activate_this.py"

    exec(open(activate_this).read(), {'__file__': activate_this})

    modules_src = str(os.getcwd()) + '/modules/'

    bdsd_modules_dst = str(os.getcwd()) + '/BinanceDataStorageDaemon/modules/'

    if (os.path.exists(bdsd_modules_dst) == True):

        shutil.rmtree(bdsd_modules_dst)

    shutil.copytree(modules_src, bdsd_modules_dst)

    warning = bdsd_modules_dst + '/__DO_NOT_EDIT_FILES_HERE__'
    open(warning, 'a').close()

    if (mode == 'dev0'):

        pass

    elif (mode == 'dev1'):

        os.environ['run_mode'] = 'dev'

        command ='pip install -r requirements.txt'
        os.system(command)

        compose_file = str(os.getcwd()) + '/DockerCompose/dev1.yml'

        command ='docker-compose -f ' + compose_file + ' up -d'
        os.system(command)

        time.sleep(60)

        os.environ['DB_HOST'] = 'localhost'

        controller_path = str(os.getcwd()) + '/controller/manage.py'

        controller_server = str(os.environ['controller_HOST']) + ':' + str(os.environ['controller_PORT'])

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

        controller_pid = subprocess.Popen([sys.executable, controller_path, 'runserver', controller_server], stdout=None)

        bdsd_pid = subprocess.Popen([sys.executable, bdsd_path], stdout=None)

        msg = '''
    controller_pid..: ''' + str(controller_pid.pid) + '''
    bdsd_pid........: ''' + str(bdsd_pid.pid) + '''

    '''
        print(msg)

    elif (mode == 'staging1'):

        command ='pip install docker-compose'
        os.system(command)

        compose_file = 'DockerCompose/staging1.yml'
        
        command ='docker-compose -f ' + compose_file + ' down'
        os.system(command)

        #command ='docker-compose -f ' + compose_file + ' build --no-cache controller'
        #os.system(command)

        #command ='docker-compose -f ' + compose_file + ' build --no-cache binancedatastoragedaemon'
        #os.system(command)

        command ='docker-compose -f ' + compose_file + ' up -d'
        os.system(command)

else:

    print('Arquivo de variáveis de ambiente não encontrado')
