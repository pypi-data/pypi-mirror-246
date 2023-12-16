from setuptools import setup

# with open("README.rst", "r", encoding='utf-8') as f:
#     long_description = f.read()



setup(name='FreeWork',  # 包名
      version='0.0.3',  # 版本号
      description='简单又实用的office操作函数！(Simple and practical office operation functions!)',
      long_description="由于restructedText的兼容性原因，目前暂时无法上传详细介绍，我们将在下一个个版本中发布CSDN的连接，"
                       "那里将会有中英文双语的详细介绍！敬请期待。"
                       "\nDue to compatibility issues with reconstructedText, we are currently unable to upload a detailed introduction. We will release the CSDN connection in the next version, where there will be a detailed introduction in both Chinese and English! Stay tuned.",
      author='Jhonie King(王骏诚)',
      author_email='queenelsaofarendelle2022@gmail.com',
      license='MIT License',
      packages=["FreeWork"],
      keywords=['python', 'Office', 'Excle', 'Word', 'File\'s operation'],
      install_requires=['openpyxl', 'python-docx', 'pytest-shutil'],
      classifiers=[
          'Intended Audience :: Developers',
          'Operating System :: OS Independent',
          'Natural Language :: Chinese (Simplified)',
          'Programming Language :: Python',
          'Programming Language :: Python :: 2',
          'Programming Language :: Python :: 2.7',
          'Programming Language :: Python :: 3',
          'Programming Language :: Python :: 3.5',
          'Programming Language :: Python :: 3.6',
          'Programming Language :: Python :: 3.7',
          'Programming Language :: Python :: 3.8',
          'Topic :: Software Development :: Libraries'
      ],
      )
