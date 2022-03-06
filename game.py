from module import PokemonZukan
from module import PokemonWordleQuestioner
from module import PokemonWordleGameField

if __name__ == '__main__':
    zukan = PokemonZukan()
    questioner = PokemonWordleQuestioner(zukan=zukan)
    game_field = PokemonWordleGameField(questioner=questioner, solver=None)
    game_field.run()
