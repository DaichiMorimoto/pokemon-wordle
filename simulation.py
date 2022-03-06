from module import PokemonZukan
from module import PokemonWordleQuestioner
from module import PokemonWordleSolver
from module import PokemonWordleGameField

if __name__ == '__main__':
    zukan = PokemonZukan()

    rounds_entropy = []
    for i in range(1000):
        questioner = PokemonWordleQuestioner(zukan=zukan)
        solver = PokemonWordleSolver(zukan=zukan)
        game_field = PokemonWordleGameField(questioner=questioner, solver=solver)
        game_field.run()
        print(i, game_field.round)
        rounds_entropy.append(game_field.round)

    rounds_random = []
    for i in range(1000):
        questioner = PokemonWordleQuestioner(zukan=zukan)
        solver = PokemonWordleSolver(zukan=zukan, policy="random")
        game_field = PokemonWordleGameField(questioner=questioner, solver=solver)
        game_field.run()
        print(i, game_field.round)
        rounds_random.append(game_field.round)

    print("Entropy:", sum(rounds_entropy) / 1000)
    print("Random:", sum(rounds_random) / 1000)
