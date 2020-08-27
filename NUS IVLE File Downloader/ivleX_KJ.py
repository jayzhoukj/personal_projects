
# coding: utf-8

# In[ ]:


import time, os, shutil, getpass
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# download_path = input("Enter root directory to store/update all module folders: ")
download_path = r"C:\Users\Kai Jing\Desktop\NUS\Business (Accountancy)\NUS BAC\Sem 2.2"

# nus_timetable = input("Enter NUS Mods Timetable Share Link: ")
nus_timetable = "http://modsn.us/5k6lT"

# user_name = input("NUS Username: ")
# pass_word = getpass.getpass("NUS Password: ")
user_name = ""
pass_word = ""

chromeOptions = webdriver.ChromeOptions()
prefs = {"download.default_directory" : download_path}
chromeOptions.add_experimental_option("prefs",prefs)

driver = webdriver.Chrome(executable_path="chromedriver.exe",chrome_options=chromeOptions)

exception_list = []

def folder_creation(folder_name, input_path, directory_listing):
    current_path = input_path
    dir_listing = directory_listing
    
    if folder_name not in dir_listing:
        os.mkdir(current_path+"\\"+folder_name)
    elif folder_name in dir_listing:
        pass

def download_status():
    for i in os.listdir(download_path):
        if '.crdownload' in i:
            time.sleep(0.5)
            download_status()

def folder_method(input_path, directory_listing):
    current_path = input_path
    dir_listing = directory_listing
    child_folder = {}
    
    for i in range(100):            
        try:
            icon_path = '//*[@id="mainTable"]/tbody/tr['+str(i+1)+']/td[2]/img'
            listed_icon = WebDriverWait(driver,5).until(EC.element_to_be_clickable((By.XPATH,icon_path)))
            icon_source = listed_icon.get_attribute('src')
        except:
            break

        try:
            file_path = '//*[@id="mainTable"]/tbody/tr['+str(i+1)+']/td[3]/'
            listed_item = driver.find_element_by_xpath(file_path+'a')
        except:
            continue

        if 'folder_empty' in icon_source:
            folder_creation(listed_item.text, current_path, dir_listing)

        elif 'folder_upload' in icon_source:
            continue

        elif 'folder_full' in icon_source:
            folder_creation(listed_item.text, current_path, dir_listing)
            listed_name = listed_item.text
            listed_link = listed_item.get_attribute('href')
            child_folder.update({listed_name:listed_link})
            
        elif 'folder_close' in icon_source:
            continue
            
        elif listed_item.text in exception_list:
            continue

        else:
            try:
                dl_icon = driver.find_element_by_xpath(file_path+'img')
                driver.get(listed_item.get_attribute('href'))
                
                time.sleep(0.5)
                download_status()
                time.sleep(1)
                
                shutil.move((download_path+"\\"+listed_item.text),(current_path+"\\"+listed_item.text))
                download_consolidated.update({listed_item.text:current_path})
                
            except:
                if listed_item.text not in dir_listing:
                    driver.get(listed_item.get_attribute('href'))
                    
                    time.sleep(0.5)
                    download_status()
                    time.sleep(1)
                    
                    shutil.move((download_path+"\\"+listed_item.text),(current_path+"\\"+listed_item.text))
                    download_consolidated.update({listed_item.text:current_path})
                    
                elif listed_item.text in dir_listing:
                    continue
    
    if len(child_folder) != 0:
        for i in child_folder:
            current_path += "\\" + i
            dir_listing = os.listdir(current_path)
            
            additional_path = len(i) + 1
            driver.get(child_folder[i])
            
            folder_method(current_path, dir_listing)
            
            current_path = current_path[:-additional_path]
        
    elif len(child_folder) == 0:
        pass

driver.get(nus_timetable)

my_modules = {}

for i in range(15):
    module_xpath = '//*[@id="app"]/div/div[1]/main/div/div/div[2]/div[2]/div/div[3]/div/div['+str(i+1)+']/div[2]/a'
    
    try:
        module_element = WebDriverWait(driver,5).until(EC.element_to_be_clickable((By.XPATH,module_xpath)))
    except:
        break
    
    module_code = module_element.text[:7]
    module_code = module_code.strip()
    module_name = module_element.text[len(module_code)+1:]
    my_modules.update({module_code:module_name})

print(my_modules,"\n")

for i in my_modules:
    root_listing = os.listdir(download_path)
    module_folder = i + " - " + my_modules[i]
    
    if module_folder not in root_listing:
        folder_creation(module_folder,download_path,root_listing)
    else:
        continue

driver.get("https://ivle.nus.edu.sg/default.aspx")

user_field = driver.find_element_by_xpath('//*[@id="ctl00_ctl00_ContentPlaceHolder1_userid"]')
user_field.send_keys(user_name)

pw_field = driver.find_element_by_xpath('//*[@id="ctl00_ctl00_ContentPlaceHolder1_password"]')
pw_field.send_keys(pass_word,Keys.ENTER)
    
download_consolidated = {}

