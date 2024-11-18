# ai-searcher

This repository converts the audio files of WhatsApp to get a transcription and then can find your required part

## Starter

To run this program in a clean way you just need to build the docker image and get access to read the audio files

```bash
  docker build -t whisper .
  docker run --rm whisper --volume ./resources:/app/resources
```

## Resources

- [Whisper](https://github.com/openai/whisper)
- [Faster whisper](https://github.com/SYSTRAN/faster-whisper)
