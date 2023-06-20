
## pywebvtt

> to parse WebVTT subtitle file into a traversable data structure

* to run tests `poetry install && poetry run pytest`

* to run example `poetry install && poetry run python examples/parse-sample.py`

* sample usage

```
import pywebvtt


scenes = pywebvtt.ParseFile('sample.vtt')
for s in scenes:
    # every scene has: s.start, s.end, s.start_millisec, s.end_millisec, s.transcript
    print(s.string())
```

---
