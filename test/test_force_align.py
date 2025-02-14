#!/usr/bin/env python3

"""
Test force-alignment with SoundsSwallower FSG search from Python API
"""

import os
import unittest

from basic_test_case import BasicTestCase
from lxml import etree

from readalongs.align import align_audio, convert_to_xhtml, create_input_tei
from readalongs.log import LOGGER
from readalongs.portable_tempfile import PortableNamedTemporaryFile
from readalongs.text.util import load_txt, save_xml


class TestForceAlignment(BasicTestCase):
    """Unit testing suite for forced-alignment with SoundsSwallower"""

    def test_align(self):
        """Basic alignment test case with XML input"""
        xml_path = os.path.join(self.data_dir, "ej-fra.xml")
        wav_path = os.path.join(self.data_dir, "ej-fra.m4a")
        results = align_audio(xml_path, wav_path, unit="w")

        # Verify that the same IDs are in the output
        converted_path = os.path.join(self.data_dir, "ej-fra-converted.xml")
        xml = etree.parse(converted_path).getroot()
        words = results["words"]
        xml_words = xml.xpath(".//w")
        self.assertEqual(len(words), len(xml_words))
        for w, xw in zip(words, xml_words):
            self.assertEqual(xw.attrib["id"], w["id"])

    def test_align_text(self):
        """Basic alignment test case with plain text input"""
        txt_path = os.path.join(self.data_dir, "ej-fra.txt")
        wav_path = os.path.join(self.data_dir, "ej-fra.m4a")
        _, temp_fn = create_input_tei(
            input_file_name=txt_path, text_languages=("fra",), save_temps=None
        )
        results = align_audio(temp_fn, wav_path, unit="w", save_temps=None)

        # Verify that the same IDs are in the output
        converted_path = os.path.join(self.data_dir, "ej-fra-converted.xml")
        xml = etree.parse(converted_path).getroot()
        words = results["words"]
        xml_words = xml.xpath(".//w")
        self.assertEqual(len(words), len(xml_words))
        for w, xw in zip(words, xml_words):
            self.assertEqual(xw.attrib["id"], w["id"])


class TestXHTML(BasicTestCase):
    """Test converting the output to xhtml"""

    def test_convert(self):
        """Test converting the output to xhtml"""
        xml_path = os.path.join(self.data_dir, "ej-fra-converted.xml")
        xml = etree.parse(xml_path).getroot()
        convert_to_xhtml(xml)
        with PortableNamedTemporaryFile(suffix=".xml") as tf:
            save_xml(tf.name, xml)
            txt = load_txt(tf.name)
            self.maxDiff = None
            self.assertEqual(
                txt, load_txt(os.path.join(self.data_dir, "ej-fra-converted.xhtml")),
            )


if __name__ == "__main__":
    LOGGER.setLevel("DEBUG")
    unittest.main()
