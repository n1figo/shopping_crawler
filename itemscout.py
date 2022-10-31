# https://colab.research.google.com/drive/1-kXetzPDefEi_IVvLO8UuviN4jnOvmuV#scrollTo=iVMUNP3iYkOe


import pandas as pd
import numpy as np
import matplotlib.pyplot as plt


from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
# from pyvirtualdisplay import Display
from datetime import datetime
# from GetFirmCode import GetCode
import requests, os, itertools, json, time, sys, re, sqlite3
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt


# 맥에서 pip 설치
# curl https://bootstrap.pypa.io/get-pip.py -o get-pip.py
# 맥에서 pip install 
# python -m pip install bs4
# 맥 가상환경 설정 : https://hidekuma.github.io/python/virtualenv/virtualenvwrapper/python-virtualenv-wrapper/
# 가상환경 설정 : python -m venv neres_test
# 가상환경 진입 : source [가상환경이름] /bin/activate


# 1. 손익계산서 크롤링
class GetItemScoutWebpage:
    def __init__(self):
        self.BASE_DIR = os.path.dirname(os.path.abspath('__file__'))
        print('='*50)
        print('--- 크롤링을 시작합니다. ---')
        print('현재 경로는',self.BASE_DIR,'입니다.')
        print('='*50)
        

    def run(self):
      self.getItemScout()


    def getItemScout(self):
      chrome_options = webdriver.ChromeOptions()

      #지정한 user-agent로 설정합니다.
      user_agent = "Mozilla/5.0 (Linux; Android 9; SM-G975F) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.83 Mobile Safari/537.36"
      chrome_options.add_argument('user-agent=' + user_agent)

      # options.add_argument('headless') #headless모드 브라우저가 뜨지 않고 실행됩니다.
      chrome_options.add_argument('--window-size= x, y') #실행되는 브라우저 크기를 지정할 수 있습니다.
      chrome_options.add_argument('--start-maximized') #브라우저가 최대화된 상태로 실행됩니다.
      chrome_options.add_argument('--start-fullscreen') #브라우저가 풀스크린 모드(F11)로 실행됩니다.
      chrome_options.add_argument('--blink-settings=imagesEnabled=false') #브라우저에서 이미지 로딩을 하지 않습니다.
      chrome_options.add_argument('--mute-audio') #브라우저에 음소거 옵션을 적용합니다.
      chrome_options.add_argument('incognito') #시크릿 모드의 브라우저가 실행됩니다.


      # 기본 설정
      # chrome_options = webdriver.ChromeOptions()
      # chrome_options.add_argument('--headless')
      # chrome_options.add_argument('--window-size=1920x1080')
      # chrome_options.add_argument('--no-sandbox')
      # chrome_options.add_argument('--disable-gpu')
      # chrome_options.add_argument('--disable-dev-shm-usage')
      # chrome_options.add_argument('--user-agent="Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.125 Safari/537.36"')

      # 윈도우버전 --> 크롬드라이버 교체할 것
      chrome_path = os.path.join(self.BASE_DIR, 'chromedriver')
      # 맥버전
      # 리눅스버전
      chrome_path = self.BASE_DIR
      # chrome_path = os.path.join(self.BASE_DIR, 'chromedriver2')
      # print('크롬 설치경로입니다:',chrome_path)
      # self.driver = webdriver.Chrome(executable_path=chrome_path, options=chrome_options)

      # colab버전
      self.driver = webdriver.Chrome('chromedriver',chrome_options=chrome_options)
      # print('---크롤링 준비가 완료되었습니다.---')

      # 1.1. 종목코드 직접입력
      # url 정의
      url = 'https://itemscout.io/category?c=6,142,346'
      self.driver.get(url)
     

      # PC웹버전 클릭
      time.sleep(5)
      pc_xpath = '/html/body/div[1]/div/div/div/div[1]/div/a'
      pc_web = self.driver.find_element_by_xpath(pc_xpath)
      pc_web.click()


      # 3번째 카테고리 풀리스트 3차분류 클릭
      # 3번째 카테고리 첫번째 입력
      third_cate_xpath = '/html/body/div[1]/div/div/div[1]/main/div/div/div/div[1]/div[1]/div[2]/div/div/div[3]/div[1]'
      third_cate = self.driver.find_element_by_xpath(third_cate_xpath)
      third_cate.click()

      # 3번째 카테고리 리스트 출력 -> 몇개나 있나?
      third_full_list_xpath = '/html/body/div[1]/div/div/div[2]'

      third_elem_list = self.driver.find_element_by_xpath(third_full_list_xpath)
      print(third_elem_list)


      # tbl = driver.find_element_by_xpath(테이블주소).get_attribute('outerHTML')

      """
      # 테이블 긁어오기 
      soup = BeautifulSoup(tbl, 'html.parser')
      # print(soup)

      # 테이블 내용 파싱
      l = []
      table_all = soup.find('table',{'class':'genTbl reportTbl'})

      '/html/body/div[1]/div/div/div[2]/div/div/div[2]/div'
      """




    def getIS(self):
      # 분기 손익계산서 파싱
      df_is_recent, driver = self.get_finance_info_start()  

      # 연간손익계산서 파싱
      tbl, driver = self.get_finance_info_year(driver)

      # 분기 손익계산서 최근 합 구하고 4분기, 최근 4분기 합 내보내기
      df_is_recent_1yr_ttm, df2_T = self.make_recent_1year(df_is_recent, 'df_is_recent_1year_ttm.csv', 'df2_T.csv')


      return df_is_recent_1yr_ttm, driver


    # 최근 1년간 4개 분기 손익계산서 합산
    def make_recent_1year(self, df, filename1,filename2):
      # 세로 합 구하기
      df2 = df.copy()
      
      # 데이터 유형 변경 (행 합 산출)
      for idx, col in enumerate(df2.columns):
        if idx >= 1:
          df2[col] = df2[col].str.replace('-','0')
          df2[col] = df2[col].astype(float)

      # 컬럼이름 추가
      col = df2.columns.tolist()[1] + '_TTM'

      # 최근4분기 합 산출
      df2[col] = df2.iloc[:,1:].sum(axis=1)

      filename0 = os.path.join(self.BASE_DIR, 'df2.csv')
      df2.to_csv(filename0)

      # 행/열변환해서 저장
      df2_T = df2.T

      # 컬럼정하기 및 기존 0행 삭제
      df2_T.columns = df2_T.iloc[0,:]
      df2_T = df2_T.iloc[1:,:]

      # 최근 4분기 합을 별도 데이터프레임으로 반환
      df_is_recent_1yr_ttm = df2_T.iloc[[-1]]
      df_is_recent_1yr_ttm = pd.DataFrame(df_is_recent_1yr_ttm)

      # csv로 내보내기
      filename11 = os.path.join(self.BASE_DIR, filename1)
      filename22 = os.path.join(self.BASE_DIR, filename2)
      df_is_recent_1yr_ttm.to_csv(filename11)
      df2_T.to_csv(filename22)

      return df_is_recent_1yr_ttm, df2_T

     
    def get_finance_info_year(self, driver):
      # annual 버튼 클릭
      # print('--- 연도 버튼을 클릭합니다.--- ')
      annual_button = '/html/body/div[5]/section/div[8]/div[1]/a[1]'
      elem_year = driver.find_element_by_xpath(annual_button)
      elem_year.click()
      
      # 2. 재무제표 저장
      # 2.1. 연간 손익계산서 저장
      테이블주소 = '/html/body/div[5]/section/div[9]/table'
      #  '/html/body/div[5]/section/div[9]/table'
      tbl = driver.find_element_by_xpath(테이블주소).get_attribute('outerHTML')

      # 테이블 긁어오기 
      soup = BeautifulSoup(tbl, 'html.parser')
      # print(soup)

      # 테이블 내용 파싱
      l = []
      table_all = soup.find('table',{'class':'genTbl reportTbl'})
      # print('---테이블을 출력합니다.=---')
      # print(table_all)
      # 제목 tbody
      table_contents = table_all.find_all('tbody')
      # print('---제목 및 내용을 출력합니다.---')
      # print(len(table_contents))
      
      # 행 출력
      for idx, trs in enumerate(table_contents):
        if idx == 0:
          """제목행(연월일)을 리스트로 저장"""
          single_year = [span.text for span in trs.find_all('span')]
          single_year = single_year[1:] # period_year 제외
          single_month_day = [div.text for div in trs.find_all('div')]
          # print('---single_row---')
          # 연월일 돌리면서 계정명 추가
          single_date_all = [y + m_d for y, m_d in zip(single_year, single_month_day)] 
          # 영문삭제
          single_date_all = [re.sub('[^0-9/]','',one) for one in single_date_all]
          # 올해연도 추가
          # single_date_all[0] = str(datetime.today().year) + single_date_all[0]
          # 컬럼정리를 위해 1개 컬럼 추가
          single_date_all = ['finance_account'] + single_date_all
          # single_date_all = 'finance_account' + single_date_all[0] [ymd[0] for ymd in single_date_all]
          # print(single_date_all)
          # single_row = [tr.text for tr in trs]
          l.append(single_date_all)
          
        else:
          """본문행일 경우, for loop 돌린후 리스트로 저장"""
          # print('%d 번째 행입니다.' % idx)
          # 여러 tr 들이 섞여 있음
          # tbody가 있을 경우, for loop 한번 더 돌려서 데이터 저장
          for tr in trs.find_all('tr'):
            """tbody가 있으면 한번 더 돌려서 뽑아냄"""
            if tr.find('tbody'):
              continue

            else:
              """tbody가 없으면 바로 뽑아냄"""
              tds = tr.find_all('td')
              # print('---한줄을 출력합니다.---')
              single_row = [td.text for td in tds]
              # print(single_row)
              l.append(single_row)

      # 파일 떨구기
      filename = os.path.join(self.BASE_DIR, 'sample_year.csv')
      df = pd.DataFrame(l)
      # 헤더지정
      df.columns = df.iloc[0]
      df = df.iloc[1:]
      df.to_csv(filename)

      # 드라이버 넘기기
      driver = self.driver

      return df, driver
        
    def get_finance_info_start(self):
      # 기본 설정
      chrome_options = webdriver.ChromeOptions()
      chrome_options.add_argument('--headless')
      chrome_options.add_argument('--window-size=1920x1080')
      chrome_options.add_argument('--no-sandbox')
      chrome_options.add_argument('--disable-gpu')
      chrome_options.add_argument('--disable-dev-shm-usage')
      chrome_options.add_argument('--user-agent="Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.125 Safari/537.36"')

      # 윈도우버전 --> 크롬드라이버 교체할 것
      chrome_path = os.path.join(self.BASE_DIR, 'chromedriver')
      # 맥버전
      # 리눅스버전
      chrome_path = self.BASE_DIR
      # chrome_path = os.path.join(self.BASE_DIR, 'chromedriver2')
      # print('크롬 설치경로입니다:',chrome_path)
      # self.driver = webdriver.Chrome(executable_path=chrome_path, options=chrome_options)

      # colab버전
      self.driver = webdriver.Chrome('chromedriver',chrome_options=chrome_options)
      # print('---크롤링 준비가 완료되었습니다.---')

      # 1.1. 종목코드 직접입력
      # url 정의
      url = 'https://itemscout.io/category?c=6,142,346'
      self.driver.get(url)

      # 1.2. 기업명 클릭
      elem2 = self.driver.find_element_by_xpath("/html/body/div[5]/section/div/div[2]/div[2]/div[1]/a/span[2]")
      elem2.click()
      # print('--- 검색창을 찾았습니다. ---')

      # 1.3. Finaacials 클릭
      # iframe 확인
      # self.driver.switch_to.frame(self.driver.find_elements_by_tag_name("iframe"))
      self.driver.implicitly_wait(3)
      time.sleep(2)
      elem3 = self.driver.find_element_by_xpath('/html/body/div[5]/section/ul[1]/li[4]')
      # self.driver.execute_script("arguments[0].click();", elem3)
      elem3.click()

      # 2. 재무제표 저장
      # 2.1. 손익계산서 저장
      elem4 = self.driver.find_element_by_xpath('/html/body/div[5]/section/ul[2]/li[2]/a')
      elem4.click()
      
      테이블주소 = '/html/body/div[5]/section/div[9]/table'
      tbl = self.driver.find_element_by_xpath(테이블주소).get_attribute('outerHTML')

      # 테이블 긁어오기 
      soup = BeautifulSoup(tbl, 'html.parser')
      # print(soup)

      # 테이블 내용 파싱
      # headlines = soup.find_all('th')
      # print(headlines)
      l = []
      # single_row = []
      
      table_all = soup.find('table',{'class':'genTbl reportTbl'})
      # print('---테이블을 출력합니다.=---')
      # print(table_all)
      # 제목 tbody
      table_contents = table_all.find_all('tbody')
      # print('---제목 및 내용을 출력합니다.---')
      # print(len(table_contents))
      
      # 행 출력
      for idx, trs in enumerate(table_contents):
        if idx == 0:
          """제목행(연월일)을 리스트로 저장"""
          single_year = [span.text for span in trs.find_all('span')]
          single_year = single_year[1:] # period_year 제외
          single_month_day = [div.text for div in trs.find_all('div')]
          # print('---single_row---')
          # 연월일 돌리면서 계정명 추가
          single_date_all = [y + m_d for y, m_d in zip(single_year, single_month_day)] 
          # 영문삭제
          single_date_all = [re.sub('[^0-9/]','',one) for one in single_date_all]
          # 올해연도 추가
          # single_date_all[0] = str(datetime.today().year) + single_date_all[0]
          # 컬럼정리를 위해 1개 컬럼 추가
          single_date_all = ['finance_account'] + single_date_all
          # single_date_all = 'finance_account' + single_date_all[0] [ymd[0] for ymd in single_date_all]
          # print(single_date_all)
          # single_row = [tr.text for tr in trs]
          l.append(single_date_all)
          
        else:
          """본문행일 경우, for loop 돌린후 리스트로 저장"""
          # print('%d 번째 행입니다.' % idx)
          # 여러 tr 들이 섞여 있음
          # tbody가 있을 경우, for loop 한번 더 돌려서 데이터 저장
          for tr in trs.find_all('tr'):
            """tbody가 있으면 한번 더 돌려서 뽑아냄"""
            if tr.find('tbody'):
              continue
              # for tds in tr.find('tbody'):
              #   single_row = [td for td in tds]
              #   """# 여기가 문제였음!!"""
              #   print('---single_row출력합니다.---')
              #   print(single_row)
              #   l.append(single_row)
            else:
              """tbody가 없으면 바로 뽑아냄"""
              tds = tr.find_all('td')
              # print('---한줄을 출력합니다.---')
              single_row = [td.text for td in tds]
              # print(single_row)
              l.append(single_row)

      # 파일 떨구기
      filename = os.path.join(self.BASE_DIR, 'sample.csv')
      df = pd.DataFrame(l)
      # 헤더지정
      df.columns = df.iloc[0]
      df = df.iloc[1:]
      df.to_csv(filename)

      driver = self.driver

      return df, driver

