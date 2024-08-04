# home_assistant_litedb/main.py

import argparse
import logging
import os
import sqlite3
from datetime import datetime, time

import requests
import yaml

# Load configuration from conf.yml
with open("conf.yml", "r") as file:
    config = yaml.safe_load(file)

HA_URL = config["HA_URL"]
HA_TOKEN = config["HA_TOKEN"]
DB_PATH = config["DB_PATH"]
POLL_INTERVAL = config.get("POLL_INTERVAL", 120)

headers = {
    "Authorization": f"Bearer {HA_TOKEN}",
    "content-type": "application/json",
}


def setup_logging(debug, run_no_logging):
    """
    Setup logging configuration.
    """
    if not run_no_logging:
        log_file = os.path.expanduser("~") + "\\home_assistant_litedb.log"
        logging.basicConfig(
            filename=log_file, level=logging.DEBUG if debug else logging.INFO
        )
    else:
        logging.basicConfig(level=logging.DEBUG if debug else logging.INFO)


def log_method_call(method_name, details=None):
    """
    Log method call details.
    """
    log_message = f"{datetime.now()}: Called {method_name}"
    if details:
        log_message += f" with details: {details}"
    logging.info(log_message)
    save_log_to_db(log_message)


def save_log_to_db(log_message):
    """
    Save log message to the database.
    """
    try:
        conn = sqlite3.connect(DB_PATH)
        c = conn.cursor()
        c.execute(
            """
            CREATE TABLE IF NOT EXISTS logs (
                id INTEGER PRIMARY KEY,
                timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
                message TEXT
            )
        """
        )
        c.execute("INSERT INTO logs (message) VALUES (?)", (log_message,))
        conn.commit()
        conn.close()
    except Exception as e:
        logging.error(f"Failed to save log to database: {e}")


def get_entities():
    """
    Get entities from Home Assistant.
    """
    log_method_call("get_entities")
    try:
        response = requests.get(f"{HA_URL}/api/states", headers=headers)
        response.raise_for_status()
        return response.json()
    except Exception as e:
        logging.error(f"Error in get_entities: {e}")
        return None


def save_entities_to_db(entities):
    """
    Save entities to the database.
    """
    log_method_call("save_entities_to_db", f"entities count: {len(entities)}")
    try:
        conn = sqlite3.connect(DB_PATH)
        c = conn.cursor()

        c.execute(
            """
            CREATE TABLE IF NOT EXISTS entities (
                id INTEGER PRIMARY KEY,
                entity_id TEXT,
                friendly_name TEXT,
                state TEXT,
                entity_type TEXT,
                timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
            )
        """
        )

        for entity in entities:
            entity_id = entity["entity_id"]
            state = entity["state"]
            friendly_name = entity["attributes"].get(
                "friendly_name", "No friendly name"
            )
            entity_type = entity_id.split(".")[0]

            c.execute(
                """
                INSERT INTO entities (
                    entity_id,
                    friendly_name,
                    state,
                    entity_type
                    )
                VALUES (?, ?, ?, ?)
            """,
                (entity_id, friendly_name, state, entity_type),
            )

        conn.commit()
        conn.close()
    except Exception as e:
        logging.error(f"Error in save_entities_to_db: {e}")


def print_entities(entities):
    """
    Print entities to the console.
    """
    log_method_call("print_entities", f"entities count: {len(entities)}")
    try:
        entity_types = {}
        for entity in entities:
            entity_id = entity["entity_id"]
            state = entity["state"]
            friendly_name = entity["attributes"].get(
                "friendly_name", "No friendly name"
            )

            entity_type = entity_id.split(".")[0]
            if entity_type not in entity_types:
                entity_types[entity_type] = []

            entity_types[entity_type].append(
                {"entity_id": entity_id,
                 "friendly_name": friendly_name,
                 "state": state}
            )

        for entity_type, entities in entity_types.items():
            print(f"\n--- {entity_type.upper()} ---")
            for entity in entities:
                print(f"ID: {entity['entity_id']}")
                print(f"Name: {entity['friendly_name']}")
                print(f"State: {entity['state']}")
                print("---")
    except Exception as e:
        logging.error(f"Error in print_entities: {e}")


def purge_database():
    """
    Purge the database.
    """
    log_method_call("purge_database")
    try:
        conn = sqlite3.connect(DB_PATH)
        c = conn.cursor()
        c.execute("DROP TABLE IF EXISTS entities")
        c.execute("DROP TABLE IF EXISTS logs")
        conn.commit()
        conn.close()
        logging.info("Database purged and recreated.")
    except Exception as e:
        logging.error(f"Error in purge_database: {e}")


def display_logs():
    """
    Display the last 50 rows of the logs.
    """
    log_method_call("display_logs")
    try:
        log_file = os.path.expanduser("~") + "\\home_assistant_litedb.log"
        if os.path.exists(log_file):
            with open(log_file, "r") as file:
                logs = file.readlines()
                for line in logs[-50:]:
                    print(line.strip())
        else:
            print("Log file does not exist.")
    except Exception as e:
        logging.error(f"Error in display_logs: {e}")


def main(args):
    """
    Main function to handle arguments and execute methods accordingly.
    """
    if args.purge:
        purge_database()
        print("Database purged.")
        return

    if args.logs:
        display_logs()
        return

    while True:
        entities = get_entities()
        if entities:
            if not args.run_no_logging:
                save_entities_to_db(entities)
            if args.debug:
                print_entities(entities)
        else:
            print("Failed to fetch entities")

        if args.debug:
            break
        else:
            time.sleep(POLL_INTERVAL)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Home Assistant LiteDB Script")
    parser.add_argument(
        "-d",
        "--debug",
        action="store_true",
        help="Run once and output logging to terminal",
    )
    parser.add_argument(
        "-p",
        "--purge",
        action="store_true",
        help="Purge entire database and recreate"
    )
    parser.add_argument(
        "-l",
        "--logs",
        action="store_true",
        help="Display the last 50 rows of the logs"
    )
    parser.add_argument(
        "rd",
        "--run-detached",
        action="store_true",
        help="Run this script headless"
    )
    parser.add_argument(
        "rnl",
        "--run-no-logging",
        action="store_true",
        help="Run this script without logging",
    )

    args = parser.parse_args()
    setup_logging(args.debug, args.run_no_logging)

    main(args)
