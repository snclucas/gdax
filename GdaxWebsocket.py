import json
import asyncio
import websockets


async def subscribe(subscribe_string):
    async with websockets.connect('wss://ws-feed.gdax.com') as webs:
        await webs.send(str(subscribe_string))

        greeting = await webs.recv()
        print(greeting)


subscribe_string_tosend = {
    "type": "subscribe",
    "product_ids": [
        "ETH-USD"
    ],
    "channels": [
        "level2",
        "heartbeat",
        {
            "name": "ticker",
            "product_ids": [
                "ETH-USD"
            ]
        },
    ]
}


print(subscribe_string_tosend)

subscribe_string_tosend_json = json.dumps(subscribe_string_tosend)

print(subscribe_string_tosend_json)

asyncio.get_event_loop().run_until_complete(subscribe(subscribe_string_tosend_json))

