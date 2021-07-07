from unittest.mock import patch

from django.core.management import call_command  # call command from source code
from django.db.utils import OperationalError     # this throws error when django is not available
from django.test import TestCase