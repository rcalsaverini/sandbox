from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
import time
import random
from pathlib import Path
from datetime import datetime
import logging

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)
logger = logging.getLogger(__name__)


def crawl_and_save_html(output_path: Path):
    """
    Crawl LinkedIn connections page and save the full HTML to a file.
    Returns the path to the saved HTML file.
    """
    logger.info("Starting LinkedIn connections scraping process")
    driver = webdriver.Chrome()

    try:
        logger.info("Attempting to log in to LinkedIn")
        login(driver)
        logger.info("Successfully logged in to LinkedIn")

        logger.info("Navigating to connections page")
        navigate_to_connections(driver)
        logger.info("Successfully reached connections page")

        output_file = get_output_file(output_path)
        logger.info(f"Will save connections to: {output_file}")

        last_height = driver.execute_script("return document.body.scrollHeight")
        scroll_count = 0
        same_height_count = 0
                
        while True:
            scroll_count += 1
            logger.info(f"Scrolling page (attempt {scroll_count})")
            scroll_to_bottom(driver)
            new_height = driver.execute_script("return document.body.scrollHeight")
            
            if new_height == last_height:
                same_height_count += 1
                logger.info(f"Page height unchanged (attempt {same_height_count}/3)")
                
                if same_height_count >= 3:
                    logger.info("Page height unchanged for 3 consecutive attempts")
                    # Count visible connection cards
                    connection_cards = driver.find_elements(By.CLASS_NAME, "mn-connection-card")
                    logger.info(f"Found {len(connection_cards)} connection cards")
                    
                    # Ask user for confirmation
                    user_input = input("\nThe page seems to have stopped loading. "
                                     f"Found {len(connection_cards)} connections. "
                                     "Do you want to continue scrolling? (y/n): ").lower()
                    
                    if user_input != 'y':
                        logger.info("User confirmed end of page, saving HTML content")
                        output_file.write_text(driver.page_source, encoding="utf-8")
                        logger.info(f"Successfully saved {len(driver.page_source)} bytes to {output_file}")
                        break
                    else:
                        logger.info("User chose to continue scrolling")
                        same_height_count = 0
            else:
                same_height_count = 0
                
            last_height = new_height
            wait_time = random.uniform(2, 4)
            logger.info(f"Waiting {wait_time:.1f} seconds before next scroll")
            time.sleep(wait_time)
            
    except TimeoutException:
        logger.error("Timeout waiting for page to load")
        return None
    except IOError as e:
        logger.error(f"Failed to save HTML file: {e}")
        return None
    finally:
        logger.info("Closing browser")
        driver.quit()


def login(driver):
    logger.info("Navigating to LinkedIn login page")
    driver.get("https://www.linkedin.com/login")
    
    # Wait for and fill in login form
    logger.info("Waiting for login form to load")
    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.ID, "username"))
    )
    logger.info("Filling in login credentials")
    driver.find_element(By.ID, "username").send_keys("rafael.calsaverini@gmail.com")
    driver.find_element(By.ID, "password").send_keys("r!BBVkDnOTqz*74")
    logger.info("Submitting login form")
    driver.find_element(By.CSS_SELECTOR, "button[type='submit']").click()


def navigate_to_connections(driver):
    logger.info("Navigating to connections page")
    driver.get("https://www.linkedin.com/mynetwork/invite-connect/connections/")
    logger.info("Waiting for connection cards to load")
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, "mn-connection-card")))
    logger.info("Connection cards loaded successfully")
    return driver


def get_output_file(output_path: Path) -> Path:
    logger.info(f"Creating output directory: {output_path}")
    output_path.mkdir(parents=True, exist_ok=True)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    output_file = output_path / f"linkedin_connections_{timestamp}.html"
    logger.info(f"Generated output file path: {output_file}")
    return output_file


def scroll_to_bottom(driver: webdriver.Chrome) -> None:
    """Scroll to bottom of page to load more connections"""
    logger.debug("Scrolling to bottom of page")
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    time.sleep(2)  # Wait for content to load


def main():
    """Main entry point for the LinkedIn connections scraper"""
    try:
        logger.info("Starting LinkedIn connections scraper")
        
        # Setup output path
        output_path = Path("./data/connections.html").resolve()
        logger.info(f"Using output path: {output_path}")
        logger.info(f"Output directory exists: {output_path.parent.exists()}")
        
        # Create parent directory if it doesn't exist
        if not output_path.parent.exists():
            logger.info(f"Creating output directory: {output_path.parent}")
            output_path.parent.mkdir(parents=True, exist_ok=True)
        
        # Run the scraper
        result = crawl_and_save_html(output_path)
        
        if result:
            logger.info(f"Successfully saved connections to: {result}")
            logger.info(f"File size: {Path(result).stat().st_size / 1024:.1f} KB")
        else:
            logger.error("Failed to save connections")
            
    except Exception as e:
        logger.error(f"Unexpected error in main: {str(e)}", exc_info=True)
        raise
    finally:
        logger.info("LinkedIn connections scraping process completed")


if __name__ == "__main__":
    main()
