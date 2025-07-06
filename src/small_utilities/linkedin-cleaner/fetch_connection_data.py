import sqlite3
from pathlib import Path
import logging
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from unidecode import unidecode
import time
import random

BASE_URL = "https://www.linkedin.com"

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

def get_connection_from_db(db_path: str = "./data/linkedin_connections.db") -> list[tuple]:
    """Get all connections from the database"""
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        cursor.execute('SELECT profile_url, name FROM connections')
        connections = cursor.fetchall()
        logger.info(f"Retrieved {len(connections)} connections from database")
        return connections
    except sqlite3.Error as e:
        logger.error(f"Error reading from database: {str(e)}")
        raise
    finally:
        conn.close()

def login_to_linkedin(driver: webdriver.Chrome) -> None:
    """Login to LinkedIn"""
    logger.info("Navigating to LinkedIn login page")
    driver.get("https://www.linkedin.com/login")
    
    # Wait for and fill in login form
    logger.info("Waiting for login form to load")
    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.ID, "username"))
    )
    logger.info("Filling in login credentials")
    driver.find_element(By.ID, "username").send_keys("servo.patsy+clean@gmail.com")
    driver.find_element(By.ID, "password").send_keys("renbey@12")
    logger.info("Submitting login form")
    driver.find_element(By.CSS_SELECTOR, "button[type='submit']").click()
    
    # Wait for login to complete
    time.sleep(3)

def fetch_profile_page(driver: webdriver.Chrome, profile_url: str, profile_name: str, output_dir: Path) -> bool:
    """Fetch and save a single profile page"""
    try:
        logger.info(f"Fetching profile: {profile_url}")
        filename = profile_name.encode('ascii', 'ignore').decode('ascii').lower().replace(" ", "_")
        output_file = output_dir / f"{filename}.html"
        
        if output_file.exists():
            logger.info(f"Profile page already exists: {output_file}")
            return True
        else:
            sleep_time = random.uniform(20, 40)
            logger.info(f"Profile page not found. Will fetch after sleeping for {sleep_time} seconds.")
            time.sleep(sleep_time)

            driver.get(profile_url)
            WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.ID, "experience"))
            )
                    
            with open(output_file, "w", encoding="utf-8") as f:
                logger.info("Saving to file")
                f.write(driver.page_source)        
            logger.info(f"Successfully saved profile page to {output_file}.")
            
            return True
        
    except TimeoutException:
        logger.exception(f"Timeout while loading profile: {profile_url}")
        return False
    except Exception as e:
        logger.exception(f"Error fetching profile {profile_url}", e)
        return False

def main():
    # Setup paths
    db_path = "./data/linkedin_connections.db"
    output_dir = Path("./data/profile_pages/")
    output_dir.mkdir(parents=True, exist_ok=True)
    
    try:
        # Get connections from database
        connections = get_connection_from_db(db_path)
        
        # Initialize webdriver
        driver = webdriver.Chrome()
        
        try:
            # Login to LinkedIn
            login_to_linkedin(driver)
            
            # Fetch each profile
            for profile_url, name in connections:
                actual_url = BASE_URL + profile_url
                success = fetch_profile_page(driver, actual_url, name, output_dir)
                if success:
                    logger.info(f"Successfully fetched profile for {name}")
                else:
                    logger.error(f"Failed to fetch profile for {name}")
                
                # Add a random delay between requests
                
        finally:
            driver.quit()
            
    except Exception as e:
        logger.exception(f"Error in main execution: {str(e)}", e)
        raise

if __name__ == "__main__":
    main()
