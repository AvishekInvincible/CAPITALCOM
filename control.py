running =True
import asyncio

loop = asyncio.new_event_loop()

def stop():
  loop.stop()