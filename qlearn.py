import connection as cn

port = 2037
s = cn.connect(port)

action_names = {0: "left", 1: "right", 2: "jump"}
q_table = [[0, 0, 0] * 96] # inicia com 96 estados nulos
estados_finais = [] # verifica o fim de uma iteração

def do_action(state: str, lrate: float, dfactor: float) -> tuple[str, int, int]:
    """Obtém o estado atual em sua forma binária e retorna o novo estado, a ação executada e sua recompensa"""
    state_row = q_table[int(state, 2)] # localiza estado na q table

    #1 =============================== Escolher uma ação e executá-la
    action = [
        m[0]
        for m in enumerate(state_row)
        if m[1] == max(state_row)
    ][0] # escolhe a primeira ação dentre as máximas

    action_name = action_names[action] # converte a ação para string
    print(f"Estado: {int(state, 2)}, Ação: {action_name}")

    #2 =============================== Observar o novo estado
    new_state, reward = cn.get_state_reward(s, action_name) # recebe novo estado
    new_state_row = q_table[int(new_state, 2)] # localiza o novo estado na q table

    #3 =============================== Aplicar a recompensa recebida
    state_row[action] += lrate * (reward + dfactor * max(new_state_row) - state_row[action])
    return new_state, action, reward


def generate_policy(lrate: float, dfactor: float, initial_state: str = '0000000'):
    """Executa o loop de avançar entre estados até que um estado final seja alcançado"""

    state, _, _ = do_action(initial_state, lrate, dfactor) # Executa a primeira ação
    state_block = int(state[:5], 2) # identifica o bloco alcançado

    # Loop é executado enquanto não alcança um estado final
    while state_block not in estados_finais:
        state, _, _ = do_action(state, lrate, dfactor)
        

if __name__ == "__main__":
    learning_rate = 0.1
    discount_factor = 0.25
    n_times = 100

    for _ in range(n_times):
        generate_policy(learning_rate, discount_factor)
