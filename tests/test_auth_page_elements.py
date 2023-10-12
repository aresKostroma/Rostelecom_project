import time

import pytest
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from pages.auth_page import AuthPage
from pages.setting import *


def test_tab_phone(web_browser):
    """ Тест-кейс 1: проверка наличия таба Телефон на странице авторизации """

    page = AuthPage(web_browser)

    # Переходим на таб Телефон
    page.swich_tab(page.tab_phone)
    print(page.title_username.text)
    assert page.title_username.text == u"Мобильный телефон", "1 failed: Таб Телефон не найден"


def test_tab_email(web_browser):
    """ Тест-кейс 2: проверка наличия таба Почта на странице авторизации """

    page = AuthPage(web_browser)

    # Переходим на таб Почта
    page.swich_tab(page.tab_email)
    print(page.title_username.text)
    assert page.title_username.text == u"Электронная почта", "2 failed: Таб Почта не найден"


def test_tab_login(web_browser):
    """ Тест-кейс 3: проверка наличия таба Логин на странице авторизации """

    page = AuthPage(web_browser)

    # Переходим на таб Логин
    page.swich_tab(page.tab_login)
    print(page.title_username.text)
    assert page.title_username.text == u"Логин", "3 failed: Таб Логин не найден"


def test_tab_ls(web_browser):
    """ Тест-кейс 4: проверка наличия таба Лицевой счет на странице авторизации """

    page = AuthPage(web_browser)

    # Переходим на таб Лицевой счет
    page.swich_tab(page.tab_ls)
    print(page.title_username.text)
    assert page.title_username.text == u"Лицевой счёт", "4 failed: Таб Лицевой счет не найден"


def test_input_field(web_browser):
    """ Тест-кейс 5: проверка наличия полей ввода username и пароля на странице авторизации """

    page = AuthPage(web_browser)

    # Есть поле ввода логина
    assert page.username, "5 failed: Нет поля ввода username"
    # Есть поле ввода пароля
    assert page.password, "5 failed: Нет поля ввода пароля"
    # Есть кнопка "Войти"
    assert page.btn, "5 failed: Нет кнопки 'Войти'"


def test_ad_slogan(web_browser):
    """ Тест-кейс 6: проверка наличия слогана на странице авторизации """

    page = AuthPage(web_browser)

    assert ad_slogan in page.ad_slogan.text, f"6 failed: Нет слогана {ad_slogan}"


@pytest.mark.parametrize(("username, tab_title"),
                            [
                                (valid_email, u"Почта"),
                                (valid_login, u"Логин"),
                                (valid_ls, u"Лицевой счёт"),
                                (valid_phone, u"Телефон")
                            ],
                            ids= [
                                'By email',
                                'By login',
                                "By LS",
                                "By phone"]
                         )
def test_auto_switch_tab(username, tab_title, web_browser):
    """ Тест-кейс 7: автоматическая смена таба при вводе соотвествующего способа авторизации """

    page = AuthPage(web_browser)

    # Если проверяем ввод телефона, переходим предварительно на таб Почта, т.к. таб Телефон открыт по умолчанию
    if tab_title == "Телефон":
        page.swich_tab(page.tab_email)

    # Вводим логин
    page.enter_username(username)
    # Кликаем на пароль
    page.password.click()

    time.sleep(3)

    # Смотрим активный таб
    active_tab = web_browser.find_element(By.CSS_SELECTOR, "div.rt-tab--active").text
    # print(f"\n{active_tab} == {tab_title}")

    assert active_tab == tab_title, "7 failed: Таб автоматически не изменился"


def test_forgot_password(web_browser):
    """ Тест-кейс 8: проверка наличия ссылки "Забыл пароль" на странице авторизации """

    page = AuthPage(web_browser)

    # Кликаем по ссылке "Забыл пароль"
    page.forgot_pass.click()

    # Явное ожидание загрузки элемента div.reset-form-container - внешний контейнер формы восстановления пароля
    WebDriverWait(web_browser, 10).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, 'div.reset-form-container'))
    )

    assert "Восстановление пароля" in web_browser.find_element(By.CSS_SELECTOR, 'div.reset-form-container').text, "8 failed: На странице нет элемента 'Восстановление пароля'"


def test_new_reg(web_browser):
    """ Тест-кейс 9: проверка наличия ссылки "Зарегистрироваться" на странице авторизации """

    page = AuthPage(web_browser)

    # Кликаем по ссылке "Зарегистрироваться"
    page.new_reg.click()

    # Явное ожидание загрузки элемента div.register-form-container - внешний контейнер формы регистрации
    WebDriverWait(web_browser, 10).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, 'div.register-form-container'))
    )

    assert "Регистрация" in web_browser.find_element(By.CSS_SELECTOR, 'div.register-form-container').text, "9 failed: На странице нет элемента 'Регистрация'"


def test_user_agree(web_browser):
    """ Тест-кейс 10: проверка наличия ссылки "пользовательское соглашение" на странице авторизации """

    page = AuthPage(web_browser)

    # Кликаем по ссылке "пользовательское соглашение"
    page.user_agree.click()

    # Ссылка открывается в новой вкладке
    new_window = web_browser.window_handles[1]
    web_browser.switch_to.window(new_window)

    assert web_browser.current_url == 'https://b2c.passport.rt.ru/sso-static/agreement/agreement.html', "10 failed: Пользовательское соглашение не загружено"