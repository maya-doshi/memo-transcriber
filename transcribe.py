from datetime import datetime, timezone
import gc
from faster_whisper import WhisperModel

class Transcriber:
    def __init__(self, model_size, threads=4):
      self.model_size = model_size
      self.threads = threads
      self.model = None

    def load(self):
      self.model = WhisperModel(self.model_size, device="cpu", compute_type="int8", cpu_threads=self.threads)

    def unload(self):
      del self.model
      gc.collect()
      self.model = None

    def transcribe(self, file_path):
      if self.model is None:
        self.load()
      segments, info = self.model.transcribe(file_path, beam_size=5, vad_filter=True)
      transcript = f'{datetime.now(timezone.utc).isoformat()} - {self.model_size}:'
      for segment in segments:
        transcript += f'\n{segment.text}'
      return transcript