for i in range(20):
    driver.get('https://ivle.nus.edu.sg/v1/workspace.aspx')
    
    try:
        module_path = '//*[@id="collapseTwo"]/div/div['+str(i+1)+']/div[1]/div/div[1]/strong/u/a'
        module_item = WebDriverWait(driver,5).until(EC.element_to_be_clickable((By.XPATH,module_path)))
        module_code = module_item.text
        
        announcement_path = '//*[@id="ctl00_ctl00_ContentPlaceHolder1_ContentPlaceHolder1_LV_Student_ctrl'+str(i)+'_btnAnnStu"]'
        announcement_icon = WebDriverWait(driver,5).until(EC.element_to_be_clickable((By.XPATH,announcement_path)))
        
    except:
        break
    
    if (module_code[:7] in my_modules or module_code[-7:] in my_modules or module_code[:6] in my_modules or module_code[-6:] in my_modules) and announcement_icon.is_displayed():
        try:
            my_modules[module_code[:7]]
            module_code = module_code[:7]
        
        except:
            try:
                my_modules[module_code[-7:]]
                module_code = module_code[-7:]
            except:
                try:
                    my_modules[module_code[:6]]
                    module_code = module_code[:6]
                except:
                    my_modules[module_code[-6:]]
                    module_code = module_code[-6:]
        
        module_name = my_modules[module_code]
        print(module_code+" - "+module_name)

        driver.get(module_item.get_attribute('href'))

        module_workbin = driver.find_element_by_xpath('//*[@id="ctl00_ctl00_ctl00_ContentPlaceHolder1_ContentPlaceHolder1_divSideMenu"]/ul/li[7]/a')
        driver.get(module_workbin.get_attribute('href'))

        current_path = download_path+"\\"+module_code+" - "+my_modules[module_code]
        dir_listing = os.listdir(current_path)

        child_folder = {}

        for i in range(20):
            try:
                icon_path = '//*[@id="mainTable"]/tbody/tr['+str(i+1)+']/td[1]/img'
                listed_icon = WebDriverWait(driver,5).until(EC.element_to_be_clickable((By.XPATH,icon_path)))
                icon_source = listed_icon.get_attribute('src')
            except:
                break

            try:
                file_path = '//*[@id="mainTable"]/tbody/tr['+str(i+1)+']/td[2]/'
                listed_item = driver.find_element_by_xpath(file_path+'a')
            except:
                continue

            if 'folder_empty' in icon_source:
                folder_creation(listed_item.text, current_path, dir_listing)

            elif 'folder_upload' in icon_source:
                continue

            elif 'folder_full' in icon_source:
                folder_creation(listed_item.text, current_path, dir_listing)
                listed_name = listed_item.text
                listed_link = listed_item.get_attribute('href')
                child_folder.update({listed_name:listed_link})
                
            elif 'folder_close' in icon_source:
                continue
                
            elif listed_item.text in exception_list:
                continue

            else:
                try:
                    dl_icon = driver.find_element_by_xpath(file_path+'img')
                    driver.get(listed_item.get_attribute('href'))
                    
                    time.sleep(0.5)
                    download_status()
                    time.sleep(1)
                    
                    shutil.move((download_path+"\\"+listed_item.text),(current_path+"\\"+listed_item.text))
                    download_consolidated.update({listed_item.text:current_path})
                
                except:
                    if listed_item.text not in dir_listing:
                        driver.get(listed_item.get_attribute('href'))
                        
                        time.sleep(0.5)
                        download_status()
                        time.sleep(1)
                        
                        shutil.move((download_path+"\\"+listed_item.text),(current_path+"\\"+listed_item.text))
                        download_consolidated.update({listed_item.text:current_path})
                        
                    elif listed_item.text in dir_listing:
                        continue

        if len(child_folder) != 0:
            for i in child_folder:
                current_path += "\\" + i
                dir_listing = os.listdir(current_path)

                path_len = len(i) + 1
                driver.get(child_folder[i])

                folder_method(current_path, dir_listing)

                current_path = current_path[:-path_len]

        elif len(child_folder) == 0:
            pass
    
    else:
        continue

print("\n"+"Folder update complete!"+"\n")

if len(download_consolidated) != 0:
    print("The following files were downloaded:")
    download_count = 1

    for i in download_consolidated:
        print(str(download_count)+". \""+i+"\", Location: "+download_consolidated[i]+"\n")
        download_count += 1
        
    download_index = {}
    index_count = 1

    for i in download_consolidated:
        download_index.update({str(index_count):i})
        index_count += 1
        
    delete_ask = input("Would you like to delete any of the downloaded files? [Yes/No] ")
    delete_ask = delete_ask.replace(' ','')

    if delete_ask.lower() == "yes":
        delete_index = input("Which files would you like to delete? [Example: 1, 3, 7] ")
        delete_index = delete_index.replace(' ','').split(',')

        delete_consolidated = {}
        file_exception = []
        delete_count = 1

        for i in delete_index:
            delete_consolidated.update({str(delete_count):download_index[i]})
            file_exception.append(download_index[i])
            delete_count += 1

            delete_path = download_consolidated[download_index[i]] + "\\" + download_index[i]
            os.remove(delete_path)

        print(delete_consolidated,"\n")

        print("The following files were deleted:"+"\n")

        for i in delete_consolidated:
            print(i+". "+delete_consolidated[i]+"\n")
            
        print(file_exception)
    
elif len(download_consolidated) == 0:
    print("No files were downloaded.")

try:
    driver.find_element_by_xpath('//*[@id="ctl00_ctl00_ctl00_ContentPlaceHolder1_lblProfile"]').click()
except:
    driver.find_element_by_xpath('//*[@id="ctl00_ctl00_ContentPlaceHolder1_lblProfile"]').click()

logout_link = driver.find_element_by_xpath('//*[@id="aspnetForm"]/div[3]/div[1]/div/div[2]/ul[2]/li[1]/ul/li[3]/a').get_attribute('href')
driver.get(logout_link)

print("\n"+"Logout complete!"+"\n")

print("Remember to check Luminus for module files that are not in IVLE!")

driver.quit()

