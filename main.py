from z3 import *

def resolver_agendamento_cursos(k, m, inscricoes_em_comum):
    # Criar as variáveis booleanas para representar os minicursos nos slots
    slots = [[Bool(f"x_{i}_{j}") for j in range(m)] for i in range(1, k+1)]
    # Restrição: Cada minicurso deve ser ofertado em pelo menos um slot
    restricao_1 = [Or(slots[i-1]) for i in range(1, k+1)]
    # Restrição: Cada minicurso deve ser ofertado em no máximo um slot
    restricao_2 = [Implies(slots[i-1][j], And([Not(slots[i-1][k]) for k in range(m) if k != j])) for i in range(1, k+1) for j in range(m)]
    # Restrição: Minicursos com inscrições em comum não podem ser ofertados no mesmo slot
    restricao_3 = [Or(Not(slots[p-1][j]), Not(slots[q-1][j])) for (p, q) in inscricoes_em_comum for j in range(m)]

    # Criar o solucionador Z3
    s = Solver()

    # Adicionar as restrições ao solucionador
    s.add(restricao_1 + restricao_2 + restricao_3)

    # Verificar a satisfatibilidade
    resultado = s.check()

    if resultado == sat:
        modelo = s.model()
        # Extrair os horários dos minicursos
        horarios = {i: [j+1 for j in range(m) if is_true(modelo[slots[i-1][j]])][0] for i in range(1, k+1)}
        return horarios
    else:
        return None

# Defina aqui as entradas, sendo a variável "k" a quantidade de cursos e a variável "m" o número de slots
# Exemplo de entrada 1
k = 4
m = 3
inscricoes_em_comum = [(1, 2), (2, 3), (2, 4), (3, 4)]


# Exemplo de entrada 2
k1 = 5
m1 = 3
inscricoes_em_comum1 = [(1, 2), (2, 3), (2, 4), (3, 4), (3, 5), (4, 5)]

# Resolver o problema
horarios = resolver_agendamento_cursos(k, m, inscricoes_em_comum)
horarios1 = resolver_agendamento_cursos(k1, m1, inscricoes_em_comum1)

# Exibir a saída
print('Saída 1: ')
if horarios:
    for curso, horario in horarios.items():
        print(f"{curso} s{horario}")
else:
    print("Não é possível agendar os cursos respeitando as inscrições em comum.")
print('----------')
print('Saída 2: ')
if horarios1:
    for curso, horario in horarios1.items():
        print(f"{curso} s{horario}")
else:
    print("Não é possível agendar os cursos respeitando as inscrições em comum..")