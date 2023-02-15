import connection as cn
import os

port = 2037
s = cn.connect(port)

action_names = {0: "left", 1: "right", 2: "jump"}


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

    string_table = '\n'.join(str(row) for row in table)
    print(f"Tabela inicial = {string_table}")
    return table


def write_table(q_table: list):
    """Escreve a q_table atualizada no arquivo de resultado"""
    os.remove('temp.txt')
    with open('./temp.txt', 'w') as new_t:
        for line in q_table:
            row = ' '.join(f'{l:.6f}' for l in line) + '\n'
            new_t.write(row)

            
def do_action(q_table:list, state: str, lrate: float, dfactor: float) -> tuple[str, int, int]:
    """Obtém o estado atual em sua forma binária e retorna o novo estado, a ação executada e sua recompensa"""
    state_row = q_table[int(state, 2)] # localiza estado na q table

    #1 =============================== Escolher uma ação e executá-la
    action = [
        m[0]
        for m in enumerate(state_row)
        if m[1] == max(state_row)
    ][-1] # escolhe a última ação dentre as máximas (para priorizar o pulo)

    action_name = action_names[action] # converte a ação para string
    print(f"Estado: {int(state, 2)}, Ação: {action_name}")

    #2 =============================== Observar o novo estado
    new_state, reward = cn.get_state_reward(s, action_name) # recebe novo estado
    new_state_row = q_table[int(new_state, 2)] # localiza o novo estado na q table

    #3 =============================== Aplicar a recompensa recebida
    state_row[action] += lrate * (reward + dfactor * max(new_state_row) - state_row[action])
    return new_state, action, reward


def generate_policy(q_table: list, lrate: float, dfactor: float, n_times: int, initial_state: str = '0000000'):
    """Executa o loop de avançar entre estados n vezes"""

    state, _, _ = do_action(q_table, initial_state, lrate, dfactor) # Executa a primeira ação

    # Loop é executado n_vezes
    for i in range(n_times):
        print(f"Passo {i + 1}:")
        state, _, _ = do_action(q_table, state, lrate, dfactor)


def explore(q_table:list, lr: float, df: float, n_times: int):
    """Explora o ambiente e atualiza a q_table"""
    generate_policy(q_table, lr, df, n_times)
    write_table(q_table)


def apply_policy(q_table: list):
    pass
        

if __name__ == "__main__":
    q_table = read_table() # lê a q_table do arquivo resultado

    mode = int(input("Digite 1 para explorar o ambiente, 0 para executar a política: "))

    if mode:
        learning_rate = float(input("Digite a taxa de aprendizagem: "))
        discount_factor = float(input("Digite o fator de desconto: "))
        n_times = int(input("Digite a quantidade de passos: "))

        explore(q_table, learning_rate, discount_factor, n_times)
    else:
        apply_policy(q_table)