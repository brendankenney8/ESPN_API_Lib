from NFL_API import Game
import asyncio

async def main():
	result = await Game.get(401671834)
	print(result)

if __name__ == "__main__":
	asyncio.run(main())
