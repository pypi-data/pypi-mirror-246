from setuptools import setup, find_packages
 
setup(
    name='tuchuang',
    version='1.0.0',
    description='图床是一个免费上传图片到SunPics图床并获取链接工具，基于SunPics开发',
    classifiers=[
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python',
        'Intended Audience :: Developers',
        'Operating System :: OS Independent',
    ],
    install_requires=[],    # install_requires字段可以列出依赖的包信息，用户使用pip或easy_install安装时会自动下载依赖的包
    author='python学霸',
    url='https://github.com',
    author_email='wow@qq.com',
    license='MIT',
    packages=find_packages(),  
    include_package_data=False,
    zip_safe=True,
)