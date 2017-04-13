#!/usr/bin/env python
# coding=utf-8
import unittest

from flask import current_app
from app import create_app, db


class BasicsTestCase(unittest.TestCase):
    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_app_exists(self):
        pass

    def test_app_is_testing(self):
        pass
