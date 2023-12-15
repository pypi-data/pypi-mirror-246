# robotgpt-interpreter



## Getting started

```python
import interpreter
interpreter.model="openai/gpt-4"
interpreter.api_base="https://dataai.harix.iamidata.com/llm/api/ask"
interpreter.api_key="eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJrZXkiOiJkY2UwYzU2NjJlYTY0NjNiOTUyMGU5YTUxYmFlMiIsImV4cCI6MTcwMjYyMzQ0NSwiaWF0IjoxNzAyNTM3MDQ1LCJzdWIiOiJibGZS56aGFuZyJ9.rZeUMWmHpzP6CA6oYlrlMdJ7eB9T_lhZ_NHAklYI"
interpreter.chat("hello")
```

## 更新
python3.10 setup.py sdist bdist_wheel
/Library/Frameworks/Python.framework/Versions/3.10/bin/twine check dist/* 
/Library/Frameworks/Python.framework/Versions/3.10/bin/twine upload dist/* 