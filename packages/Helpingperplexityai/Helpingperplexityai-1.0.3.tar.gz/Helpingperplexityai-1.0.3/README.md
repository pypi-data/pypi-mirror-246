# Helpingperplexityai

A simple module to use Perplexity AI in Python.

## Get started:

```
python -m pip install -U Helpingperplexityai
```

## Example:

```python
from Helpingperplexityai import Helpingperplexityai

prompt = input("👦: ")
for a in Helpingperplexityai().generate_answer(prompt):
    print(f"🤖: {a['answer']}")
```

*Thanks to [nathanrchn's perplexityai](https://github.com/nathanrchn/perplexityai) for the original code.*
