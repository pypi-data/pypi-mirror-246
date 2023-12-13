# Person Cache

Cache para aplicacoes python com Redis ou em Memoria Local.

## Exemplo de Utilizacao

```python
from person_cache.main import RedisSingleton as cache
from person_cache.main import LocalCache

cache(url_redis="redis://default:redis1234@localhost:6379/0")
LocalCache()

@cache.cache_response(key_prefix="teste", expire_time=600, skip_args=0)
async def teste(abc):
    return 1 + abc

@LocalCache.cache_response(key_prefix="teste1", expire_time=600, skip_args=0)
async def teste1(abc):
    return 5 * abc

```

## Como Usar

- Para cache com redis, necessário incluir a **url_redis** para instanciar a classe. Já para o cache local não é necessário.

- Ao utilizar o decorator, em ambos os casos, é necessário informar:
    
    - **key_prefix**: Prefixo que será utilizado para compor a chave do chave;
    - **expire_time**: tempo em segundos para expirar o cache;
    - **skip_args**: a quantidade de args que deve ser desprezada para compor a chave do cache. Isso se faz necessários em caso que é informado por referencia a dependecia de banco de dados, por exemplo;


* O person cache foi idealizado considerando aplicacoes assincronas.


