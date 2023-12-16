# Helpingperplexityai

A simple module to use Perplexity AI in Python.

## Get started:

```
python -m pip install -U Helpingperplexityai
```

## Example:

```python
from Helpingperplexityai import Perplexity

prompt = input("👦: ")
for a in Perplexity().generate_answer(prompt):
    print(f"🤖: {a['answer']}")
```

