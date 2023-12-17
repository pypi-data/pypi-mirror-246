from setuptools import setup, find_packages

setup(
    name='fuck-image',
    version='1.0.0',
    author='python学霸',
    author_email='your_email@example.com',
    description='是一个免费上传图片图床，基于SunPics开发',
    packages=find_packages(),
    install_requires=[
        'requests',
    ],
)