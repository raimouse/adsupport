#使用虚拟环境
activate_this = '/var/www/ADhelper/venv/bin/activate_this.py'
import sys
sys.path.insert(0,'/var/www/ADhelper')
from main import app as application

