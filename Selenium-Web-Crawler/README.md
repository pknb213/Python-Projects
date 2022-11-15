# Web Shopping Mall Crawler
해당 프로젝트는 2019년 과제로 만들게 된 크롤링으로 \
아래 URL인 G-market과 GS-shop의 아이템을 크롤링하기 위한 목적으로 만들었다.
Gmarket: https://m.gmarket.co.kr/n/superdeal?categoryCode=400000
Gsshop: https://www.gsshop.com/shop/sect/sectL.gs?sectid=1378

## Description
Shopping mall Crawling Python Code

## Environment
- Database : MongoDB
- Library
    - Lxml : 정적 페이지에서 사용
    - Selenium : 동적 페이지 접근시에 사용
- 분산 처리
    - Async.io : 비동기 처리
    - motor : MongoDB 분산 처리 드라이버 라이브러리
- Crawling 대상 : G Market, GS Shop
- Chrome Driver : https://sites.google.com/a/chromium.org/chromedriver/home

## Prerequisite
Module|Version|Description|
---|---|---|
python|3.6|Basic
lxml|4.5.1|Crawling
selenium|3.141.0|Crawling
motor|2.4.0|Async Mongo driver
pymongo|3.12.0|Database
chrome driver|Your Chrome|Dynamic Page

## 수집 프로세스 (Extract Process)

크롤링에 앞서 하드코딩에 필요한 정보가 있다. 수집을 하고자 하는 쇼핑몰의 URL 및 상품 정보를 어떤 카테고리에서 가져올지 그리고 상품의 정보가 있는 태그를 어떻게 접근할 것 인가 등 고려할 점이 많다. 그리고 쇼핑몰 사이트가 변경이 있을 경우, 이 작업을 최소한으로 할지, 페이지가 동적일 경우 그리고 상품 정보가 상품 정보 에러로 예외처리 등 기술적으로도 생각할 점이 많다.

우선 최대한 간단한 수집 프로세스로서 쇼핑몰 URL 및 상품 태그 정보를 저장하고, 해당 정보를 토대로 크롤링을 하기로 한다.

아래 코드는 두 가지 쇼핑몰의 URL과 수집하고자 하는 카테고리를 URL Parameter로서 각 비동기로 접근하여 상품 정보를 Xpath를 이용하여 긁어 하나의 리스트로 저장한 후, 비동기 Mongo Instert를 이용하여 적재한다.

정적 페이지의 경우 **lxml**를 이용, 동적 페이지의 경우 **selenium chrome headless driver** 이용.

## Usage
1. pip install -r requirements.txt
2. install chrome
3. download chrome driver
4. execute

예전에 만든거라서 쇼핑몰 상품 html 관련해서 변경 해주셔야 될 것 같습니다.
main.py에서 주석처리해서 수집, 적재를 별도로 할 수 있습니다.
Selenium의 사용은 동적 페이지일 경우를 위해 사용했으며 페이지가 동적이 아니면 lxml만 사용해서 더 빠르게 수집할 수 있습니다.
코드 내에 업로드 되어있는 chome driver의 경우 window용 입니다.
