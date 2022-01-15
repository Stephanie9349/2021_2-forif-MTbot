import re
from time import sleep
from getpass import getuser
from selenium import webdriver

def recommend_product(product: str):
    # 사용자 입력 상품
    #product = open("product.txt", 'r')

    # 웹 드라이버 옵션 생성
    options = webdriver.ChromeOptions()
    options.add_argument('headless')

    # 웹 드라이버 생성
    driver = webdriver.Chrome(f'/Users/{getuser()}/chromedriver', options=options) # Chrome 97
    driver.implicitly_wait(10)

    # 네이버 쇼핑 사이트 접속
    driver.get('https://shopping.naver.com/home/p/index.naver')
    driver.implicitly_wait(10)

    # 디스코드로부터 입력 받은 상품 검색하기
    search_box = driver.find_element(by='xpath', value='/html/body/div[1]/div[1]/div/div[2]/div/div[2]/div/div[1]/form/fieldset/div[1]/input[1]')
    #search_box.send_keys(product.readline())
    search_box.send_keys(product)
    search_button = driver.find_element(by='xpath', value='/html/body/div[1]/div[1]/div/div[2]/div/div[2]/div/div[1]/form/fieldset/div[1]/a[2]')
    search_button.click()
    driver.implicitly_wait(10)
    

    # 검색 후 가격 비교 목록 보기
    #subfilter_button = driver.find_element(by='xpath', value='/html/body/div/div/div[2]/div[2]/div[3]/div[1]/div[1]/ul/li[2]/a')
    subfilter_button = driver.find_elements(by='class name', value='subFilter_filter__3Y-uy')[1]
    subfilter_button.click()
    driver.implicitly_wait(10)

    # 한 페이지 내 상품 개수를 20개로 조정하기
    #subfilter_select_box = driver.find_element(by='xpath', value='/html/body/div/div/div[2]/div[2]/div[3]/div[1]/div[1]/div/div[2]/div[3]/a')
    subfilter_select_box = driver.find_elements(by='class name', value='subFilter_btn_select__K6F79')[1]
    subfilter_select_box.click()
    driver.implicitly_wait(10)
    #subfilter_layer = driver.find_element(by='xpath', value='/html/body/div/div/div[2]/div[2]/div[3]/div[1]/div[1]/div/div[2]/div[3]/ul/li[1]/a')
    subfilter_layer = driver.find_elements(by='class name', value='subFilter_select__1eEJS')[7]
    subfilter_layer.click()
    driver.implicitly_wait(10)

    # 한 페이지 내 최저 금액 불러오기
    prices = []
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    driver.implicitly_wait(10)
    sleep(2) # stale 문제 방지
    #for i in range(1, 21):
        #price = driver.find_element(by='xpath', value=f'/html/body/div/div/div[2]/div[2]/div[3]/div[1]/ul/div/div[{i}]/li/div[1]/div[2]/div[2]/strong/span/span[2]').text
    for i in range(0, 20):
        price = driver.find_elements(by='class name', value='price_num__2WUXn')[i]
        price = int(''.join(re.findall(pattern=r'[0-9]', string=price.text)))
        prices.append(price)
        driver.implicitly_wait(10)

    # 최저 금액 상품 클릭하기
    #cheapest_product = driver.find_element(by='xpath', value=f'/html/body/div/div/div[2]/div[2]/div[3]/div[1]/ul/div/div[{prices.index(min(prices)) + 1}]/li/div[1]/div[2]/div[1]/a')
    cheapest_product = driver.find_elements(by='xpath', value="//div[@class='basicList_title__3P9Q7']/a")[prices.index(min(prices))]
    cheapest_product.click()
    driver.implicitly_wait(10)

    # 판매가와 배송비를 합쳐 최저가인 사이트 불러오기
    driver.switch_to.window(driver.window_handles[-1])

    total_prices = []

    product_prices = driver.find_elements(by='class name', value='productByMall_price__3F_YF')
    delivery_fees = driver.find_elements(by='class name', value='productByMall_gift__W92gX')
    total_prices = []

    if driver.find_element(by='xpath', value='/html/body/div/div/div[2]/div[2]/div[2]/div[1]/div/div[2]/div[2]/table/thead/tr/th[2]').text == '배송비 포함가':
        is_including_fee = True
    else:
        is_including_fee = False

    for i in range(0, len(product_prices)):
        product_prices[i] = int(''.join(re.findall(pattern=r'[0-9]', string=product_prices[i].text)))
        if delivery_fees[i].text == '무료배송':
            delivery_fees[i] = int(''.join(re.findall(pattern=r'[0-9]', string='0원')))
        else:
            delivery_fees[i] = int(''.join(re.findall(pattern=r'[0-9]', string=delivery_fees[i].text)))
        if is_including_fee:
            total_prices.append(product_prices[i])
        else:
            total_prices.append(product_prices[i] + delivery_fees[i])
        driver.implicitly_wait(10)

    # 최저가 상품, 사이트 정보 정리
    #cheapest_product_name = driver.find_element(by='xpath', value='/html/body/div/div/div[2]/div[2]/div[1]/h2').text
    cheapest_product_name = driver.find_element(by='xpath', value='/html/body/div/div/div[2]/div[2]/div[1]/h2').text
    cheapest_price = f'{product_prices[total_prices.index(min(total_prices))]}원'
    if is_including_fee:
        cheapest_fee = "배송비가 포함된 가격이에요!"
    else:
        cheapest_fee = f'{delivery_fees[total_prices.index(min(total_prices))]}원'
    #cheapest_site = driver.find_element(by='xpath', value=f'/html/body/div/div/div[2]/div[2]/div[2]/div[1]/div/div[2]/div[2]/table/tbody/tr[{total_prices.index(min(total_prices)) + 1}]/td[4]/a').get_attribute('href')
    cheapest_site = driver.find_elements(by='class name', value='productByMall_btn_buy__P4W5Q')[total_prices.index(min(total_prices))].get_attribute('href')

    # 디스코드로 보낼 결과 메시지
    result = open("recommended_product.txt", 'w')
    result.write(
        f'''
아래 상품을 추천해요!
상품명: {cheapest_product_name}
판매가: {cheapest_price}
배송비: {cheapest_fee}
사러가기:
{cheapest_site}
        '''
    )
    #product.close()
    result.close()
    driver.quit()
