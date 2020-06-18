from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
import time
import re
from lstm_model import LSTM_model
import os

class go_url:
    def __init__(self):
        self.driver_path()
        return None

    # def driver_path(self):
    #     # options = webdriver.FirefoxOptions()
    #     # options.add_argument("--headless")
    #     # self.driver = webdriver.Firefox(executable_path=r'instagram_scrape\driver\geckodriver.exe', options=options)
    #     self.driver = webdriver.Chrome(executable_path=r'instagram_scrape\driver\chromedriver.exe')

    def driver_path(self):
        options = webdriver.ChromeOptions()
        options.add_argument("--headless")
        options.add_argument('--disable-gpu')
        options.add_argument('--no-sandbox')
        options.binary_location = os.environ.get("GOOGLE_CHROME_BIN")
        self.driver = webdriver.Chrome(executable_path=os.environ.get("CHROMEDRIVER_PATH"), options=options)

    def profile_screenshoot(self,username,password,url2):
        url = 'https://www.instagram.com/accounts/login/'
        self.driver.get(url)
        usernameInput = username
        passwordInput = password
        username = WebDriverWait(self.driver, 20).until(
            EC.element_to_be_clickable((By.XPATH, "//input[@name='username']"))).send_keys(usernameInput)
        password = WebDriverWait(self.driver, 20).until(
            EC.element_to_be_clickable((By.XPATH, "//input[@name='password']"))).send_keys(passwordInput)
        WebDriverWait(self.driver, 20).until(
            EC.element_to_be_clickable((By.XPATH, "//input[@name='password']"))).send_keys(
            Keys.ENTER)
        time.sleep(15)
        try:
            error="//*[@id='slfErrorAlert']"
            alert=self.driver.find_element(By.XPATH,error)
            self.driver.close()
            return False
        except:
            self.driver.get(url2)
            time.sleep(5)
            self.driver.save_screenshot('static/images/profil.png')
            self.driver.close()
            return True

    def login_page(self,url2):
        url='https://www.instagram.com/accounts/login/'
        self.driver.get(url)
        usernameInput = 'deteksicyberbullying'
        passwordInput = 'Arifku96!'
        username = WebDriverWait(self.driver, 20).until(
            EC.element_to_be_clickable((By.XPATH, "//input[@name='username']"))).send_keys(usernameInput)
        password = WebDriverWait(self.driver, 20).until(
            EC.element_to_be_clickable((By.XPATH, "//input[@name='password']"))).send_keys(passwordInput)
        WebDriverWait(self.driver, 20).until(EC.element_to_be_clickable((By.XPATH, "//input[@name='password']"))).send_keys(
            Keys.ENTER)
        time.sleep(15)
        self.post_page(url2)

    def deteksi(self,text,names,n):
        # id="//*[@id='react-root']/section/main/div/div[1]/article/div[2]/div[1]/ul/ul["+str(n)+"]/div/li/div/div[1]/div[2]/div/div/button"
        # id = "//*[@id='react-root']/section/main/div/div[1]/article/div[2]/div[1]/ul/ul["+str(n)+"]/div/li/div/div[1]/div[2]/div/div/button[2]"
        # print(id)
        model=LSTM_model()
        kelas=model.balas_komen(text)
        # element_enter = self.driver.find_element_by_xpath('//*[@id="react-root"]/section/main/div/div[1]/article/div[2]/section[3]/div/form/textarea')
        # elemen_enter= WebDriverWait(driver, 15).until(EC.presence_of_all_elements_located((By.XPATH, "//*[@id='pages-2']/div/ul/li/a[@href]")))

        peringatan='Halo @'+names+' ,komentar kamu beresiko menjadi komentar jahat. Lebih berhati-hati dalam berkomentar ' \
                                 'agar tidak ada pihak yang dirugikan. Lebih lengkapnya silahkan kunjungi profil saya -BOT'
        if(n==0):
            print('Caption')
        else:
            if (kelas == 0):
                try:
                    id = "//*[@id='react-root']/section/main/div/div[1]/article/div[2]/div[1]/ul/ul[" + str(
                        n) + "]/div/li/div/div[1]/div[2]/div/div/button[2]"
                    balas = self.driver.find_element(By.XPATH, id)
                    balas.click()
                except:
                    id = "//*[@id='react-root']/section/main/div/div[1]/article/div[2]/div[1]/ul/ul[" + str(
                        n) + "]/div/li/div/div[1]/div[2]/div/div/button"
                    balas = self.driver.find_element(By.XPATH, id)
                    balas.click()
                    pass
                # balas = self.driver.find_element(By.XPATH, id)
                # balas.click()
                element_click = self.driver.find_element_by_tag_name('textarea')
                element_click.click()
                element_clear = self.driver.find_element_by_class_name('Ypffh')
                element_clear.clear()
                element_komen = self.driver.find_element_by_class_name('Ypffh')
                element_komen.send_keys(peringatan)
                element_enter = self.driver.find_element_by_xpath('/html/body/div[1]/section/main/div/div[1]/article/div[2]/section[3]/div/form/button')
                element_komen.send_keys(Keys.ENTER)
                element_enter.click()
                time.sleep(2)
                print('Find Cyberbullying')
            else:
                print('Not Cyberbullying')
        return kelas

    def post_page(self,url):
        url_post = url
        self.driver.get(url_post)
        # if(self.driver.find_element_by_xpath('/html/body/div[1]/section/nav/div[2]/div/div/div[3]/div/div/div/div/div[2]/div[1]/div').is_displayed()):
        #     self.login_page(url)
        # else:
        try:
            if(self.driver.find_element_by_xpath('/html/body/div[1]/section/nav/div[2]/div/div/div[3]/div/div/div/div/div[2]/div[1]/div').is_displayed(True)):
                self.login_page()
        except:
            pass

        try:
            # load_more_comment = WebDriverWait(self.driver, 20).until(EC.element_to_be_clickable(
            #     (By.XPATH, '//*[@id="react-root"]/section/main/div/div/article/div[2]/div[1]/ul/li/div/button')))
            load_more_comment = driver.find_element_by_xpath(
                '/html/body/div[1]/section/main/div/div/article/div[2]/div[1]/ul/li/div/button/span')
            i = 0
            while load_more_comment.is_displayed() and i < 50:
                load_more_comment.click()
                i += 1
                time.sleep(2)
                load_more_comment = driver.find_element_by_xpath(
                    '/html/body/div[1]/section/main/div/div/article/div[2]/div[1]/ul/li/div/button/span')
        except:
                pass

        user_names = []
        user_comments = []
        label_comment=[]
        tuple=[]
        comment = self.driver.find_elements_by_class_name('gElp9 ')
        n=-1
        for c in comment:
            container = c.find_element_by_class_name('C4VMK')
            name = container.find_element_by_class_name('_6lAjh').text
            content = container.find_element_by_tag_name('span').text
            content = content.replace('\n', ' ').strip().rstrip()
            user_names.append(name)
            user_comments.append(content)
            n+=1
            x=self.deteksi(content,name,n)
            label_comment.append(x)
            data=(name,content,x)
            tuple.append(data)

        print(tuple)
        user_names.pop(0)
        user_comments.pop(0)
        label_comment.pop(0)
        from instagram_scrape import save
        from instagram_scrape import excel_exporter
        save.export(user_names, user_comments, label_comment, url_post,tuple)
        text = re.sub(r'[^a-zA-Z0-9]', '', url_post)
        print(text)
        with open('static/images/'+text+'.png', 'wb') as file:
            file.write(self.driver.find_element_by_xpath('/html/body/div[1]/section/main/div/div/article/div[1]/div/div/div[2]').screenshot_as_png)
        self.driver.close()

# arif=go_url()
# arif.login_page()
# arif.post_page('https://www.instagram.com/p/CA1c8b4DIFA/')