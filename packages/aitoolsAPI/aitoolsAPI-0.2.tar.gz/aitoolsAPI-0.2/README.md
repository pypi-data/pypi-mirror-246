# aitoolsAPI

This is a simple async API client library for aitoolsAPI.

## Installation

You can install the library using pip:

pip install aitoolsAPI

## Using

Since this library is asynchronous, you should write the code like this:

GPT request:

```
import asyncio
import aitoolsAPI

async def main(prompt):
  print(await aitoolsAPI.gpt(prompt)) # Will send a response as text

asyncio.run(main("What package of sanctions was imposed on Russia last time?"))
```

SDXL request:

```
import asyncio
import aitoolsAPI

async def main(prompt):
  print(await aitoolsAPI.sdxl(prompt)) # Will send the answer in the form of a link

asyncio.run(main("Red ball flies among the clouds, 4K, realistic, no blur"))
```
