import time, os, shutil
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

song_details = input("Song Track Details for one or more songs (Artist - Song Name, Artist - Song Name, etc.): ")
song_list = song_details.split(sep=", ")

download_path = r"C:\Users\Kai Jing\Music\Songs\normalized\00 normalize\test"

chromeOptions = webdriver.ChromeOptions()
prefs = {"download.default_directory" : download_path}
chromeOptions.add_experimental_option("prefs",prefs)

for item in song_list:
    driver = webdriver.Chrome(executable_path=r"C:\Users\Kai Jing\Desktop\KJ's Online Sync\Selenium\chromedriver.exe",chrome_options=chromeOptions)
    driver.get("https://www.google.com/")

    def download_status():
        for i in os.listdir(download_path):
            if '.crdownload' in i:
                time.sleep(0.5)
                download_status()

    artist_name, song_name = item.split(" - ")

    # Extracting album from Wikipedia
    try:
        google_search = driver.find_element_by_xpath('//*[@id="tsf"]/div[2]/div[1]/div[1]/div/div[2]/input')
    except:
        google_search = driver.find_element_by_xpath("//*[@id='tsf']/div[2]/div[1]/div[1]/div/div[2]/input")

    google_search.send_keys(artist_name+" "+song_name+" Wikipedia", Keys.ENTER)

    try:
        wiki_url = driver.find_element_by_xpath("//*[@id='rso']/div[1]/div/div[1]/div/div/div[1]/a").get_attribute("href")
        driver.get(wiki_url)
    except:
        try:
            wiki_url = driver.find_element_by_xpath('//*[@id="rso"]/div[1]/div/div/div/div[1]/a').get_attribute("href")
            driver.get(wiki_url)
        except:
            pass

    try:
        assert song_name.lower() in driver.title.lower()
    except:
        print("Song name not found in Wikipedia title.")

    try:
        song_check = driver.find_element_by_xpath("//*[@id='mw-content-text']/div/table/tbody/tr[1]/th").text
        assert song_name.lower() in song_check.lower()
    except:
        print("Song name not found in Wikipedia table header.")

    try:
        song_desc = driver.find_element_by_xpath("//*[@id='mw-content-text']/div/table[1]/tbody/tr[3]/th").text
        assert artist_name.lower() in song_desc.lower()
    except:
        print("Artist name not found in table description.")

    try:
        length_min = driver.find_element_by_css_selector("span[class='min']").text
        length_sec = driver.find_element_by_css_selector("span[class='s']").text
        print(song_name+" by "+artist_name+" is "+length_min+" mins and "+length_sec+" seconds long.")
    except:
        pass

    try:
        album_name = driver.find_element_by_xpath("//*[@id='mw-content-text']/div/table/tbody/tr[4]/th/i/a").text
    except:
        try:
            album_name = driver.find_element_by_xpath("//*[@id='mw-content-text']/div/table[1]/tbody/tr[4]/th/i/a").text
        except:
            try:
                album_name = driver.find_element_by_xpath("//*[@id='mw-content-text']/div/table[2]/tbody/tr[4]/th/i/a").text
            except:
                try:
                    driver.get("https://www.google.com/")
                    google_search = driver.find_element_by_xpath("//*[@id='tsf']/div[2]/div[1]/div[1]/div/div[1]/input")
                    google_search.send_keys(artist_name+" "+song_name+" song", Keys.ENTER)

                    bool_check = driver.find_element_by_xpath("//*[@id='rso']/div[1]/div/div[1]/div/div[1]/div[2]/div[3]/div/div[1]/div/g-expandable-container/div/div/div").text
                    assert bool_check == "Lyrics"

                    artist_ele = driver.find_element_by_xpath("//*[@id='rso']/div[1]/div/div[1]/div/div[1]/div[2]/div[3]/div/div[3]/div/div/span[1]/a").text
                    assert artist_ele == "Artist"
                    artist_google = driver.find_element_by_xpath("//*[@id='rso']/div[1]/div/div[1]/div/div[1]/div[2]/div[3]/div/div[3]/div/div/span[2]/a").text
                    assert artist_name == artist_google

                    album_ele = driver.find_element_by_xpath("//*[@id='rso']/div[1]/div/div[1]/div/div[1]/div[2]/div[3]/div/div[4]/div/div/span[1]/a").text
                    assert album_ele == "Album"
                    album_name = driver.find_element_by_xpath("//*[@id='rso']/div[1]/div/div[1]/div/div[1]/div[2]/div[3]/div/div[4]/div/div/span[2]/a").text
                except:
                    try:
                        artist_ele = driver.find_element_by_xpath("//*[@id='rso']/div[1]/div/div[1]/div/div[1]/div[2]/div[3]/div/div[2]/div/div/span[1]/a").text
                        assert artist_ele == "Artist"
                        artist_google = driver.find_element_by_xpath("//*[@id='rso']/div[1]/div/div[1]/div/div[1]/div[2]/div[3]/div/div[2]/div/div/span[2]/a").text
                        assert artist_name == artist_google

                        album_ele = driver.find_element_by_xpath("//*[@id='rso']/div[1]/div/div[1]/div/div[1]/div[2]/div[3]/div/div[3]/div/div/span[1]/a").text
                        assert album_ele == "Album"
                        album_name = driver.find_element_by_xpath("//*[@id='rso']/div[1]/div/div[1]/div/div[1]/div[2]/div[3]/div/div[3]/div/div/span[2]/a").text
                    except:
                        try:
                            driver.get(wiki_url)
                            album_name = input("Album: ")
                        except:
                            album_name = input("Album: ")

    print(song_name+" is from the album \""+album_name+"\".")

    driver.get("https://www.google.com/")
    try:
        google_search = driver.find_element_by_xpath("//*[@id='tsf']/div[2]/div[1]/div[1]/div/div[1]/input")
    except:
        google_search = driver.find_element_by_xpath("//*[@id='tsf']/div[2]/div[1]/div[1]/div/div[2]/input")
    google_search.send_keys(artist_name+" "+song_name+" song", Keys.ENTER)

    try:
        for i in range(5):
            year_check = "//*[@id='rso']/div[1]/div/div[1]/div/div[1]/div[2]/div[3]/div/div["+str(i+3)+"]/div/div/span[1]/a"
            year_xpath = "//*[@id='rso']/div[1]/div/div[1]/div/div[1]/div[2]/div[3]/div/div["+str(i+3)+"]/div/div/span[2]"

            year_ele = driver.find_element_by_xpath(year_check).text
            if year_ele == "Released":
                song_year = year_ele = driver.find_element_by_xpath(year_xpath).text
                break

        print(song_name+" was released in "+song_year+".")
    except:
        try:
            driver.get(wiki_url)
            song_year = driver.find_element_by_css_selector("td[style='width: 33%; text-align: center; vertical-align: top; padding:.2em .1em;']").text
            song_year = song_year[-5:-1]

            print(song_name+" was released in "+song_year+".")
        except:
            pass

    driver.get("https://www.youtube.com/")
    yt_search = driver.find_element_by_xpath("//*[@id='search']")
    yt_search.send_keys(str.lower(artist_name)+' '+str.lower(song_name)+' hq')
    driver.find_element_by_xpath("//*[@id='search-icon-legacy']").click()

    skip_song = input("Would you like to skip the current song? (y/n) ")
    if skip_song.lower() == 'y':
        driver.quit()
        continue

    url = input("Download Link: ")

    driver.get("https://www.bigconverter.com/index.php")
    dl_url = driver.find_element_by_xpath("//*[@id='videoURL']")
    dl_url.send_keys(url)

    driver.find_element_by_xpath("//*[@id='ftype']/optgroup[1]/option[5]").click()
    driver.find_element_by_xpath("//*[@id='conversionForm']/div/div[1]/span/button").click()

    time.sleep(10)

    element = WebDriverWait(driver,30).until(EC.element_to_be_clickable((By.XPATH,"//*[@id='editFurtherButton']")))
    further_edit = driver.find_element_by_xpath("//*[@id='editFurtherButton']").get_attribute('href')
    driver.get(further_edit)

    title_field = driver.find_element_by_name("atitle")
    title_field.clear()
    title_field.send_keys(song_name)

    artist_field = driver.find_element_by_name("artist")
    artist_field.send_keys(artist_name)

    album_field = driver.find_element_by_name("album")
    album_field.send_keys(album_name)

    try:
        driver.find_element_by_xpath("//*[@id='pressing']").click()
    except:
        driver.find_element_by_xpath("/html/body/div[1]/div[1]/div[1]/div/div/div/div/center/div[2]").click()
    time.sleep(5)

    url2 = driver.find_element_by_css_selector("a[class='btn btn-success']").get_attribute("href")

    driver.get(url2)

    time.sleep(0.5)
    download_status()
    time.sleep(1)

    dl_folder = os.listdir(r"C:\Users\Kai Jing\Music\Songs\normalized\00 normalize\test")

    dl_dir = r"C:\Users\Kai Jing\Music\Songs\normalized\00 normalize\test"
    master_dir = r"C:\Users\Kai Jing\Music\Songs\normalized\00 normalize"
    shutil.move((dl_dir+"\\"+dl_folder[0]),(master_dir+"\\"+item+".mp3"))

    driver.quit()