class GetFinanceInfo_BS:
  def __init__(self, driver, BASE_DIR):
    self.driver = driver
    self.BASE_DIR = BASE_DIR

  def getBS(self):  
    """재무제표 스크래핑 총괄"""
    df, driver = self.get_BSInfo_start('df_BS.csv')
    df2, driver2 =  self.make_recent_BS(df, driver)
    
    return df2, driver2

  def make_recent_BS(self, df, driver):
    # 최근 분기 재무상태표만 남기고 그것을 쌓아서 트래킹 예정
    # 세로 합 구하기
    df2 = df.copy()
      
    # 데이터 유형 변경 (행 합 산출)
    for idx, col in enumerate(df2.columns):
      if idx >= 1:
        df2[col] = df2[col].str.replace('-','0')
        df2[col] = df2[col].astype(float)

    # 컬럼이름 추가
    df2 = df2.add_suffix('_TTM')

    # tmp = df2.copy()
    # filename = os.path.join(self.BASE_DIR, 'tmp.csv')
    # tmp.to_csv(filename)

    # 행/열변환해서 저장
    df2_T = df2.T

    # 첫행을 컬럼으로 지정
    df2_T.columns = df2_T.iloc[0]
    
    # 제목으로 사용된 행 삭제
    df2_T = df2_T.iloc[1:]

    # 가장 최근분기 재무상태표를 별도 데이터프레임으로 반환
    df_is_recent_1yr_ttm = df2_T.iloc[[0]]
 
    # csv로 내보내기
    filename1 = os.path.join(self.BASE_DIR, 'df_is_recent_1year_ttm_BS.csv')
    filename2 = os.path.join(self.BASE_DIR, 'df2_T_BS.csv')
    df_is_recent_1yr_ttm.to_csv(filename1)
    df2_T.to_csv(filename2)

    return df_is_recent_1yr_ttm, driver


  def get_BSInfo_start(self, filename):
    # 대차대조표 계정으로 이동
    bs_button = '/html/body/div[5]/section/ul[2]/li[3]/a'
    elem_bs = self.driver.find_element_by_xpath(bs_button)
    elem_bs.click()
    self.driver.implicitly_wait(3)

    """분기버튼 클릭"""
    bs_quarter_button = '/html/body/div[5]/section/div[8]/div[1]/a[2]'
    elem_bs_quarter = self.driver.find_element_by_xpath(bs_quarter_button)
    elem_bs_quarter.click()

    """분기 재무상태표 파싱"""
    테이블주소 = '/html/body/div[5]/section/div[9]/table'
    tbl = self.driver.find_element_by_xpath(테이블주소).get_attribute('outerHTML')

    # 테이블 긁어오기 
    soup = BeautifulSoup(tbl, 'html.parser')
    # print(soup)
    # print('---soup출력을 완료했습니다.---')

    l = []
    table_all = soup.find('table',{'class':'genTbl reportTbl'})
    table_contents = table_all.find_all('tbody')
    # print('---제목 및 내용을 출력합니다.---')
    # print(len(table_contents))
    
    # 행 출력
    for idx, trs in enumerate(table_contents):
      if idx == 0:
        """제목행(연월일)을 리스트로 저장"""
        single_year = [span.text for span in trs.find_all('span')]
        single_year = single_year[1:] # period_year 제외
        single_month_day = [div.text for div in trs.find_all('div')]
        # print('---single_row---')
        # 연월일 돌리면서 계정명 추가
        single_date_all = [y + m_d for y, m_d in zip(single_year, single_month_day)] 
        # 영문삭제
        single_date_all = [re.sub('[^0-9/]','',one) for one in single_date_all]
        # 올해연도 추가
        # single_date_all[0] = str(datetime.today().year) + single_date_all[0]
        # 컬럼정리를 위해 1개 컬럼 추가
        single_date_all = ['finance_account'] + single_date_all
        # single_date_all = 'finance_account' + single_date_all[0] [ymd[0] for ymd in single_date_all]
        # print(single_date_all)
        # single_row = [tr.text for tr in trs]
        l.append(single_date_all)
        
      else:
        """본문행일 경우, for loop 돌린후 리스트로 저장"""
        # print('%d 번째 행입니다.' % idx)
        # 여러 tr 들이 섞여 있음
        # tbody가 있을 경우, for loop 한번 더 돌려서 데이터 저장
        for tr in trs.find_all('tr'):
          """tbody가 있으면 한번 더 돌려서 뽑아냄"""
          if tr.find('tbody'):
            continue
            # for tds in tr.find('tbody'):
            #   single_row = [td for td in tds]
            #   """# 여기가 문제였음!!"""
            #   print('---single_row출력합니다.---')
            #   print(single_row)
            #   l.append(single_row)
          else:
            """tbody가 없으면 바로 뽑아냄"""
            tds = tr.find_all('td')
            # print('---한줄을 출력합니다.---')
            single_row = [td.text for td in tds]
            # print(single_row)
            l.append(single_row)

    # 파일 떨구기
    filename_f = os.path.join(self.BASE_DIR, filename)
    df = pd.DataFrame(l)
    # 헤더지정
    df.columns = df.iloc[0]
    df = df.iloc[1:]
    df.to_csv(filename_f)

    driver = self.driver

    return df, driver


