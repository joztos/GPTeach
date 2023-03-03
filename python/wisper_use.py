import whisper
import pyaudio
import wave
import os

chunk = 1024
format = pyaudio.paInt32
channels = 1
rate = 16000
record_seconds = 6
here = os.path.dirname(os.path.abspath(__file__))
filename = os.path.join(here, 'sample.mp3') 

p = pyaudio.PyAudio()


def get_audio():

    stream = p.open(format=format,
                    channels=channels,
                    rate=rate,
                    input=True,
                    frames_per_buffer=chunk)

    frames = []

    print("Recording...")
    for i in range(0, int(rate / chunk * record_seconds)):
        data = stream.read(chunk)
        frames.append(data)

    stream.stop_stream()
    stream.close()

    print("Finished recording.")

    wf = wave.open(filename, 'wb')
    wf.setnchannels(channels)
    wf.setsampwidth(p.get_sample_size(format))
    wf.setframerate(rate)
    wf.writeframes(b''.join(frames))
    wf.close()

    print(filename)

get_audio()

model = whisper.load_model("base") 

result = model.transcribe(filename,fp16=False)
print(result["text"])


# Write the output to a file
f = open("output.txt", "w")
f.write(result["text"])
f.close()