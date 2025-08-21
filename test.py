from espn_api import Game

def main():
	result = Game.get(401671834)
	print(result)

if __name__ == "__main__":
	main()
