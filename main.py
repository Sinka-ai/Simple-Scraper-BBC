import time
import logging
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager

# Настройка логирования
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger()

def setup_driver():
    """Настройка веб-драйвера."""
    options = webdriver.ChromeOptions()
    options.add_argument('--headless')  # Работает в фоновом режиме
    options.add_argument('--disable-gpu')
    driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()), options=options)
    return driver

def fetch_news(driver):
    """Функция для извлечения новостей с сайта BBC."""
    news_data = []
    try:
        logger.info("Ожидание появления заголовков новостей...")
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "h2[data-testid='card-headline']"))
        )

        logger.info("Заголовки найдены. Извлечение заголовков новостей...")
        news_cards = driver.find_elements(By.CSS_SELECTOR, "div[data-testid$='-card']")

        for idx, card in enumerate(news_cards):
            try:
                headline_element = card.find_element(By.CSS_SELECTOR, "h2[data-testid='card-headline']")
                headline = headline_element.text
                link_element = card.find_element(By.CSS_SELECTOR, "a[data-testid='internal-link']")
                link = link_element.get_attribute('href')
                if headline and link:
                    news_data.append((headline, link))
                    logger.info(f"Извлечено: {headline} - {link}")
            except Exception as e:
                logger.error(f"Ошибка при обработке карточки {idx + 1}: {e}")

    except Exception as e:
        logger.error(f"Произошла ошибка: {e}")

    return news_data

def save_news(news_data, file_path="news.txt"):
    """Сохранение новостей в файл."""
    with open(file_path, "w", encoding="utf-8") as file:
        for idx, (headline, link) in enumerate(news_data):
            file.write(f"{idx + 1}. {headline}\n{link}\n\n")
    logger.info(f"Данные сохранены в {file_path}")

def main():
    """Основная функция для выполнения скрипта."""
    driver = setup_driver()
    driver.get("https://www.bbc.com/news")
    news_data = fetch_news(driver)
    driver.quit()
    save_news(news_data)

if __name__ == "__main__":
    main()
