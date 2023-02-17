import connection as cn
import os
from random import randint, random as rand

port = 2037
s = cn.connect(port)

action_names = {0: "left", 1: "right", 2: "jump"}
dir_names = {0: "norte", 1: "leste", 2: "sul", 3: "oeste"}


def read_table() -> list:
    """Lê o arquivo da q_table"""
    table = []
    with open('./resultado.txt') as t:
        for line in t:
            row = line.strip().split() # separa cada ação na linha
            # converte os valores lidos para float
            for i in range(len(row)):
                row[i] = float(row[i])
            
            table.append(row) # inclui na tabela local

    string_table = '\n'.join(f"{row[0]:.6f} {row[1]:.6f} {row[2]:.6f}" for row in table)
    print(f"Tabela inicial =\n{string_table}")
    return table


def write_table(q_table: list):
    """Escreve a q_table atualizada no arquivo de resultado"""
    os.remove('./resultado.txt')
    with open('./resultado.txt', 'w') as new_t:
        for line in q_table:
            row = ' '.join(f'{l}' for l in line) + '\n'
            new_t.write(row)

            
def do_action(q_table:list, state: str, randomness: float) -> tuple:
    """Obtém o estado atual e retorna ele mesmo, a ação executada, o novo estado e a recompensa"""
    state_row = q_table[int(state, 2)] # localiza estado na q table
    r = rand() # gera valor aleatorio

    #1 =============================== Escolher uma ação e executá-la
    if r <= randomness:
        action = randint(0, len(state_row) - 1) # escolhe uma ação aleatória
    else:
        action = [
            m[0]
            for m in enumerate(state_row)
            if m[1] == max(state_row)
        ][-1] # escolhe a melhor ação

    action_name = action_names[action] # converte a ação para string
    print('{' + f"Estado: {int(state, 2)} ({int(state[-7:-2], 2)} - {dir_names[int(state[-2:], 2)]}), Ação: {action_name}", end='')

    #2 =============================== Observar o novo estado
    new_state, reward = cn.get_state_reward(s, action_name) # recebe novo estado
    return state_row, action, new_state, reward


def update_table(state_row: list, action: int, new_state: str, reward: float, lrate: float, dfactor: float):
    """Aplica a recompensa na q_table"""
    new_state_row = q_table[int(new_state, 2)] # localiza o novo estado na q table

    #3 =============================== Aplicar a recompensa recebida
    state_row[action] += lrate * (reward + dfactor * max(new_state_row) - state_row[action])
    print(f", Recompensa: {reward}" + '}')


def do_and_update(q_table: list, state: str, lrate: float, dfactor: float, randomness: float):
    """Executa a ação, atualiza a q_table e retorna o novo estado e a recompensa"""
    state_row, action, new_state, reward = do_action(q_table, state, randomness)
    update_table(state_row, action, new_state, reward, lrate, dfactor)
    return new_state, reward


def generate_policy(q_table: list, lrate: float, dfactor: float, randomness: float, n_times: int, initial_state: str = '0000000', step_limit: int = 999):
    """Percorre o ambiente até um estado final n vezes"""
    for i in range(n_times):
        print(f"\nIteração {i + 1}:")

        state, reward = do_and_update(q_table, initial_state, lrate, dfactor, randomness) # executa a primeira ação
        counter = 0
        while reward != 300 and counter <= step_limit: # explora até chegar num estado terminal
            counter += 1
            print(f"Passo {counter}:", end=' ')
            state, reward = do_and_update(q_table, state, lrate, dfactor, randomness)


def explore(q_table:list, lr: float, df: float, rd: float, n_times: int, initial_state: str = '0000000'):
    """Explora o ambiente e atualiza o arquivo da q_table"""
    generate_policy(q_table, lr, df, rd, n_times, initial_state)
    write_table(q_table)


def apply_policy(q_table: list, n_times: int, initial_state: str = '0000000'):
    for i in range(n_times):
        print(f"\nIteração {i + 1}:")

        _, _, state, reward = do_action(q_table, initial_state, 0)
        counter = 0
        while reward != 300:
            counter += 1
            print('}\n' + f"Passo {counter}:", end=' ')
            _, _, state, reward = do_action(q_table, state, 0)
        print('}\n')
        

if __name__ == "__main__":
    q_table = read_table() # lê a q_table do arquivo resultado

    mode = int(input("Digite 1 para explorar o ambiente, 0 para executar a política: "))

    initial_state = '00000' + '00'
    n_times = int(input("Digite a quantidade de iterações: "))
    
    if mode:
        learning_rate = float(input("Digite a taxa de aprendizagem: "))
        discount_factor = float(input("Digite o fator de desconto: "))
        randomness = float(input("Digite a frequencia de ações aleatórias: "))

        explore(q_table, learning_rate, discount_factor, randomness, n_times, initial_state)
    else:
        apply_policy(q_table, n_times, initial_state)