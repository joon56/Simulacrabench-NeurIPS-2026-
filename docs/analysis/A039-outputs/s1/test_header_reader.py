"""New in-memory boundary examples only; never opens respondent files."""
import io
import json
import unittest

from header_reader import HeaderHold, read_header


class GuardedBytes(io.BytesIO):
    def __init__(self, data):
        super().__init__(data)
        self.boundary = data.find(b"\n") + 1 or len(data)
        self.requests = []

    def read(self, size=-1):
        self.requests.append(size)
        if size != 1 or self.tell() >= self.boundary:
            raise AssertionError("Read outside first physical line")
        return super().read(size)


class HeaderBoundaryTests(unittest.TestCase):
    def test_normal_stops_before_response(self):
        stream = GuardedBytes(b"ID_main,Form\nDO_NOT_READ\n")
        raw, names = read_header(stream)
        self.assertEqual(names, ["ID_main", "Form"])
        self.assertEqual(raw, b"ID_main,Form\n")
        self.assertEqual(stream.tell(), stream.boundary)
        self.assertEqual(stream.requests, [1] * len(raw))

    def test_bom_crlf_and_quoted_delimiter(self):
        stream = GuardedBytes(b'\xef\xbb\xbf"ID_main","a,b"\r\nDO_NOT_READ')
        raw, names = read_header(stream)
        self.assertEqual(names, ["ID_main", "a,b"])
        self.assertTrue(raw.endswith(b"\r\n"))

    def test_duplicate_and_whitespace_preserved(self):
        _, names = read_header(GuardedBytes(b"ID_main, Form ,ID_main\nSECRET"))
        self.assertEqual(names, ["ID_main", " Form ", "ID_main"])

    def test_quoted_newline_stops_at_first_lf(self):
        stream = GuardedBytes(b'ID_main,"broken\nsecond line"\nSECRET')
        with self.assertRaises(HeaderHold):
            read_header(stream)
        self.assertEqual(stream.tell(), stream.boundary)

    def test_bad_utf8_no_raw_exception(self):
        with self.assertRaisesRegex(HeaderHold, "UTF8_INVALID"):
            read_header(GuardedBytes(b"ID_main,\xff\nSECRET"))

    def test_suspicious_values_no_raw_exception(self):
        for header in (b"123,456\nSECRET", b"ID_main,\nSECRET", b"ID_main,2024-01-02\nSECRET"):
            with self.subTest(header_shape=len(header)):
                with self.assertRaisesRegex(HeaderHold, "SUSPICIOUS_HEADER"):
                    read_header(GuardedBytes(header))

    def test_malformed_quotes(self):
        for header in (b'ID_main,a"b\nSECRET', b'ID_main,"a"junk\nSECRET'):
            with self.assertRaises(HeaderHold):
                read_header(GuardedBytes(header))

    def test_limit_does_not_request_extra_byte(self):
        stream = GuardedBytes(b"LongName,Other\nSECRET")
        with self.assertRaisesRegex(HeaderHold, "HEADER_LIMIT"):
            read_header(stream, limit=5)
        self.assertEqual(stream.tell(), 5)

    def test_missing_lf(self):
        with self.assertRaisesRegex(HeaderHold, "NO_LF"):
            read_header(io.BytesIO(b"ID_main,Form"))


if __name__ == "__main__":
    result = unittest.TextTestRunner(verbosity=2).run(
        unittest.defaultTestLoader.loadTestsFromTestCase(HeaderBoundaryTests)
    )
    print(json.dumps({"tests": result.testsRun, "pass": result.wasSuccessful(),
                      "actual_data_opens": 0}))
    raise SystemExit(0 if result.wasSuccessful() else 1)
