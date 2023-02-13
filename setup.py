from distutils.core import setup

from pathlib import Path
this_directory = Path(__file__).parent
long_description = (this_directory / "README.md").read_text()

setup(
  name = 'mashup_yt',
  packages = ['mashup_yt'],
  version = '0.0.2',
  license='MIT',        
  description = 'This module creates a mashup of songs of your favorite singer with a single click.',
  long_description=long_description,
  long_description_content_type='text/markdown',   
  author = 'Chitraksh Kumar',                   
  author_email = 'chitraksh24@gmail.com',      
  url = 'https://github.com/Chitru4/mashup_yt',
  download_url = 'https://github.com/Chitru4/mashup_yt/archive/refs/tags/mashup_yt.tar.gz',
  keywords = ['MASHUP', 'YOUTUBE', 'PROJECT','MUSIC','MP3'],   
  install_requires=[           
          'pytube',
          'pydub',
          'flask',
          'requests'
      ],
  entry_points='''
    [console_scripts]
    mashup_yt = mashup_yt.app:main
  ''',
  classifiers=[
    'Development Status :: 3 - Alpha',      
    'Intended Audience :: Developers',      
    'Topic :: Software Development :: Build Tools',
    'License :: OSI Approved :: MIT License',   
    'Programming Language :: Python :: 3',      
    'Programming Language :: Python :: 3.4',
    'Programming Language :: Python :: 3.5',
    'Programming Language :: Python :: 3.6',
  ],
)
