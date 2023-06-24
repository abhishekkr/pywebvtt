
## pywebvtt

> to parse WebVTT subtitle file into a traversable data structure
>
> [pypi/pywebvtt](https://pypi.org/project/pywebvtt/)

* to run tests `poetry install && poetry run pytest`

* to run example `poetry install && poetry run python examples/parse-sample.py`

* sample usage `pip install pywebvtt` and

```
import pywebvtt


scenes = pywebvtt.ParseFile('sample.vtt')
for s in scenes:
    # every scene has: s.start, s.end, s.start_millisec, s.end_millisec, s.transcript
    print(s.string())
```

---

### ToDo

> [source: VTT Mozilla doc](https://developer.mozilla.org/en-US/docs/Web/API/WebVTT_API)

* add support for multi-line NOTE

* add support for Style & Cue blocks

---
