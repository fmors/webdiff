import json
import unittest

from ddt import unpack, data, ddt
from flask import Flask

from v1.routes import compare_left_and_right, post_diff_id_side, show_diff_id
import v1.routes


@ddt
class TestRoutes(unittest.TestCase):
    @unpack
    @data(
        (b'1234567890', b'1234567890', {'result': 'Left and right contents are the same'}),
        (b'1234567890', b'123456789', {'result': 'Left and right sizes do not match'}),
        (
                b'1234567890',
                b'1212565690',
                {
                    'result': 'Left and right contents do not match',
                    'differences': [
                        {'offset': 2, 'size': 2},
                        {'offset': 6, 'size': 2}
                    ]
                }
        )
    )
    def test_compare_left_and_right(self, left, right, expected_result):
        result = compare_left_and_right(left, right)
        self.assertEqual(result, expected_result)

    @unpack
    @data(
        (
            1, 'left', 'application/json', '{"data": "sdfkjsdfhaksjlhfasdkjh"}',
            {'result': 'Diff session 1 left side successfully set'}, 200
        ),
        (
            13, 'right', 'application/json', '{"data": "asdfkjhasfdkjhsdfkjkjh"}',
            {'result': 'Diff session 13 right side successfully set'}, 200
        ),
        (
            8, 'right', 'text/html', '{"data": "asdfkjhasfdkjhsdfkjkjh"}',
            {'error': 'Invalid data type: only \'application/json\' accepted'}, 400
        ),
        (
            7, 'center', 'anything', 'anything',
            {'error': 'Only left or right side accepted.'}, 400
        ),
        (
            2, 'right', 'application/json', '{"data2": "asdfkjhasfdkjhsdfkjkjh"}',
            {'error': 'No \'data\' received'}, 400
        ),
        (
            3, 'left', 'application/json', '{"data": ""}',
            {'error': 'Empty \'data\' received'}, 400
        )
    )
    def test_post_diff_id_side(self, diff_id, side, content_type, data, expected_msg, expected_status):
        app = Flask(__name__)

        with app.test_request_context('/v1/diff/1/left', method='POST', content_type=content_type, data=data):
            result = post_diff_id_side(diff_id, side)
            self.assertEqual(result.status_code, expected_status)
            self.assertEqual(json.loads(result.data), expected_msg)

    def test_post_diff_id_side_fill(self):
        # Test the case of filling up the max number of sessions and
        # adding an extra session to check if we get the expected error
        app = Flask(__name__)

        with app.test_request_context('/v1/diff/1/left',
                                      method='POST',
                                      content_type='application/json',
                                      data='{"data": "123456"}'):

            max_number_of_sessions = 16
            for i in range(max_number_of_sessions):
                result = post_diff_id_side(i, 'left')
                self.assertEqual(result.status_code, 200)
                self.assertEqual(json.loads(result.data),
                                 {'result': 'Diff session {} left side successfully set'.format(i)})

            result = post_diff_id_side(max_number_of_sessions, 'left')
            self.assertEqual(result.status_code, 400)
            self.assertEqual(json.loads(result.data),
                             {'error': 'Max number of diff sessions ({}) reached.'.format(max_number_of_sessions)})

    @unpack
    @data(
        (
            1, {1: {'left': 'abc', 'right': 'abc'}}, {'result': 'Left and right contents are the same'}, 200
        ),
        (
            2, {1: {'left': 'abc', 'right': 'abc'}}, {'error': 'Diff session ID not found'}, 404
        ),
        (
            3, {3: {'left': 'abc'}}, {'error': 'Right side missing'}, 400
        ),
        (
            4, {4: {'right': 'abc'}}, {'error': 'Left side missing'}, 400
        ),
    )
    def test_show_diff_id(self, diff_id, sessions, expected_msg, expected_status):
        app = Flask(__name__)

        v1.routes.diff_sessions = sessions

        with app.test_request_context('/v1/diff/1'):
            result = show_diff_id(diff_id)
            self.assertEqual(result.status_code, expected_status)
            self.assertEqual(json.loads(result.data), expected_msg)
