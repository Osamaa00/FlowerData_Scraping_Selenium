from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from pymongo import MongoClient
import script2_flowerNames
import time

PATH = r"C:\Users\N B C\Downloads\chromedriver.exe"

cluster = MongoClient("mongodb+srv://osamanadeem:bmw600bmw600@cluster0.8ke0m.mongodb.net/db_flowers?retryWrites=true&w=majority")
db = cluster['db_flowers']
collection = db['flowers']


# flower_names = 
# driver.maximize_window()

# driver = webdriver.Chrome(PATH)
f = open("notFound.txt", "a")

# flowerName = "Moss rose"
def main (flowerName):
    ser = Service(PATH)
    driver = webdriver.Chrome(service=ser)
    flower_obj = {}
    driver.get(f"https://www.bhg.com/bin/plants/?name={flowerName}")
    flower_obj["flower_name"] = flowerName
    try:
        searchResultsDiv = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CLASS_NAME, "search-results-content-results-wrapper"))
        )

        childDivResults = searchResultsDiv.find_elements(By.XPATH, './child::div')
        # check if any results came in
        if ( len(childDivResults) > 0 ) :
            # print("this is the data I got: ", childDivResults)
            getLinkTag = []
            for linkTag in childDivResults:
                getLinkTag.append(linkTag.find_elements(By.CLASS_NAME, "tout__titleLink"))
            print("====================", getLinkTag)
            linkPage = ""
            for link in getLinkTag:
                try:
                    if len(link) > 0:
                        print(link[0].get_attribute("title").lower()[:len(flowerName) + 1])
                        if f"{flowerName.lower()}," == link[0].get_attribute("title").lower()[:len(flowerName) + 1]:
                            linkPage = link[0]
                            print('I GOT THE EXACT NAME --------------')
                except:
                    continue
            # linkPages = [link[0].get_attribute('href') if len(link)!= 0 else print('') for link in getLinkTag]
            linkDriver = webdriver.Chrome(service=ser)
            if flowerName == "Iris":
                linkDriver.get(getLinkTag[2][0].get_attribute("href"))
            else:
                linkDriver.get(linkPage.get_attribute("href"))

            try:
                tableData = WebDriverWait(linkDriver, 10).until(
                    EC.presence_of_element_located((By.CLASS_NAME, "entityCard__table"))
                )
                # print("Table Content: ", tableData)
                tBodyElements = tableData.find_elements(By.CLASS_NAME, "field-row")
                # print("Table Body Elements: ", tBodyElements)
                flowerData = {}
                for tBody in tBodyElements:
                    tableRow = tBody.find_element(By.XPATH, "./tr")
                    tableData = tableRow.find_elements(By.TAG_NAME, "td")
                    data = tableData[1].find_element(By.XPATH, "./ul")
                    liElements = data.find_elements(By.TAG_NAME, "li")
                    text = [li.text for li in liElements]
                    text = ", ".join(text)
                    flowerData[tableData[0].text] = text
                    if tableData[0].text == "GENUS NAME":
                        flower_obj["botanical_name"] = text
                    elif tableData[0].text == "PLANT TYPE":
                        flower_obj["plant_type"] = text
                    elif tableData[0].text == "LIGHT":
                        flower_obj["sun_exposure"] = text
                    elif tableData[0].text == "FLOWER COLOR":
                        flower_obj["flower_color"] = text
                    elif tableData[0].text == "SPECIAL FEATURES":
                        flower_obj["special_features"] = text
                    elif tableData[0].text == "ZONES":
                        flower_obj["hardiness_zones"] = text
                    elif tableData[0].text == "SEASON FEATURES":
                        flower_obj["bloom_time"] = text
                    elif tableData[0].text == "HEIGHT":
                        flower_obj["height"] = text
                    elif tableData[0].text == "WIDTH":
                        flower_obj["width"] = text
                    # f.write(tableData[0].text + ": " + text + "\n")
                # print("This is flower data: ", flowerData)
                print(flower_obj)

                containerContent = WebDriverWait(linkDriver, 10).until(
                    EC.presence_of_element_located((By.CLASS_NAME, "articleContainer__content"))
                )
                # print("Container Content: ", containerContent)
                mainContentDiv = containerContent.find_element(By.XPATH, "./following-sibling::div")
                secondHeaders = mainContentDiv.find_elements(By.TAG_NAME, "h2")
                headerTag = ""
                for i in range(len(secondHeaders)):
                    print(secondHeaders[i].text)
                    if "Care Must-Knows" in secondHeaders[i].text:
                        print("i got it")
                        f.write(flowerName + '\n')
                        headerTag = secondHeaders[i]
                    elif "Planting Must-Knows" in secondHeaders[i].text.strip():
                        print("I got it")
                        f.write(flowerName + '\n')
                        headerTag = secondHeaders[i]
                    elif f"{flowerName} Care" in secondHeaders[i].text.strip():
                        print("I got it")
                        f.write(flowerName + '\n')
                        headerTag = secondHeaders[i]
                    elif f"Seasonal {flowerName} Care" in secondHeaders[i].text.strip():
                        print("I got it")
                        f.write(flowerName + '\n')
                        headerTag = secondHeaders[i]
                contentDivs = headerTag.find_elements(By.XPATH, './following-sibling::div[@class="paragraph"]')
                iterator = 0
                plantCareText = ""
                while True:
                    if contentDivs[iterator].tag_name == "div" and contentDivs[iterator].get_attribute("class") == "paragraph":
                        print("--------------I AM A DIV-----------------")
                        if contentDivs[iterator].find_element(By.TAG_NAME, "p").text != 'Related: Annual Care Guide':
                            plantCareText += contentDivs[iterator].find_element(By.TAG_NAME, "p").text
                            print(contentDivs[iterator].find_element(By.TAG_NAME, "p").text)
                        iterator += 1
                    else:
                        break
                [print(header.text) if "Care Must-Knows" in header.text else print("") for header in secondHeaders]
                if flower_obj != {}:
                    # collection.find_one_and_delete({ "botanical_name" : flower_obj["botanical_name"] })
                    print(plantCareText)
                    if plantCareText != '':
                        print('----------------------------')
                        flower_obj['plant_care'] = plantCareText
                        collection.insert_one(flower_obj)
            except:
                linkDriver.quit()
    except:
        print("no page found")
        driver.quit()
    driver.quit()

# for flower in script2_flowerNames.flowerNames:
main('Sunflower')
    # time.sleep(5)
f.close()