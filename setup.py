from setuptools import setup, find_packages

setup(name="geventdaemon",
      version="0.1dev",
      author="Antonin Amand",
      author_email="antonin.amand@gmail.com",
      description="gevent daemonizer",
      package_dir = {'':'lib'},
      packages=find_packages('lib'),
      zip_safe=False,
      install_requires=[
          'python-daemon',
        ],
    )

