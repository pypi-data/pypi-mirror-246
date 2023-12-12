import json
import os
import unittest
from contentstack_utils import Utils
from contentstack_utils.render.options import Options
from tests.mocks.supercharged.results import Results


def __is_json(file):
    try:
        json.dumps(file)
        return True
    except ValueError:
        return False


def load_mock():
    path = os.path.join(
        os.path.dirname(os.path.abspath(__file__)),
        'mocks/supercharged', 'supercharged.json')
    with open(path) as file:
        return json.load(file)


class TestSuperchargedUtils(unittest.TestCase):
    global _json_data  # Note that the PyCharm warnings are not actual python errors

    def setUp(self):
        self._json_data = load_mock()

    def test_plaintext_in_supercharged_dict_to_html(self):
        array_str = ['plaintext']
        Utils.json_to_html(self._json_data, array_str, Options())
        self.assertEqual(Results.plainTextHtml, self._json_data['plaintext'])

    def test_plaintext_in_supercharged_list_to_html(self):
        array_str = ['plaintext_array']
        Utils.json_to_html(self._json_data, array_str, Options())
        self.assertEqual(Results.plainTextHtml, self._json_data['plaintext_array'][0])

    def test_paragraph_in_supercharged_dict_to_html(self):
        array_str = ['paragraph']
        Utils.json_to_html([self._json_data], array_str, Options())
        self.assertEqual(Results.paragraphHtml, self._json_data['paragraph'])

    def test_h1_in_supercharged_dict_to_html(self):
        array_str = ['h_one']
        Utils.json_to_html([self._json_data], array_str, Options())
        self.assertEqual(Results.h1Html, self._json_data['h_one'])

    def test_h2_in_supercharged_dict_to_html(self):
        array_str = ['h_two']
        Utils.json_to_html([self._json_data], array_str, Options())
        self.assertEqual(Results.h2Html, self._json_data['h_two'])

    def test_h3_in_supercharged_dict_to_html(self):
        array_str = ['h_three']
        Utils.json_to_html([self._json_data], array_str, Options())
        self.assertEqual(Results.h3Html, self._json_data['h_three'])

    def test_h4_in_supercharged_dict_to_html(self):
        array_str = ['h_four']
        Utils.json_to_html([self._json_data], array_str, Options())
        self.assertEqual(Results.h4Html, self._json_data['h_four'])

    def test_h5_in_supercharged_dict_to_html(self):
        array_str = ['h_five']
        Utils.json_to_html([self._json_data], array_str, Options())
        self.assertEqual(Results.h5Html, self._json_data['h_five'])

    def test_h6_in_supercharged_dict_to_html(self):
        array_str = ['h_six']
        Utils.json_to_html([self._json_data], array_str, Options())
        self.assertEqual(Results.h6Html, self._json_data['h_six'])

    def test_order_list_in_supercharged_dict_to_html(self):
        array_str = ['order_list']
        Utils.json_to_html([self._json_data], array_str, Options())
        self.assertEqual(Results.orderListHtml, self._json_data['order_list'])

    def test_un_order_list_in_supercharged_dict_to_html(self):
        array_str = ['un_order_list']
        Utils.json_to_html([self._json_data], array_str, Options())
        self.assertEqual(Results.unorderListHtml, self._json_data['un_order_list'])

    def test_image_list_in_supercharged_dict_to_html(self):
        array_str = ['img']
        Utils.json_to_html([self._json_data], array_str, Options())
        self.assertEqual(Results.imgHtml, self._json_data['img'])

    def test_table_list_in_supercharged_dict_to_html(self):
        array_str = ['table']
        Utils.json_to_html([self._json_data], array_str, Options())
        self.assertEqual(Results.tableHtml, self._json_data['table'])

    def test_blockquote_list_in_supercharged_dict_to_html(self):
        array_str = ['blockquote']
        Utils.json_to_html([self._json_data], array_str, Options())
        self.assertEqual(Results.blockquoteHtml, self._json_data['blockquote'])

    def test_code_list_in_supercharged_dict_to_html(self):
        array_str = ['code']
        Utils.json_to_html([self._json_data], array_str, Options())
        self.assertEqual(Results.codeHtml, self._json_data['code'])

    def test_linkin_list_in_supercharged_dict_to_html(self):
        array_str = ['link']
        Utils.json_to_html([self._json_data], array_str, Options())
        self.assertEqual(Results.linkInPHtml, self._json_data['link'])

    # def test_reference_list_in_supercharged_dict_to_html(self):
    #     array_str = ['reference']
    #     Utils.json_to_html([self._json_data], array_str, Options())
    #     self.assertEqual(Results.linkInPHtml, self._json_data['reference'])
