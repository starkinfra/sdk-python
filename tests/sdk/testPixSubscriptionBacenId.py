import re
import starkinfra
from unittest import TestCase, main
from datetime import datetime


class TestPixSubscriptionBacenId(TestCase):

    def test_success(self):
        bacen_id = starkinfra.pixsubscriptionbacenid.create("32160637", "RR")
        self.assertEqual(29, len(bacen_id))
        self.assertIsNotNone(re.fullmatch(r"RR32160637\d{8}[a-zA-Z0-9]{11}", bacen_id))
        self.assertEqual(datetime.utcnow().strftime("%Y%m%d"), bacen_id[10:18])

    def test_random_part_differs(self):
        first = starkinfra.pixsubscriptionbacenid.create("32160637", "RR")
        second = starkinfra.pixsubscriptionbacenid.create("32160637", "RR")
        self.assertNotEqual(first, second)

    def test_non_string_arguments_are_stringified_and_left_to_the_api(self):
        none_prefix = starkinfra.pixsubscriptionbacenid.create("32160637", None)
        number_prefix = starkinfra.pixsubscriptionbacenid.create(32160637, 12)
        none_bank_code = starkinfra.pixsubscriptionbacenid.create(None, "RR")
        self.assertIsNotNone(re.fullmatch(r"None32160637\d{8}[a-zA-Z0-9]{11}", none_prefix))
        self.assertIsNotNone(re.fullmatch(r"1232160637\d{8}[a-zA-Z0-9]{11}", number_prefix))
        self.assertIsNotNone(re.fullmatch(r"RRNone\d{8}[a-zA-Z0-9]{11}", none_bank_code))

    def test_end_to_end_id_and_return_id_keep_minute_precision(self):
        end_to_end_id = starkinfra.endtoendid.create("32160637")
        return_id = starkinfra.returnid.create("32160637")
        self.assertEqual(32, len(end_to_end_id))
        self.assertEqual(32, len(return_id))
        self.assertIsNotNone(re.fullmatch(r"E32160637\d{12}[a-zA-Z0-9]{11}", end_to_end_id))
        self.assertIsNotNone(re.fullmatch(r"D32160637\d{12}[a-zA-Z0-9]{11}", return_id))


if __name__ == '__main__':
    main()
