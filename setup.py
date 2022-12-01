import sys
import subprocess
from Classes import log

log.printSection('Installing packages')
subprocess.check_call([sys.executable, '-m', 'pip', 'install', '--upgrade', 'pip'])
subprocess.check_call([sys.executable, '-m', 'pip', 'install', '-Iv', '-U', 'spacy==3.4.3'])
subprocess.check_call([sys.executable, '-m', 'pip', 'install', '-Iv', 'flask==2.2.2'])
subprocess.check_call([sys.executable, '-m', 'pip', 'install', '-U', 'pip', 'setuptools', 'wheel'])
subprocess.check_call([sys.executable, '-m', 'pip', 'install', '-Iv', 'PyPDF2==2.10.9'])
subprocess.check_call([sys.executable, '-m', 'pip', 'install', '-Iv', 'neo4j==5.3.0'])
subprocess.check_call([sys.executable, '-m', 'pip', 'install', '-Iv', 'waitress==2.1.2'])
subprocess.check_call([sys.executable, '-m', 'pip', 'install', '-Iv', 'coreferee==1.3.0'])
subprocess.check_call([sys.executable, '-m', 'coreferee', 'install', 'en'])

log.printSection('Downloading Required Models')
subprocess.check_call([sys.executable, '-m', 'pip', 'install', '-Iv', 'https://github.com/explosion/spacy-models/releases/download/en_core_web_trf-3.4.0/en_core_web_trf-3.4.0.tar.gz'])
subprocess.check_call([sys.executable, '-m', 'pip', 'install', '-Iv', 'https://github.com/explosion/spacy-models/releases/download/en_core_web_lg-3.4.0/en_core_web_lg-3.4.0.tar.gz'])

print("\nSetup complete, You can now run the application with the command\npython main.py")
