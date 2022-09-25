from appium import webdriver
from appium.webdriver.common.appiumby import AppiumBy
from appium.webdriver.common.mobileby import MobileBy
import time
import pytest

caps = {}
caps["appium:appPackage"] = "com.lbrc.PeriodCalendar"
caps["platformName"] = "Android"
caps["appium:platformVersion"] = "9"
caps["appium:deviceName"] = "Huawei P10"
caps["appium:automationName"] = "UiAutomator2"
caps["appium:udid"] = "YLM0217811000139"
caps["appium:appActivity"] = "com.digitalchemy.period.activity.MainActivity"
caps["appium:ensureWebviewsHavePages"] = True
caps["appium:nativeWebScreenshot"] = True
caps["appium:newCommandTimeout"] = 3600
caps["appium:connectHardwareKeyboard"] = True

# Commons
back_btn = "/hierarchy/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.FrameLayout/android.widget.FrameLayout[1]/android.widget.FrameLayout/android.view.View/android.view.View/android.view.View/android.view.View/android.widget.ImageView[1]"

driver = webdriver.Remote("http://0.0.0.0:4723/wd/hub", caps)


@pytest.fixture(scope="module", autouse=True)
def test_skip_setup():
    driver.implicitly_wait(5)
    driver.find_element(by=AppiumBy.ACCESSIBILITY_ID, value="Продолжить").click()

    driver.implicitly_wait(5)
    driver.find_element(by=AppiumBy.ACCESSIBILITY_ID, value="Пропустить").click()

    driver.implicitly_wait(5)
    driver.find_element(by=AppiumBy.ACCESSIBILITY_ID, value="Отслеживать цикл\nБудьте готовы к следующим месячным и "
                                                            "узнайте больше о своем организме благодаря статистике "
                                                            "предыдущих циклов").click()

    driver.implicitly_wait(5)
    # Dirty hack because ACCESSIBILITY_ID doesn't work
    driver.find_element(by=AppiumBy.XPATH, value="/hierarchy/android.widget.FrameLayout/android.widget.LinearLayout"
                                                 "/android.widget.FrameLayout/android.widget.FrameLayout/android"
                                                 ".widget.FrameLayout["
                                                 "3]/android.widget.RelativeLayout/android.widget.ImageView[1]").click()

    # Skip screens
    elems = ["Не уверена", "Не уверена", "Не уверена", "Пропустить"]
    for el in elems:
        time.sleep(0.2)
        driver.implicitly_wait(5)
        driver.find_element(by=AppiumBy.ACCESSIBILITY_ID, value=el).click()

    driver.implicitly_wait(5)
    driver.find_element(by=AppiumBy.ID, value="com.lbrc.PeriodCalendar:id/skip_button").click()

    driver.implicitly_wait(5)
    driver.find_element(by=AppiumBy.ACCESSIBILITY_ID, value="Настройки").click()


def test_backup_location():
    driver.implicitly_wait(5)
    driver.find_element(MobileBy.ANDROID_UIAUTOMATOR, value="new UiScrollable(new UiSelector().scrollable(true)).setMaxSearchSwipes(2).scrollIntoView(new UiSelector().text(\"Язык\"))")
    driver.find_element(by=AppiumBy.ACCESSIBILITY_ID, value="Язык").click()

    localizations = {
        'en': ["English", "Back up data", "Auto backup\nAutomatic data backup is performed every 5 days", "CANCEL", "Language"],
        'ind': ["Bahasa Indonesia", "Cadangkan data", "Cadangkan data secara otomatis\nPencadangan data otomatis dilakukan setiap 5 hari", "BATAL", "Bahasa"],
        'ces': ["Čeština", "Zálohovat", "Automatické zálohování dat\nAutomatické zálohování dat se provádí každých 5 dní", "ZRUŠIT", "Jazyk"]
    }

    for lang, values in localizations.items():
        driver.implicitly_wait(5)
        print(f"Checking localization: {lang}")
        driver.find_element(by=AppiumBy.ACCESSIBILITY_ID, value=localizations[lang][0]).click()
        driver.find_element(by=AppiumBy.XPATH, value=back_btn).click()

        driver.implicitly_wait(5)
        driver.find_element(by=AppiumBy.ACCESSIBILITY_ID, value=localizations[lang][1]).click()
        driver.find_element(by=AppiumBy.ACCESSIBILITY_ID, value=localizations[lang][2]).click()

        driver.implicitly_wait(5)
        driver.find_element(by=AppiumBy.ACCESSIBILITY_ID, value=localizations[lang][3]).click()
        driver.find_element(by=AppiumBy.XPATH, value=back_btn).click()

        driver.implicitly_wait(5)
        driver.find_element(by=AppiumBy.ACCESSIBILITY_ID, value=localizations[lang][4]).click()

    driver.quit()
