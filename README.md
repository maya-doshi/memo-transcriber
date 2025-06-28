# memo transcriber
currently a pretty barebones mvp. works with a webhook on port 5000 with a function to transcribe all memos which meet requirements if you want. probably a lot of bugs and typos

adds transcripts like this:
![transcripts example](./_imgs/mvp_screenshot.webp)

## usage
1. fill all the variables in the code, modify the filters and stuff
2. get all requirements (ive only tried the nix stuff)
3. run `python main.py`
2. add the webhook to your memos instance

### optional
- run `do_all()` if u want, this is still pretty rough. there will be a better way eventually

## motivation
be able to see what i log without having to download the whole video/audio file which can be several gigabytes. also searchability

## TODO
- [ ] figure out a better name for this (super important, obviously)
- [ ] make the code not a disaster
  - [ ] env vars instead of hardcoded
  - [ ] figure out unloading the model in downtime
  - [ ] package properly
  - [ ] error handling
  - [ ] more robust filtering of which memos should be transcribed
- [ ] docker image
- [ ] barebones webui
- [ ] add option for external transcription
