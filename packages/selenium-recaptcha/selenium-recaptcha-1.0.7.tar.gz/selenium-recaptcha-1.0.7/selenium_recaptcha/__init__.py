import os, requests, ffmpeg_downloader as ffdl, whisper, warnings, shutil
from selenium.webdriver.common.by import By
from .components import *

warnings.filterwarnings("ignore")
model = whisper.load_model("base.en")

class Recaptcha_Solver:
    """### Usage
	solver = Recaptcha_Solver(driver, ffmpeg_path, log)\n
	solver.solve_recaptcha()

    ### Params
    driver: selenium.webdriver
        This param is required.

    ffmpeg_path: str
        This param is optional. Provide ffmpeg executable `file` path
        or the `folder` path where ffmpeg exists.
        If nothing provided, it will use the ffmpeg from system.
        If ffmpeg is not found in your system, it will automaticlly download and install it.

    log: bool
        Set True if you want to view the progress.
	"""
    def __init__(s, driver, ffmpeg_path:str = None, log:bool = False) -> None:
        s.d = driver
        s.fp = ffmpeg_path
        s.l = log
        s.manage_ffmpeg()
    
    def manage_ffmpeg(s):
        if not s.fp:
            s.fp=shutil.which('ffmpeg')
            if not s.fp:
                if not ffdl.installed():
                    os.system('ffdl install --add-path -y')
                s.fp = ffdl.ffmpeg_path

        if not os.path.exists(s.fp):
            raise FFMPEG_Path_Error('The ffmpeg path does not exists. Path: %s' % s.fp)

        if os.path.isfile(s.fp):
            s.fp = os.path.dirname(s.fp)

        os.environ['PATH'] = os.pathsep.join([os.environ.get("PATH", ''), str(s.fp)])
    
    def o(s,*a,**b):
        b['end'], b['sep'] = '', ' '
        if s.l: print('\r' + b['sep'].join(a), **b)
    
    def transcribe(s, url):
        with open('.temp', 'wb') as f:
            s.o('Downloading Audio...')
            f.write(requests.get(url).content)
        s.o('Transcribing Audio...')
        try:
            result = model.transcribe('.temp')
        except FileNotFoundError:
            raise FileNotFoundError('FFMPEG executable is not found.')
        os.remove('.temp')
        return result["text"].strip()

    def click_checkbox(s):
        s.d.switch_to.default_content()
        s.o('Clicking Checkbox...')
        s.d.switch_to.frame(find_until_located(s.d, By.XPATH, ".//iframe[@title='reCAPTCHA']"))
        find_until_clickable(s.d, By.ID, "recaptcha-anchor-label").click()

    def request_audio_version(s):
        s.d.switch_to.default_content()
        s.o('Switching to Audio...')
        s.d.switch_to.frame(find_until_located(s.d, By.XPATH, ".//iframe[@title='recaptcha challenge expires in two minutes']"))
        find_until_clickable(s.d, By.ID, "recaptcha-audio-button").click()

    def solve_audio_captcha(s):
        text = s.transcribe(find_until_located(s.d, By.ID, "audio-source").get_attribute('src'))
        s.o('Sending transcribe...')
        find_until_located(s.d, By.ID, "audio-response").send_keys(text)
        find_until_clickable(s.d, By.ID, "recaptcha-verify-button").click()

    def check_blocking(s):
        try:
            find_until_located(s.d, By.CLASS_NAME, 'rc-doscaptcha-header-text')
        except KeyboardInterrupt:
            raise KeyboardInterrupt
        s.d.switch_to.default_content()
        raise Block_Error('Request blocked by google.')

    def solve_recaptcha(s):
        scroll_to_element(s.d, find_until_located(s.d, By.XPATH, ".//iframe[@title='reCAPTCHA']"))
        s.click_checkbox()
        try:
            s.request_audio_version()
            s.solve_audio_captcha()
        except KeyboardInterrupt:
            raise KeyboardInterrupt
        except:
            s.check_blocking()

        s.o('Recaptcha Solved')
        print()
        s.d.switch_to.default_content()






