import time
import tempfile
import gc
import os

from flask import Flask, request, jsonify

from memos import Memos, sanitize_name
from transcribe import Transcriber

MODEL_SIZE = os.environ['MODEL_SIZE']
BASE_URL = os.environ['BASE_URL']
TOKEN = os.environ['TOKEN']
PORT = os.environ['PORT']

TAG_INCLUDE = [ 'vlog', 'log', 'voice', 'voice_note' ]
TAG_EXCLUDE = [ 'wrct' ]
RESOURCE_TYPES = [ 'audio', 'video' ]

WEBHOOK_UPDATE =  [ 'memos.memo.created', 'memos.memo.updated' ]

t = Transcriber(MODEL_SIZE, threads=12)
m = Memos(BASE_URL, TOKEN)
f = Flask(__name__)

def transcribe_resource(r):
  with tempfile.TemporaryDirectory() as temp_dir:
    print(r)
    transcript = t.transcribe(m.get_resource(r, temp_dir))
    if len(transcript.split('\n')) > 1:
        memo = m.get_memo(r['memo'])
        print(m.update_memo(memo, r, transcript))

def transcribe_resources(rs):
  for r in rs:
    transcribe_resource(r)

def do_all():
  rs = m.get_resources_transcribe_all()
  transcribe_resources(rs)

def transcribe_memo(memo_name):
  memo = m.get_memo(memo_name)
  rs = memo['resources']

  transcribe_resource(rs)


@f.route('/webhook', methods=[ 'POST' ])
def webhook():
  #try:
  data = request.json
  if data['activityType'] in WEBHOOK_UPDATE:
    memo = m.get_memo(data['memo']['name'])
    transcripts = m.get_existing_transcripts(memo)
    rs = m.get_resources_transcribe(memo)
    # TODO: make this better
    # - [ ] function so it's not repeated
    # - [ ] possible to update transcript if model is different
    for r in rs:
      transcript = transcripts.get(sanitize_name(r['filename']), None)
      if transcript is None:
        transcribe_resource(r)
  return jsonify({'status': 'success'})
  #except:
    #print('oopsie!')
    #return jsonify({'status': 'failure'})

if __name__ == '__main__':
  f.run(host='0.0.0.0', port=PORT)
