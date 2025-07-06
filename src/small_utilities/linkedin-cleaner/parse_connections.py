from dataclasses import dataclass
from bs4 import BeautifulSoup
from pathlib import Path
import logging
import sqlite3
from datetime import datetime

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

@dataclass
class connection:
    name: str
    profile_url: str
    headline: str
    connected_date: str

def init_db(db_path: str = "linkedin_connections.db") -> None:
    """Initialize the SQLite database with the required table"""
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS connections (
                profile_url TEXT PRIMARY KEY,
                name TEXT NOT NULL,
                headline TEXT,
                connected_date TEXT,
                last_updated TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        conn.commit()
        logger.info(f"Database initialized at {db_path}")
    except sqlite3.Error as e:
        logger.error(f"Error initializing database: {str(e)}")
        raise
    finally:
        conn.close()

def save_connections_to_db(connections: dict[str, connection], db_path: str = "linkedin_connections.db") -> None:
    """Save connections to the SQLite database"""
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        for connection_data in connections.values():
            cursor.execute('''
                INSERT OR REPLACE INTO connections 
                (profile_url, name, headline, connected_date, last_updated)
                VALUES (?, ?, ?, ?, ?)
            ''', (
                connection_data.profile_url,
                connection_data.name,
                connection_data.headline,
                connection_data.connected_date,
                datetime.now().isoformat()
            ))
        
        conn.commit()
        logger.info(f"Successfully saved {len(connections)} connections to database")
    except sqlite3.Error as e:
        logger.error(f"Error saving to database: {str(e)}")
        raise
    finally:
        conn.close()

def parse_html_file(html_file: Path) -> dict[str, connection]:
    """Parse a saved HTML file to extract connection information"""

    connections = {}
    logger.info(f"Starting to parse HTML file: {html_file}")
    
    try:
        with open(html_file, "r", encoding="utf-8") as f:
            logger.debug("Reading HTML file content")
            soup = BeautifulSoup(f.read(), "html.parser")
            
        connection_cards = soup.find_all("li", class_="mn-connection-card")
        logger.info(f"Found {len(connection_cards)} connection cards")
        
        for card in connection_cards:
            try:
                name = card.find("span", class_="mn-connection-card__name").text.strip()
                profile_url = card.find("a", class_="mn-connection-card__link")["href"]
                headline = card.find("span", class_="mn-connection-card__occupation").text.strip()
                connected_date = card.find("time", class_="time-badge").text.replace("Connected", "").strip()
                
                conn = connection(name=name, profile_url=profile_url, headline=headline, connected_date=connected_date)
                connections[conn.profile_url] = conn
                logger.debug(f"Successfully parsed connection: {name}")
            except Exception as e:
                logger.error(f"Error parsing connection card: {str(e)}")
                continue
        
        logger.info(f"Successfully parsed {len(connections)} connections")
        return connections
        
    except Exception as e:
        logger.error(f"Error processing HTML file: {str(e)}")
        raise

def main():
    path = "./data/linkedin_connections_20250518_200645.html"
    db_path = "./data/linkedin_connections.db"
    
    logger.info("Starting LinkedIn connections parser")
    try:
        # Initialize database
        init_db(db_path)
        
        # Parse connections
        output = parse_html_file(path)
        
        # Save to database
        save_connections_to_db(output, db_path)
        
        # Log summary
        for (key, data) in output.items():
            logger.debug(f"Connection data for {data.name}: {data}")
            
    except Exception as e:
        logger.error(f"Error in main execution: {str(e)}")
        raise

if __name__ == "__main__":
    main()
    