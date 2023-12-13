from setuptools import setup, find_packages

setup(
    name='tybase2',
    version='1.0.4',
    description='字幕处理新增setup_default_style,可以添加字幕的效果',
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