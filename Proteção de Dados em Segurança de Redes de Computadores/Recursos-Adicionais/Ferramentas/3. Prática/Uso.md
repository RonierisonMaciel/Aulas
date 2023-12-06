# Como usar o Fernet

1. Digite no seu terminal Python. Em seguida faça esse passo a passo para criar uma chave usando o Fernet.

```python
>> from cryptography.fernet import Fernet
>> key = Fernet.generate_key()
>> print(key)
```
