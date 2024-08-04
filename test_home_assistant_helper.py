import unittest
from unittest.mock import patch, MagicMock
import home_assistant_helper as hah


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

    @patch('home_assistant_helper.print')
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
        mock_conn = MagicMock()  # noqa E481
        mock_connect.return_value
