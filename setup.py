from distutils.core import setup
import os

os.system("pip install -r requirements.txt")

setup(name='ViterbiDecoder',
      version='1.0',
      description='Implementation for Hard Viterbi Decoder on python ',
      author='Taher Anas',
      author_email='taheranas24@gmail.com',
      url='https://github.com/AnasTaherGit/ViterbiDecoder.git',
      package_dir={'Viterbi':'src'},
      packages=['Viterbi'] 
     )