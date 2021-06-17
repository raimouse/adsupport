#使用虚拟环境
activate_this = '/var/www/adsupport/venv/bin/activate_this.py'
import sys
sys.path.insert(0,'/var/www/adsupport')
from main import app as application

