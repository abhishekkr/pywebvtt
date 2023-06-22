import pywebvtt


"""
options = pywebvtt.Options({
    max_lines: 2,
    max_chars_per_line: 16,
})
"""
options = pywebvtt.Options()
scenes = pywebvtt.ParseFileWithOptions('sample.vtt', options)
for s in scenes:
    print(s.string())
