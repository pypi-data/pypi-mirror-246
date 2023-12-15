from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

class FFMPEG_Path_Error(Exception): pass
class Block_Error(Exception): pass

def find_until_located(driver,find_by,name,timeout=10):
	return WebDriverWait(driver, timeout).until(EC.presence_of_element_located((find_by, name)))

def find_until_clickable(driver,find_by,name,timeout=10):
	return WebDriverWait(driver, timeout).until(EC.element_to_be_clickable((find_by, name)))

def scroll_to_element(driver,element):
	driver.execute_script("arguments[0].scrollIntoView();", element)

