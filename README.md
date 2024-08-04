# Home Assistant LiteDB

Home Assistant LiteDB is a Python script designed to interact with Home Assistant, fetch entities, save them to a local SQLite database, and provide various command-line functionalities.

## Features

- Fetch entities from Home Assistant and save them to a SQLite database.
- Purge the database and recreate it.
- Display the last 50 rows of logs.
- Configurable polling interval.
- Logging to file and/or console.

## Installation

1. Clone the repository:

    ```sh
    git clone https://github.com/willmo103/home_assistant_litedb.git
    cd home_assistant_litedb
    ```

2. Create a virtual environment and install dependencies:

    ```sh
    python -m venv venv
    source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
    pip install -r requirements.txt
    ```

3. Run the setup script to create the configuration file:

    ```sh
    python setup.py
    ```

4. Edit `conf.yml` to add your Home Assistant URL and long-lived access token.

## Usage

### Command Line Arguments

- `-d`, `--debug`: Run once and output logging to terminal.
- `-p`, `--purge`: Purge entire database and recreate, do not poll after creation, exit and inform.
- `-l`, `--logs`: Display the last 50 rows of the logs.
- `--run-detached`: Run this script headless.
- `--run-no-logging`: Run this script without logging (can only be used with `-d` or `--debug`).

### Examples

1. Fetch entities and save to database:

    ```sh
    python home_assistant_litedb/main.py
    ```

2. Run in debug mode:

    ```sh
    python home_assistant_litedb/main.py --debug
    ```

3. Purge the database:

    ```sh
    python home_assistant_litedb/main.py --purge
    ```

4. Display the last 50 rows of logs:

    ```sh
    python home_assistant_litedb/main.py --logs
    ```

## Configuration

The configuration is stored in `conf.yml`. Edit this file to set your Home Assistant URL, token, database path, and polling interval.

Example `conf.yml`:

```yaml
HA_URL: 'http://192.168.xxx.xxx:8123'
HA_TOKEN: '<your_long_lived_access_token>'
DB_PATH: 'C:\\Users\\YourUsername\\HomeAssistantLiteDB.db'
POLL_INTERVAL: 120
```

## License

This project is licensed under the MIT [License](LICENSE).

## Roadmap

- **Integration with Other Home Automation Platforms**
  - Extend the functionality of Home-Assistant LiteDB to support data collection and management from other popular home automation platforms.
  - Implement a unified interface to manage data from multiple platforms.

Read the full [Roadmap](ROADMAP.md).

## Contributing

Contributions are welcome! Please fork the repository and submit a pull request.

## Contact

For any issues or questions, please open an issue on GitHub or contact me at <willmorris103@gmail.com>.
