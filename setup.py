from distutils.core import setup

setup(name='Ketcher',
      version='1.0',
      description='Ketcher toolkit and service',
      author='Andrew Yip',
      author_email='pandaaaa906@gmail.com',
      url='https://github.com/Pandaaaa906/ketcher_server',
      packages=['flask_ketcher', ],
      package_dir={'flask_ketcher': 'flask_ketcher'},
      package_data={'flask_ketcher': ['static/*', 'static/*/*']},
      requires=['flask', ]
      )
