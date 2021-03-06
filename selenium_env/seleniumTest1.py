from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from pymongo import MongoClient
import script1_flowerNames
import time

PATH = r"C:\Users\N B C\Downloads\chromedriver.exe"

cluster = MongoClient("mongodb+srv://osamanadeem:bmw600bmw600@cluster0.8ke0m.mongodb.net/db_flowers?retryWrites=true&w=majority")
db = cluster['db_flowers']
collection = db['flowers']


# driver.maximize_window()

# driver = webdriver.Chrome(PATH)
# array = ['daisies', 'roses']

# flowerName = "Hydrangeas"


# f = open(f"{flowerName}.txt", "w")

def main(flowerName):
    ser = Service(PATH)
    driver = webdriver.Chrome(service=ser)
    flower_obj = {}
    driver.get(f"https://www.almanac.com/plant/{flowerName}")
    if flowerName == 'shasta-daisies':
        flowerName = 'Daisy'
    elif flowerName == 'Roses':
        flowerName = 'Rose'
    elif flowerName == 'Lilies':
        flowerName = 'Lily'
    elif flowerName == 'Daffodils':
        flowerName = 'Daffodil'
    else:
        flower_obj["flower_name"] = flowerName
    try:
        botanical_name = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CLASS_NAME, "field--name-field-botanicalname"))
        )

        field__label = botanical_name.find_element(By.CLASS_NAME , 'field__label').text
        print(field__label)
        # f.write(field__label)
        field__item = botanical_name.find_element(By.CLASS_NAME, 'field__item').text
        print(field__item)
        # f.write(": " + field__item + "\n")
        flower_obj['botanical_name'] = field__item

        # modify this
        try:

            plant_type = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.CLASS_NAME, "field--name-field-plant-type-term"))
            )
            if plant_type:
                field__label = plant_type.find_element(By.CLASS_NAME, 'field__label').text
                print(field__label)
                # f.write(field__label)
                field__items = plant_type.find_elements(By.CLASS_NAME, 'field__item')
                field__items_links = [div.find_element(By.TAG_NAME, "a").text for div in field__items]
                # f.write(": " + ", ".join(field__items_links) + "\n")
                flower_obj['plant_type'] = ", ".join(field__items_links)
                print(field__items_links)
        except:
            flower_obj["plant_type"] = ""

        # modify this
        try:
            sun_exposure = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.CLASS_NAME, "field--name-field-sun-exposure-term"))
            )
            
            if sun_exposure:
                # content = sun_exposure.find_elements_by_tag_name("div")
                # content = sun_exposure.find_element_by_xpath('/div[@class="field__label"')
                # print(content.text)
                # sunExposureValue = [];
                field__label = sun_exposure.find_element(By.CLASS_NAME, 'field__label').text
                print(field__label)
                # f.write(field__label)
                field__items = sun_exposure.find_elements(By.CLASS_NAME, 'field__item')
                field__items_links_text = [div.find_element(By.TAG_NAME, "a").text for div in field__items]
                print(field__items_links_text)
                # f.write(": " + ", ".join(field__items_links_text) + "\n")
                flower_obj['sun_exposure'] = ", ".join(field__items_links_text)
                print(flower_obj)
        except:
            flower_obj["sun_exposure"] = ""
        # for div in content:
        #     # field__items = div.find_element_by_xpath('.//following-sibling::div')
        #     # field__items = div.find_element_by_xpath('.//div[@class="field__item"]')
        #     field__items = div.find_elements_by_class_name('field__item')
        #     sunExposureValue.append(div.text)
        # print(sunExposureValue)

        # modify this and if ph varies then give more detail from the following content
        try:
            soil_ph = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.CLASS_NAME, "field--name-field-soil-ph-term"))
            )

            if soil_ph:
                field__label = soil_ph.find_element(By.CLASS_NAME, 'field__label').text
                print(field__label)
                # f.write(field__label)
                field__items = soil_ph.find_elements(By.CLASS_NAME, 'field__item')
                field__items_links = [div.find_element(By.TAG_NAME, "a").text for div in field__items]
                print(field__items_links)
                # f.write(": " + ", ".join(field__items_links) + "\n")
                flower_obj['soil_ph'] = ", ".join(field__items_links)
        except:
            flower_obj["soil_ph"] = ""
        # modify this
        try:
            bloom_time = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.CLASS_NAME, "field--name-field-bloom-time-term"))
            )

            if bloom_time:
                field__label = bloom_time.find_element(By.CLASS_NAME, 'field__label').text
                print(field__label)
                # f.write(field__label)
                field__items = bloom_time.find_elements(By.CLASS_NAME, 'field__item')
                field__items_links = [div.find_element(By.TAG_NAME, "a").text for div in field__items]
                print(field__items_links)
                # f.write(": " + ", ".join(field__items_links) + "\n")
                flower_obj['bloom_time'] = ", ".join(field__items_links)
        except:
            flower_obj["bloom_time"] = ""
        # modify this
        try:

            flower_color = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.CLASS_NAME, "field--name-field-flower-color-term"))
            )
            if flower_color:
                field__label = flower_color.find_element(By.CLASS_NAME, 'field__label').text
                print(field__label)
                # f.write(field__label)
                field__items = flower_color.find_elements(By.CLASS_NAME, 'field__item')
                field__items_links = [div.find_element(By.TAG_NAME, "a").text for div in field__items]
                print(field__items_links)
                # f.write(": " + ", ".join(field__items_links) + "\n")
                flower_obj['flower_color'] = ", ".join(field__items_links)
        except:
            flower_obj["flower_color"] = ""
        # modify this
        try:

            harding_zone = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.CLASS_NAME, "field--name-field-hardiness-zone-term"))
            )
            if harding_zone:

                field__label = harding_zone.find_element(By.CLASS_NAME, 'field__label').text
                print(field__label)
                # f.write(field__label)
                field__items = harding_zone.find_elements(By.CLASS_NAME, 'field__item')
                field__items_links = [div.find_element(By.TAG_NAME, "a").text for div in field__items]
                print(field__items_links)
                # f.write(": " + ", ".join(field__items_links) + "\n")
                flower_obj['hardiness_zones'] = ", ".join(field__items_links)
        except:
            flower_obj["hardiness_zones"] = ""
        # modify this
        try:
            special_features = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.CLASS_NAME, "field--name-field-special-features-term"))
            )
            if special_features:
                field__label = special_features.find_element(By.CLASS_NAME, 'field__label').text
                print(field__label)
                # f.write(field__label)
                field__items = special_features.find_elements(By.CLASS_NAME, 'field__item')
                field__items_links = [div.find_element(By.TAG_NAME, "a").text for div in field__items]
                print(field__items_links)
                # f.write(": " + ", ".join(field__items_links) + "\n")
                flower_obj['special_features'] = ", ".join(field__items_links)
        except:
            flower_obj["special_features"] = ""

        # planting
        content_div = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((
                By.CLASS_NAME, 
                "field--name-field-planting"
                ))
        )
        # //div[@class='block-field-blocknodeplantfield-planting']/div[@class='block__content']/div[@class='field--name-field-planting']
        # print(content_div)
        # nested_div = content_div.find_elements(By.XPATH, './/div[@class="block__content"]//following::div')
        label = content_div.find_element(By.CLASS_NAME, "field__label").text
        print(label)
        # f.write(label)

        textContentDiv = content_div.find_element(By.CLASS_NAME, "field__item")
        # findAllHeadings = textContentDiv.find_elements(By.TAG_NAME, "h3")
        # firstHeader = textContentDiv.find_element(By.XPATH, ".//child::h3[2]")
        # print(firstHeader.text)

        getContent = []
        headerCount = 1
        ulCount = 1
        pCount = 1
        iterator = 0
        # f.write("Plant Care: ")
        flower_obj["plant_care"] = ""
        tagName = ["h3", "p", "ul"]
        plantCareText = ""
        checkTag = textContentDiv.find_elements(By.XPATH, './/*')
        # while 1:
        for element in checkTag:
            if element.tag_name == 'h3':
                plantCareText += element.text + '\n'
                # print('i am h3\n')
                # print(element.text + '\n')
                # checkTag = checkTag.find_element(By.XPATH, './following-sibling::ul')
                # print(checkTag)
            elif element.tag_name == "ul":
                # print('i was ul\n')
                getList = element.find_elements(By.XPATH, "./child::li")
                if len(getList) > 0:
                    for li in getList:
                        if li.text not in plantCareText:
                            # print(li.text + '\n')
                            plantCareText += li.text
                    # plantCareText += '\n'
                # checkTag = checkTag.find_element(By.XPATH, './following-sibling')
            elif element.tag_name == "p":
                # print('i was p\n', element.text)
                plantCareText += element.text
                # checkTag = checkTag.find_element(By.XPATH, './following-sibling')
            elif element.tag_name == "div":
                print('i am div')
                break

        # print(plantCareText)
        if flower_obj != {}:
            # collection.find_one_and_delete({ "botanical_name" : flower_obj["botanical_name"] })
            # print(plantCareText)
            if plantCareText != '':
                flower_obj['plant_care'] = plantCareText
                print(flower_obj)
                found = collection.find_one_and_update({ "flower_name": flowerName }, { '$set': flower_obj })
                print(f"------------{found}")
                # collection.insert_one(flower_obj)
        # f.close()


    except:
        print("--------------I WAS HERE AND DID NOT FIND ANYTHING--------------------")
        if flower_obj != {}:
            # collection.find_one_and_delete({ "botanical_name" : flower_obj["botanical_name"] })
            print(plantCareText)
            if plantCareText != '':
                flower_obj['plant_care'] = plantCareText
                # collection.insert_one(flower_obj)
                print(flower_obj)
                found = collection.find_one_and_update({ "flower_name": flowerName }, { '$set': flower_obj })
                print(f"------------{found}")
        driver.quit()
    driver.quit()

for flower in script1_flowerNames.flowerNames:
    main(flower)
    time.sleep(5)