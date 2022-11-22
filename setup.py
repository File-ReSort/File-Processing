import sys
import subprocess
from Classes import log

log.printSection('Downloading Required Models')
subprocess.check_call([sys.executable, '-m', 'coreferee', 'install', 'en'])
subprocess.check_call([sys.executable, '-m', 'spacy', 'download', 'en_core_web_trf'])
subprocess.check_call([sys.executable, '-m', 'spacy', 'download', 'en_core_web_lg'])

log.printSection('Installing packages')
subprocess.check_call([sys.executable, '-m', 'pip', 'install', '--upgrade', 'pip'])
subprocess.check_call([sys.executable, '-m', 'pip', 'install', 'flask'])
subprocess.check_call([sys.executable, '-m', 'pip', 'install', 'coreferee'])
subprocess.check_call([sys.executable, '-m', 'pip', 'install', '-U', 'pip', 'setuptools', 'wheel'])
subprocess.check_call([sys.executable, '-m', 'pip', 'install', '-U', 'spacy'])

print("\nSetup complete, You can now run the application with the command\nflask --app main run")