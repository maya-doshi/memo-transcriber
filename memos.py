import requests as rq
import os

API_EP = '/api/v1/'
MEMO_LIST_EP = f"{API_EP}memos?pageSize=50000"

TAG_INCLUDE = [ 'vlog', 'log', 'voice', 'voice_note' ]
TAG_EXCLUDE = [ 'wrct' ]
RESOURCE_TYPES = [ 'audio', 'video' ]

def is_type(resource):
  return resource['type'].split('/')[0] in RESOURCE_TYPES

def has_not_tag(memo):
  for tag in TAG_EXCLUDE:
    if tag in memo['tags']:
      return False
  return True

def get_transcripts(desc):
  return dict(map(lambda x: x.split('\n', 1), filter(lambda x: len(x) > 1, desc.split('```'))))

# this should really be a regex lol
def norm_name(name):
  return name.replace(' ', '_').replace('.', '_').replace('-', '_').replace("'", '_').replace('__', '_')

def gen_desc(transcripts):
  final = ""
  for name, trans in transcripts.items():
    final += f"\n```{name}\n{trans}\n```"
  return final

class Memos:
  def __init__(self, url, token, delim = "\n---\n---"):
    self.base_url = url
    self.headers = { "Authorization": f"Bearer {token}", }
    self.delim = delim

  def get(self, url):
    return rq.get(url, headers=self.headers)

  def patch(self, url, json):
    return rq.patch(url, headers=self.headers, json=json)

  def get_resource(self, resource, temp_dir):
    url = self.base_url + '/file/' + resource['name'] + '/' + resource['filename']
    resp = self.get(url)
    if resp.status_code != 200:
      print('resource retrival fail')
      return None

    tempfile_path = os.path.join(temp_dir, resource['filename'])
    with open(tempfile_path, 'wb') as file:
      file.write(resp.content)
    return tempfile_path

  def get_memo(self, name):
    url = f'{self.base_url}{API_EP}{name}'
    resp = self.get(url)
    if resp.status_code != 200:
      print('get memo failure')
      return {}

    return resp.json()

  def get_existing_transcripts(self, memo):
    splitted = memo["content"].split(self.delim)

    transcripts = {}
    if len(splitted) > 1:
      transcripts = get_transcripts(splitted[1])
    return transcripts

  def update_memo(self, memo, resource, transcript):
    url = f'{self.base_url}{API_EP}{memo["name"]}'

    transcripts = self.get_existing_transcripts(memo)
    transcripts[norm_name(resource['filename'])] = transcript
    splitted = memo["content"].split(self.delim)
    json = { 'content': f'{splitted[0]}{self.delim}{gen_desc(transcripts)}', }

    resp = self.patch(url, json)
    if resp.status_code != 200:
      print('patch memo failure')
      return {}

    return resp.json()

  def get_memos(self):
    resp = self.get(self.base_url+MEMO_LIST_EP)
    if resp.status_code != 200:
      print('get memo failure')
      return
    return resp.json()

  def get_resources_transcribe(self, memo):
    if not has_not_tag(memo):
      return []

    return filter(is_type, memo['resources'])


  def get_resources_transcribe_all(self):
    memos = filter(has_not_tag, self.get_memos()['memos'])
    resources = filter(is_type, sum(map(lambda x: x['resources'], memos), []))
    return list(resources)
