from unittest.mock import patch

from django.core.management import call_command  # call command from source code
from django.db.utils import OperationalError     # this throws error when django is not available
from django.test import TestCase


class CommandTests(TestCase):

    def test_wait_for_db_ready(self):
        """Test waiting for db when db is available"""
        with patch('django.db.utils.ConnectionHandler.__getitem__') as gi:
            gi.return_value = True
            call_command('wait_for_db')  # wait for db is name of management command
            self.assertEqual(gi.call_count, 1)

    @patch('time.sleep', return_value=True)  # replaces the time.sleep with return value
    def test_wait_for_db(self, ts):
        """Test waiting for db"""
        with patch('django.db.utils.ConnectionHandler.__getitem__') as gi:
            gi.side_effect = [OperationalError] * 5 + [True]
            call_command('wait_for_db')
            self.assertEqual(gi.call_count, 6)

