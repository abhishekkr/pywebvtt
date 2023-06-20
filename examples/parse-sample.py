import pywebvtt


scenes = pywebvtt.ParseFile('sample.vtt')
for s in scenes:
    print(s.string())