class GetFinanceInfo_CF:
  def __init__(self, driver, BASE_DIR):
    self.driver = driver
    self.BASE_DIR = BASE_DIR

  def getCF(self):
    """재무제표 스크래핑 총괄"""
    df, driver = self.get_CSInfo_start('df_cf_raw.csv')
    df2 = self.make_recent_CF(df, driver)
    # print('df2:',type(df2)) # tuple

    # 현금흐름표 최근 4분기 산출
    # IS = GetFinanceInfo_IS()
    # df_cf_recent_1yr_ttm, df2_T = IS.make_recent_1year(df_CF, 'df_cf1.csv', 'df_cf2.csv')
    # df_cf_recent_1yr_ttm, driver
    return df2, driver
    

  def make_recent_CF(self, df, driver):
    # 최근 분기 재무상태표만 남기고 그것을 쌓아서 트래킹 예정
    # 세로 합 구하기
    df2 = df.copy()
    # print('df2: ', type(df2))
      
    # 데이터 유형 변경 (행 합 산출)
    for idx, col in enumerate(df2.columns):
      if idx >= 1:
        df2[col] = df2[col].str.replace('-','0')
        df2[col] = df2[col].astype(float)

    # 최근4분기 현금흐름표 합 컬럼명 지정
    # 컬럼이름 추가
    col = df2.columns.tolist()[1] + '_TTM'

    # 최근4분기 현금흐름표 합 산출
    df2[col] = df2.iloc[:,1:].sum(axis=1)

    # 행/열변환해서 저장
    df2_T = df2.T

    # 첫행을 컬럼으로 지정
    df2_T.columns = df2_T.iloc[0]
    
    # 제목으로 사용된 행 삭제
    df2_T = df2_T.iloc[1:]

    # 최근 4분기 현금흐름표의 합을 별도 데이터프레임으로 반환
    df_is_recent_1yr_ttm = df2_T.iloc[[-1]]

    df_is_recent_1yr_ttm = pd.DataFrame(df_is_recent_1yr_ttm)
    # print(type(df_is_recent_1yr_ttm))

    # csv로 내보내기
    filename1 = os.path.join(self.BASE_DIR, 'df_is_recent_1year_ttm_CF.csv')
    filename2 = os.path.join(self.BASE_DIR, 'df2_T_CF.csv')
    df_is_recent_1yr_ttm.to_csv(filename1)
    # print('df_is_recent_1yr_ttm:',type(df_is_recent_1yr_ttm)) # datafrmae
    df2_T.to_csv(filename2)

    return df_is_recent_1yr_ttm

  
  def get_CSInfo_start(self, filename):
    # 현금흐름표 계정으로 이동
    cf_button = '/html/body/div[5]/section/ul[2]/li[4]/a'
    elem_cf = self.driver.find_element_by_xpath(cf_button)
    elem_cf.click()
    self.driver.implicitly_wait(3)

    테이블주소 = '/html/body/div[5]/section/div[9]/table'
    tbl = self.driver.find_element_by_xpath(테이블주소).get_attribute('outerHTML')

    # 테이블 긁어오기 
    soup = BeautifulSoup(tbl, 'html.parser')
    # print(soup)
    # print('---soup출력을 완료했습니다.---')

    l = []
    table_all = soup.find('table',{'class':'genTbl reportTbl'})
    table_contents = table_all.find_all('tbody')
    # print('---제목 및 내용을 출력합니다.---')
    # print(len(table_contents))
    
    # 행 출력
    for idx, trs in enumerate(table_contents):
      if idx == 0:
        """제목행(연월일)을 리스트로 저장"""
        single_year = [span.text for span in trs.find_all('span')]
        single_year = single_year[1:] # period_year 제외
        single_month_day = [div.text for div in trs.find_all('div')]
        # print('---single_row---')
        # 연월일 돌리면서 계정명 추가
        single_date_all = [y + m_d for y, m_d in zip(single_year, single_month_day)] 
        # 영문삭제
        single_date_all = [re.sub('[^0-9/]','',one) for one in single_date_all]
        # 올해연도 추가
        # single_date_all[0] = str(datetime.today().year) + single_date_all[0]
        # 컬럼정리를 위해 1개 컬럼 추가
        single_date_all = ['finance_account'] + single_date_all
        # single_date_all = 'finance_account' + single_date_all[0] [ymd[0] for ymd in single_date_all]
        # print(single_date_all)
        # single_row = [tr.text for tr in trs]
        l.append(single_date_all)
        
      else:
        """본문행일 경우, for loop 돌린후 리스트로 저장"""
        # print('%d 번째 행입니다.' % idx)
        # 여러 tr 들이 섞여 있음
        # tbody가 있을 경우, for loop 한번 더 돌려서 데이터 저장
        for tr in trs.find_all('tr'):
          """tbody가 있으면 한번 더 돌려서 뽑아냄"""
          if tr.find('tbody'):
            continue
            # for tds in tr.find('tbody'):
            #   single_row = [td for td in tds]
            #   """# 여기가 문제였음!!"""
            #   print('---single_row출력합니다.---')
            #   print(single_row)
            #   l.append(single_row)
          else:
            """tbody가 없으면 바로 뽑아냄"""
            tds = tr.find_all('td')
            # print('---한줄을 출력합니다.---')
            single_row = [td.text for td in tds]
            # print(single_row)
            l.append(single_row)

    # 파일 떨구기
    filename_f = os.path.join(self.BASE_DIR, filename)
    df = pd.DataFrame(l)
    # 헤더지정
    df.columns = df.iloc[0]
    df = df.iloc[1:]
    df.to_csv(filename_f)

    driver = self.driver

    return df, driver



  def modify_column_name(self, df):
    df2 = df.copy()
    df2 = df2.loc[:, ~df2.columns.duplicated()]

    return df2

  def sqlite_append(self, df):
    # /content/drive/"My Drive"/"Colab Notebooks"
    con = sqlite3.connect("/content/drive/My Drive/Colab Notebooks/neres_stock.db")
    filename = os.path.join(self.BASE_DIR, 'tmp.csv')
    df.to_csv(filename)
    df.to_sql('indonesia', con, if_exists='append', index=True)
    con.close()

  # 종목코드 읽기
  def GetStockCode(self):
    con = sqlite3.connect('/content/drive/My Drive/Colab Notebooks/neres_stock_code_indonesia.db')
    df = pd.read_sql_query("SELECT * FROM indonesia_stock_code", con, index_col=None)
    # 
    filename = os.path.join(self.BASE_DIR,'code.csv')
    df.to_csv(filename)

    return df


if __name__ == "__main__" :
  get = GetItemScoutWebpage()
  get.run()
  