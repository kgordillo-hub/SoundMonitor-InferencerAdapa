import unittest
from inferencer.Adapatask5 import DcaseAdapatask5
import soundfile as sf
import io


class TestStringMethods(unittest.TestCase):

    def test_inferencer(self):
        inferencer = DcaseAdapatask5()
        audio = open('test/test_audio.wav', 'rb')
        data, samplerate = sf.read(io.BytesIO(audio.read()))
        result = inferencer.runInferencer("", data, samplerate)
        audio.close()

        resultExpectedKeys = ['audio_filename', 'small-sounding-engine',
       'medium-sounding-engine', 'large-sounding-engine',
       'engine-of-uncertain-size', 'rock-drill', 'jackhammer',
       'hoe-ram', 'pile-driver', 'other-unknown-impact-machinery',
       'non-machinery-impact', 'chainsaw',
       'small-medium-rotating-saw', 'large-rotating-saw',
       'other-unknown-powered-saw', 'car-horn', 'car-alarm',
       'siren', 'reverse-beeper', 'other-unknown-alert-signal',
       'stationary-music', 'mobile-music', 'ice-cream-truck',
       'music-from-uncertain-source', 'person-or-small-group-talking',
       'person-or-small-group-shouting', 'large-crowd',
       'amplified-speech', 'other-unknown-human-voice',
       'dog-barking-whining', 'engine', 'machinery-impact',
       'non-machinery-impact', 'powered-saw', 'alert-signal', 'music',
       'human-voice', 'dog']
        self.assertEqual(result.keys().tolist(), resultExpectedKeys)


if __name__ == '__main__':
    unittest.main()