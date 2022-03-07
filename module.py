import random
import math

def iter_p_adic(p, n):
    '''
    連続して増加するp進数をリストとして返す。nはリストの長さ
    return
    ----------
    所望のp進数リストを次々返してくれるiterator
    '''
    from itertools import product
    tmp = [range(p)] * n
    return product(*tmp)

class PokemonZukan:
    def __init__(self, zukan_file_path="zukan.txt"):
        self.zukan = []
        with open(zukan_file_path) as f:
            l = f.readlines()
            for e in l:
                e = e.replace("\n", "")
                if len(e) != 5: continue
                self.zukan.append(e)
            print(len(self.zukan))

    def copy(self):
        return self.zukan.copy()

    def get_pokemon_at_random(self):
        return random.choice(self.zukan)

    def __len__(self):
        return len(self.zukan)


class PokemonWordleSolver:
    def __init__(self, zukan: PokemonZukan, policy="random"):
        self.zukan = zukan
        self.candidate_list = zukan.copy()
        self.policy = policy

    def filter_for_simulation(self, answer_pokemon, result_signals, candidate_list):
        for i in range(5):
            signal = int(result_signals[i])
            zukan_tmp = []
            if signal == 0:
                # 文字を含んでいないものだけ入れたい
                for pokemon in candidate_list:
                    if answer_pokemon[i] in pokemon: continue
                    zukan_tmp.append(pokemon)

            elif signal == 1:
                # 文字を含んでいたら入れる
                for pokemon in candidate_list:
                    if answer_pokemon[i] == pokemon[i]: continue
                    for j in range(5):
                        if answer_pokemon[i] == pokemon[j]:
                            zukan_tmp.append(pokemon)
                            break

            elif signal == 2:
                # 文字が一致していたら入れる
                for pokemon in candidate_list:
                    if answer_pokemon[i] == pokemon[i]:
                        zukan_tmp.append(pokemon)
    
            candidate_list = zukan_tmp.copy()
        return candidate_list

    def filter(self, answer_pokemon, result_signals):
        self.candidate_list = self.filter_for_simulation(answer_pokemon, 
                result_signals, self.candidate_list)

    def get_entropy(self, pokemon, candidate_list):
        iterator = iter_p_adic(3, 5)
        entropy = 0
        for result_signals_list in iterator:
            result_signals = ""
            for i in result_signals_list:
                result_signals += str(i)

            can = self.filter_for_simulation(pokemon, result_signals, candidate_list)
            if len(can) == 0: continue

            p = len(can) / len(candidate_list)
            entropy +=  - p * math.log(p)

        return entropy
        
    def get_candidate(self):
        if self.policy == "entropy-rentora":
            if len(self.candidate_list) == len(self.zukan):
                candidate = "レントラー"
            else:
                entropy_list = []
                for pokemon in self.candidate_list:
                    entropy = self.get_entropy(pokemon, self.candidate_list)
                    entropy_list.append((pokemon, entropy))

                entropy_list_sorted = sorted(entropy_list, key=lambda e: -e[1])
                candidate = entropy_list_sorted[0][0]
        elif self.policy == "entropy-jiransu":
            if len(self.candidate_list) == len(self.zukan):
                candidate = "ジーランス"
            else:
                entropy_list = []
                for pokemon in self.candidate_list:
                    entropy = self.get_entropy(pokemon, self.candidate_list)
                    entropy_list.append((pokemon, entropy))

                entropy_list_sorted = sorted(entropy_list, key=lambda e: -e[1])
                candidate = entropy_list_sorted[0][0]
        else: 
            candidate = random.choice(self.candidate_list)

        return candidate

    def get_count_candidate(self):
        return len(self.candidate_list)


class PokemonWordleQuestioner:
    def __init__(self, zukan: PokemonZukan):
        self.zukan = zukan
        self.target = zukan.get_pokemon_at_random()

    def judge(self, answer_pokemon):
        result = ""
        for i in range(5):
            if answer_pokemon[i] == self.target[i]:
                result += "2"
            elif answer_pokemon[i] in self.target:
                result += "1"
            else:
                result += "0"
        return result 


class PokemonWordleGameField:
    def __init__(self, questioner, solver):
        self.questioner = questioner
        self.solver = solver
        self.round = 1

    def run(self):
        if self.solver is None:
            self.run_manual()
        else:
            self.run_auto()

    def run_manual(self):
        print("ゲームスタート")
        while True:
            print("Round: ", self.round)
            
            answer_pokemon = input()
            print("回答入力", answer_pokemon)
            if len(answer_pokemon) != 5: 
                print("お題エラー")
                continue

            result_signals = self.questioner.judge(answer_pokemon=answer_pokemon)
            print("結果（2: eat, 1: bite, 0: or not）", result_signals)
            if result_signals == "22222":
                print("ゲームクリア!!! お題:", self.questioner.target)
                print("かかったラウンド:", self.round)
                break
            elif self.round == 5:
                print("ゲームオーバー!!! お題:", self.questioner.target)
                break
            
            self.round += 1
    
    def run_auto(self):
        while True:
            candidate = self.solver.get_candidate()
            count_candidate = self.solver.get_count_candidate()
            answer_pokemon = candidate
            result_signals = self.questioner.judge(answer_pokemon=answer_pokemon)
            if result_signals == "22222":
                break

            self.solver.filter(answer_pokemon, result_signals)
            self.round += 1
