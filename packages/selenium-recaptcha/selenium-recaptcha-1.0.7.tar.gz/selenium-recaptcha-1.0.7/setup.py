from setuptools import setup, find_packages

VERSION = '1.0.7'
DESCRIPTION = 'reCaptcha v2 solver for selenium'
LONG_DESCRIPTION = '''
A package that allows to solve reCaptcha v2 with selenium.
<br>
<h3>Simple Example:</h3>
<pre><code>
from selenium import webdriver
from selenium_recaptcha import Recaptcha_Solver

driver = webdriver.Chrome()
driver.get('https://www.google.com/recaptcha/api2/demo')

solver = Recaptcha_Solver(
    driver=driver, # Your Web Driver
    ffmpeg_path='<PATH TO FFMPEG>', # Optional. If does not exists, it will automatically download.
    log=1 # If you want to view the progress.
)
solver.solve_recaptcha()

</code></pre>

'''

# Setting up
setup(
    name="selenium-recaptcha",
    version=VERSION,
    author="S M Shahriar Zarir",
    author_email="<shahriarzariradvance@gmail.com>",
    description=DESCRIPTION,
    long_description_content_type="text/markdown",
    long_description=LONG_DESCRIPTION,
    packages=find_packages(),
    install_requires='requests ffmpeg-downloader openai-whisper selenium'.split(),
    keywords=['python', 'reCaptcha', 'bot','selenium','selenium recaptcha solver'],
    classifiers=
[        "Development Status :: 1 - Planning",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "Operating System :: Unix",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows",
    ]
)