import unittest
from unittest.mock import patch, MagicMock, mock_open
import home_assistant_helper as hah
import re


class TestHomeAssistantHelper(unittest.TestCase):

    @patch('home_assistant_helper.requests.get')
    def test_get_entities(self, mock_get):
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = [
            {
                "entity_id": "sensor.test",
                "state": "on",
                "attributes": {
                    "friendly_name": "Test Sensor"
                }
            }
        ]
        mock_get.return_value = mock_response

        entities = hah.get_entities()
        self.assertEqual(len(entities), 1)
        self.assertEqual(entities[0]["entity_id"], "sensor.test")

    @patch('home_assistant_helper.sqlite3.connect')
    def test_save_entities_to_db(self, mock_connect):
        mock_conn = MagicMock()
        mock_connect.return_value = mock_conn
        entities = [{"entity_id": "sensor.test", "state": "on",
                     "attributes": {"friendly_name": "Test Sensor"}}]

        hah.save_entities_to_db(entities)

        mock_conn.cursor.return_value.execute.assert_called()
        mock_conn.commit.assert_called()
        mock_conn.close.assert_called()

    @patch('builtins.print')
    def test_print_entities(self, mock_print):
        entities = [{"entity_id": "sensor.test", "state": "on",
                     "attributes": {"friendly_name": "Test Sensor"}}]
        hah.print_entities(entities)

        mock_print.assert_called()
        self.assertTrue(
            any(
                "sensor.test" in call[0][0] for call in mock_print.call_args_list)  # noqa E501
        )

    @patch('home_assistant_helper.sqlite3.connect')
    def test_purge_database(self, mock_connect):
        mock_conn = MagicMock()
        mock_connect.return_value = mock_conn

        hah.purge_database()

        mock_conn.cursor.return_value.execute.assert_called()
        mock_conn.commit.assert_called()
        mock_conn.close.assert_called()

    @patch('home_assistant_helper.sqlite3.connect')
    def test_save_log_to_db(self, mock_connect):
        mock_conn = MagicMock()
        mock_connect.return_value = mock_conn

        hah.save_log_to_db("Test log message")

        mock_conn.cursor.return_value.execute.assert_called()
        mock_conn.commit.assert_called()
        mock_conn.close.assert_called()

    @patch('home_assistant_helper.logging.info')
    @patch('home_assistant_helper.save_log_to_db')
    def test_log_method_call(self, mock_save_log_to_db, mock_logging_info):
        hah.log_method_call("test_method", "test details")

        log_message_pattern = re.compile(
            r'\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}\.\d+: Called test_method with details: test details')  # noqa E501
        self.assertTrue(any(log_message_pattern.match(
            call[0][0]) for call in mock_logging_info.call_args_list))
        mock_save_log_to_db.assert_called()

    @patch('builtins.open', new_callable=mock_open, read_data="Log file content\n" * 100)  # noqa E501
    @patch('home_assistant_helper.os.path.exists')
    @patch('builtins.print')
    def test_display_logs(self, mock_print, mock_exists, mock_open):
        mock_exists.return_value = True

        hah.display_logs()

        self.assertTrue(mock_print.called)
        self.assertTrue(
            any("Log file content" in call[0][0] for call in mock_print.call_args_list))  # noqa E501


if __name__ == "__main__":
    unittest.main()
