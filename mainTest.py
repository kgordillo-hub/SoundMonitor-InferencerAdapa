from inferencer.Adapatask5 import DcaseAdapatask5
import base64
import io
import soundfile as sf
import os

inferencer = DcaseAdapatask5()

audio = open(os.environ['TEST_AUDIO_FILE'], 'rb').read()

audioBase64 = base64.b64encode(audio)

audioDecoded = base64.decodebytes(audioBase64)

data, samplerate = sf.read(io.BytesIO(audioDecoded))

result = inferencer.runInferencer(data, samplerate)

print(result)