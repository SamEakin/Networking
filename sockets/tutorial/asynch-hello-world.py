# Python has a built in library for Asynchronous capabilities.
# Allows us to run processes concurrently in "threads"
import asyncio

async def main():
	print('Hello...')
	await asyncio.sleep(1)
	print('... World!')

asyncio.run(main())