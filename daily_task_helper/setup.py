from setuptools import setup, find_namespace_packages

setup(name='daily_task_helper',
      version='0.0.1',
      description='Useful helper',
      url='https://github.com/LOKFaaDDiiV/TeamProjectAssistant',
      author='Hlib Kirin',
      author_email='koto.amatsukami@ukr.net',
      license='MIT',
      packages=find_namespace_packages(),
      install_requires=['colorama', 'wcwidth'],
      python_requires=">=3.7",
      entry_points={'console_scripts': ['daily-task-helper = daily_task_helper.main:main']}
      )
