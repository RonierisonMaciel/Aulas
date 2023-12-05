# Como usar o Fernet

1. Python interativo

```python
from cryptography.fernet import Fernet
key = Fernet.generate_key()
print(key)
```
