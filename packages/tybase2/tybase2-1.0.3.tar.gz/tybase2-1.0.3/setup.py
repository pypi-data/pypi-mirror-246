from setuptools import setup, find_packages

setup(
    name='tybase2',
    version='1.0.3',
    description='新增add_background_music_amix,可以混合叠加音乐',
    long_description=open('README.md', 'r', encoding='utf-8').read(),
    long_description_content_type='text/markdown',
    author='Ty',
    author_email='zhangtezhangte@gmail.com',
    # url='https://github.com/yourusername/your_package',
    packages=find_packages(),
    install_requires=[
        # List your package dependencies here
    ],
)