import sqlite3
import csv
import logging
from pathlib import Path

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

def create_url_csv(output_path: str = "./data/linkedin_urls.csv", db_path: str = "./data/linkedin_connections.db") -> None:
    """Create a CSV file with LinkedIn profile URLs"""
    BASE_URL = "https://www.linkedin.com"
    
    # Ensure output directory exists
    Path(output_path).parent.mkdir(parents=True, exist_ok=True)
    
    # Get connections from database
    connections = get_connection_from_db(db_path)
    
    # Write to CSV
    with open(output_path, 'w', newline='', encoding='utf-8') as csvfile:
        writer = csv.writer(csvfile)
        
        for profile_url, name in connections:
            full_url = BASE_URL + profile_url
            writer.writerow([full_url])
    
    logger.info(f"Successfully created CSV file with {len(connections)} URLs at {output_path}")

if __name__ == "__main__":
    create_url_csv()