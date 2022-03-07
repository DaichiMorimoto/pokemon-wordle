from module import PokemonZukan
from module import PokemonWordleQuestioner
from module import PokemonWordleSolver
from module import PokemonWordleGameField
from tqdm import tqdm

if __name__ == '__main__':
    zukan = PokemonZukan()
    N = 10000

    rounds_entropy_rentora = []
    for i in tqdm(range(N)):
        questioner = PokemonWordleQuestioner(zukan=zukan)
        solver = PokemonWordleSolver(zukan=zukan, policy="entropy-rentora")
        game_field = PokemonWordleGameField(questioner=questioner, solver=solver)
        game_field.run()
        rounds_entropy_rentora.append(game_field.round)
    
    rounds_entropy_jiransu = []
    for i in tqdm(range(N)):
        questioner = PokemonWordleQuestioner(zukan=zukan)
        solver = PokemonWordleSolver(zukan=zukan, policy="entropy-jiransu")
        game_field = PokemonWordleGameField(questioner=questioner, solver=solver)
        game_field.run()
        rounds_entropy_jiransu.append(game_field.round)

    rounds_random = []
    for i in tqdm(range(N)):
        questioner = PokemonWordleQuestioner(zukan=zukan)
        solver = PokemonWordleSolver(zukan=zukan, policy="random")
        game_field = PokemonWordleGameField(questioner=questioner, solver=solver)
        game_field.run()
        rounds_random.append(game_field.round)

    print("Entropy レントラー:", sum(rounds_entropy_rentora) / N)
    print("Entropy ジーランス:", sum(rounds_entropy_jiransu) / N)
    print("Random:", sum(rounds_random) / N)
