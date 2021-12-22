from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from pymongo import MongoClient
import time

PATH = r"C:\Users\N B C\Downloads\chromedriver.exe"

cluster = MongoClient("mongodb+srv://osamanadeem:bmw600bmw600@cluster0.8ke0m.mongodb.net/db_flowers?retryWrites=true&w=majority")
db = cluster['db_flowers']
collection = db['flowers']

ser = Service(PATH)
driver = webdriver.Chrome(service=ser)

flower_names = ['Daisy', 'Rose', 'Iris', 'Daffodils', 'Orchid', 'Tulip', 'Sunflower', 'Cyclamen', 'Carnation', 'Poppy', 'Pansy', 'Violet', 'Mimosa', 'Lily', 'Hyacinth', 'Anemone', 'Gladiolus', 'Forget-me-not', 'Virginia Bluebells', 'Bougainvillea', 'Buttercup', 'Christmas Cactus', 'Camellia', 'Chrysanthemum', 'Cockscomb', 'Confederate rose', 'Crocus', 'Dahlia', 'Eglantine', 'Flamboyant', 'Foxglove', 'Geranium', 'Gerbera Daisy', 'Hibiscus', 'Honeysuckle vine', 'Hop Tree', 
'Jasmine', 'Lavender', 'Lilac', 'Lotus', 'Magnolia Tree', 'Marigold', 'Morning Glory', 'Orange rose', 'Peony', 'Primrose', 'Snapdragon', 'Snowdrop', 'Tuberose Begonia', 'Apricot blossom', 'Cherry blossom', 'Dandelion', 'Moss rose', 'Shameplant', 'Hydrangea']
# driver.maximize_window()

# driver = webdriver.Chrome(PATH)

flower_obj = {}

flowerName = "Moss rose"
# def main (flowerName):
driver.get(f"https://www.bhg.com/bin/plants/?name={flowerName}")

# f = open(f"{flowerName}.txt", "w")

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
        # linkDriver.get(getLinkTag[2][0].get_attribute("href"))
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
            careHeader = 0
            headerTag = ""
            for i in range(len(secondHeaders)):
                print(secondHeaders[i].text)
                if "Care Must-Knows" in secondHeaders[i].text:
                    print("i got it")
                    careHeader = i
                    headerTag = secondHeaders[i]
                elif "Planting Must-Knows" in secondHeaders[i].text.strip():
                    print("I got it")
                    headerTag = secondHeaders[i]
                elif f"{flowerName} Care" in secondHeaders[i].text.strip():
                    print("I got it")
                    headerTag = secondHeaders[i]
                    # print(f"INDEX IS: {careHeader}")
                elif f"Seasonal {flowerName} Care" in secondHeaders[i].text.strip():
                    print("I got it")
                    headerTag = secondHeaders[i]
                    # print(f"INDEX IS: {careHeader}")
            # print('===========These are the divs------------', headerTag.find_elements(By.XPATH, './following-sibling::div'))
            contentDivs = headerTag.find_elements(By.XPATH, './following-sibling::div')
            iterator = 0
            plantCareText = ""
            while True:
                if contentDivs[iterator].tag_name == "div" and contentDivs[iterator].get_attribute("class") == "paragraph":
                    # print("--------------I AM A DIV-----------------")
                    # print(contentDivs[iterator].find_element(By.TAG_NAME, "p").text)
                    plantCareText += contentDivs[iterator].find_element(By.TAG_NAME, "p").text
                    iterator += 1
                    # if contentDivs[iterator].get_attribute('class') != '':
                    #     print(checkTag.get_attribute('class'))
                    #     headerTag = checkTag
                    # else:
                    #     continue
                # elif checkTag.tag_name == "h2":
                #     break
                # elif contentDivs[iterator].get_atrribute('class') == 'div-sm-highImpact':
                #     print('yohooo')
                else:
                    break
            [print(header.text) if "Care Must-Knows" in header.text else print("") for header in secondHeaders]
            if flower_obj != {}:
                result = collection.find_one_and_delete({ "botanical_name" : flower_obj["botanical_name"] })
                print(plantCareText)
                if plantCareText != '':
                    flower_obj['plant_care'] = plantCareText
                    collection.insert_one(flower_obj)
        except:
            linkDriver.quit()
    # field__item = botanical_name.find_element(By.CLASS_NAME, 'field__item').text
    # print(field__item)

    # modify this
    # plant_type = WebDriverWait(driver, 10).until(
    #     EC.presence_of_element_located((By.CLASS_NAME, "field--name-field-plant-type-term"))
    # )


except:
    print("no page found")
    driver.quit()

# linkDriver.quit()
driver.quit()

# for flower in flower_names:
#     main(flower.lower())    