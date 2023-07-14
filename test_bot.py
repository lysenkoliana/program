from bot import*
import unittest
#arg=message.get_args()
YDL_OPTIONS={'format': 'bestaudio/best',
             'noplaylist': 'True',
             'postprocessors': [{
                 'key': 'FFmpegExtractAudio' ,
                 'preferredcodec': 'mp3',
                 'preferredquality': '192'
                 }]
}
class Test_work(unittest.TestCase):
    def setUp(self):
        pass
    def tearDown(self):
        pass
    def test_test_work(self):
        self.assertEqual(type(search_cmd(YDL_OPTIONS)), tuple)

unittest.main()
