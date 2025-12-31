"""
Teste para encontrar o caso exato que causa KeyError
"""
import sys
import io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

import numpy as np
import skfuzzy as fuzz
from skfuzzy import control as ctrl

def testar_caso(diagnostico_valor, comorbidades_valor, idade_valor, cirurgia_valor, descricao=""):
    """Testa um caso específico"""

    diagnostico = ctrl.Antecedent(np.arange(0, 3.1, 0.1), 'diagnostico')
    diagnostico['baixo_risco'] = fuzz.trapmf(diagnostico.universe, [0, 0, 0.3, 0.8])
    diagnostico['medio_risco'] = fuzz.trimf(diagnostico.universe, [0.5, 1.5, 2.3])
    diagnostico['alto_risco'] = fuzz.trapmf(diagnostico.universe, [2, 2.5, 3, 3])

    comorbidades = ctrl.Antecedent(np.arange(0, 5.1, 0.1), 'comorbidades')
    comorbidades['baixo_risco'] = fuzz.trapmf(comorbidades.universe, [0, 0, 0.3, 1.0])
    comorbidades['medio_risco'] = fuzz.trimf(comorbidades.universe, [0.5, 2.0, 3.5])
    comorbidades['alto_risco'] = fuzz.trapmf(comorbidades.universe, [3, 3.5, 5, 5])

    idade_var = ctrl.Antecedent(np.arange(18, 101, 1), 'idade_var')
    idade_var['baixo_risco'] = fuzz.trapmf(idade_var.universe, [18, 18, 55, 65])
    idade_var['medio_risco'] = fuzz.trimf(idade_var.universe, [60, 70, 78])
    idade_var['alto_risco'] = fuzz.trapmf(idade_var.universe, [73, 75, 100, 100])

    cirurgia_var = ctrl.Antecedent(np.arange(0, 1.1, 0.1), 'cirurgia_var')
    cirurgia_var['nao'] = fuzz.trapmf(cirurgia_var.universe, [0, 0, 0.2, 0.4])
    cirurgia_var['sim'] = fuzz.trapmf(cirurgia_var.universe, [0.6, 0.8, 1, 1])

    risco_gravidade = ctrl.Consequent(np.arange(0, 101, 1), 'risco_gravidade')
    risco_gravidade['baixo'] = fuzz.trapmf(risco_gravidade.universe, [0, 0, 15, 30])
    risco_gravidade['baixo_moderado'] = fuzz.trimf(risco_gravidade.universe, [20, 32, 45])
    risco_gravidade['moderado'] = fuzz.trimf(risco_gravidade.universe, [35, 50, 65])
    risco_gravidade['moderado_alto'] = fuzz.trimf(risco_gravidade.universe, [55, 67, 80])
    risco_gravidade['alto'] = fuzz.trapmf(risco_gravidade.universe, [70, 85, 100, 100])

    # Calcular pertinências
    diag_baixo = fuzz.interp_membership(diagnostico.universe, diagnostico['baixo_risco'].mf, diagnostico_valor)
    diag_medio = fuzz.interp_membership(diagnostico.universe, diagnostico['medio_risco'].mf, diagnostico_valor)
    diag_alto = fuzz.interp_membership(diagnostico.universe, diagnostico['alto_risco'].mf, diagnostico_valor)

    comorb_baixo = fuzz.interp_membership(comorbidades.universe, comorbidades['baixo_risco'].mf, comorbidades_valor)
    comorb_medio = fuzz.interp_membership(comorbidades.universe, comorbidades['medio_risco'].mf, comorbidades_valor)
    comorb_alto = fuzz.interp_membership(comorbidades.universe, comorbidades['alto_risco'].mf, comorbidades_valor)

    idade_baixo = fuzz.interp_membership(idade_var.universe, idade_var['baixo_risco'].mf, idade_valor)
    idade_medio = fuzz.interp_membership(idade_var.universe, idade_var['medio_risco'].mf, idade_valor)
    idade_alto = fuzz.interp_membership(idade_var.universe, idade_var['alto_risco'].mf, idade_valor)

    cirurg_nao = fuzz.interp_membership(cirurgia_var.universe, cirurgia_var['nao'].mf, cirurgia_valor)
    cirurg_sim = fuzz.interp_membership(cirurgia_var.universe, cirurgia_var['sim'].mf, cirurgia_valor)

    print("\n" + "="*80)
    print(f"TESTE: {descricao}")
    print(f"Valores: diag={diagnostico_valor}, comorb={comorbidades_valor}, idade={idade_valor}, cirurg={cirurgia_valor}")
    print("="*80)

    print(f"Diagnóstico:   Baixo={diag_baixo:.3f}, Médio={diag_medio:.3f}, Alto={diag_alto:.3f}")
    print(f"Comorbidades:  Baixo={comorb_baixo:.3f}, Médio={comorb_medio:.3f}, Alto={comorb_alto:.3f}")
    print(f"Idade:         Baixo={idade_baixo:.3f}, Médio={idade_medio:.3f}, Alto={idade_alto:.3f}")
    print(f"Cirurgia:      Não={cirurg_nao:.3f}, Sim={cirurg_sim:.3f}")

    # Analisar quais regras podem ser ativadas (apenas as mais importantes)
    print("\nREGRAS DE FALLBACK que PODEM ser ativadas:")

    # Regra: diagnostico['baixo_risco'] & comorbidades['baixo_risco']
    ativacao1 = min(diag_baixo, comorb_baixo)
    print(f"  1. diag_baixo AND comorb_baixo → {ativacao1:.3f}")

    # Regra: diagnostico['baixo_risco'] & idade_var['baixo_risco']
    ativacao2 = min(diag_baixo, idade_baixo)
    print(f"  2. diag_baixo AND idade_baixo → {ativacao2:.3f}")

    # Regra: comorbidades['baixo_risco'] & idade_var['baixo_risco'] & cirurgia_var['nao']
    ativacao3 = min(comorb_baixo, idade_baixo, cirurg_nao)
    print(f"  3. comorb_baixo AND idade_baixo AND cirurg_nao → {ativacao3:.3f}")

    max_ativacao = max(ativacao1, ativacao2, ativacao3)
    print(f"\nMáxima ativação das regras de fallback: {max_ativacao:.3f}")

    if max_ativacao == 0:
        print("*** PROBLEMA: Nenhuma regra de fallback será ativada! ***")

    # Testar com o sistema
    regras = [
        # ALTO RISCO
        ctrl.Rule(diagnostico['alto_risco'] & comorbidades['alto_risco'] & idade_var['alto_risco'], risco_gravidade['alto']),
        ctrl.Rule(diagnostico['alto_risco'] & comorbidades['alto_risco'] & cirurgia_var['sim'], risco_gravidade['alto']),
        ctrl.Rule(diagnostico['alto_risco'] & idade_var['alto_risco'] & cirurgia_var['sim'], risco_gravidade['alto']),
        ctrl.Rule(diagnostico['alto_risco'] & comorbidades['alto_risco'] & idade_var['medio_risco'], risco_gravidade['alto']),
        ctrl.Rule(comorbidades['alto_risco'] & idade_var['alto_risco'] & cirurgia_var['sim'], risco_gravidade['alto']),

        # MODERADO-ALTO RISCO
        ctrl.Rule(diagnostico['alto_risco'] & comorbidades['medio_risco'] & idade_var['medio_risco'], risco_gravidade['moderado_alto']),
        ctrl.Rule(diagnostico['medio_risco'] & comorbidades['alto_risco'] & cirurgia_var['sim'], risco_gravidade['moderado_alto']),
        ctrl.Rule(diagnostico['alto_risco'] & comorbidades['baixo_risco'] & cirurgia_var['sim'], risco_gravidade['moderado_alto']),
        ctrl.Rule(diagnostico['alto_risco'] & comorbidades['medio_risco'] & idade_var['alto_risco'], risco_gravidade['moderado_alto']),
        ctrl.Rule(diagnostico['medio_risco'] & comorbidades['alto_risco'] & idade_var['alto_risco'], risco_gravidade['moderado_alto']),
        ctrl.Rule(diagnostico['alto_risco'] & idade_var['alto_risco'] & cirurgia_var['nao'], risco_gravidade['moderado_alto']),
        ctrl.Rule(diagnostico['alto_risco'] & comorbidades['alto_risco'] & idade_var['baixo_risco'], risco_gravidade['moderado_alto']),
        ctrl.Rule(diagnostico['medio_risco'] & comorbidades['medio_risco'] & idade_var['alto_risco'] & cirurgia_var['sim'], risco_gravidade['moderado_alto']),

        # MODERADO RISCO
        ctrl.Rule(comorbidades['alto_risco'] & cirurgia_var['nao'], risco_gravidade['moderado']),
        ctrl.Rule(diagnostico['medio_risco'] & comorbidades['medio_risco'] & idade_var['medio_risco'], risco_gravidade['moderado']),
        ctrl.Rule(diagnostico['alto_risco'] & comorbidades['baixo_risco'] & idade_var['baixo_risco'] & cirurgia_var['nao'], risco_gravidade['moderado']),
        ctrl.Rule(idade_var['alto_risco'] & cirurgia_var['sim'], risco_gravidade['moderado']),
        ctrl.Rule(diagnostico['alto_risco'] & comorbidades['baixo_risco'] & idade_var['medio_risco'], risco_gravidade['moderado']),
        ctrl.Rule(diagnostico['medio_risco'] & comorbidades['alto_risco'] & idade_var['baixo_risco'], risco_gravidade['moderado']),
        ctrl.Rule(diagnostico['alto_risco'] & comorbidades['medio_risco'] & idade_var['baixo_risco'], risco_gravidade['moderado']),
        ctrl.Rule(diagnostico['medio_risco'] & comorbidades['medio_risco'] & cirurgia_var['sim'], risco_gravidade['moderado']),
        ctrl.Rule(diagnostico['alto_risco'] & idade_var['medio_risco'] & cirurgia_var['nao'], risco_gravidade['moderado']),
        ctrl.Rule(diagnostico['medio_risco'] & comorbidades['alto_risco'] & cirurgia_var['nao'], risco_gravidade['moderado']),

        # BAIXO-MODERADO RISCO
        ctrl.Rule(diagnostico['medio_risco'] & comorbidades['baixo_risco'] & idade_var['medio_risco'], risco_gravidade['baixo_moderado']),
        ctrl.Rule(diagnostico['baixo_risco'] & comorbidades['medio_risco'] & idade_var['medio_risco'], risco_gravidade['baixo_moderado']),
        ctrl.Rule(diagnostico['medio_risco'] & comorbidades['medio_risco'] & idade_var['baixo_risco'], risco_gravidade['baixo_moderado']),
        ctrl.Rule(diagnostico['baixo_risco'] & comorbidades['alto_risco'] & idade_var['baixo_risco'], risco_gravidade['baixo_moderado']),
        ctrl.Rule(diagnostico['baixo_risco'] & comorbidades['baixo_risco'] & idade_var['alto_risco'], risco_gravidade['baixo_moderado']),
        ctrl.Rule(diagnostico['medio_risco'] & idade_var['alto_risco'] & cirurgia_var['nao'], risco_gravidade['baixo_moderado']),
        ctrl.Rule(diagnostico['baixo_risco'] & comorbidades['medio_risco'] & cirurgia_var['sim'], risco_gravidade['baixo_moderado']),
        ctrl.Rule(comorbidades['medio_risco'] & idade_var['medio_risco'] & cirurgia_var['nao'], risco_gravidade['baixo_moderado']),

        # BAIXO RISCO
        ctrl.Rule(diagnostico['baixo_risco'] & comorbidades['baixo_risco'] & idade_var['baixo_risco'] & cirurgia_var['nao'], risco_gravidade['baixo']),
        ctrl.Rule(diagnostico['baixo_risco'] & comorbidades['baixo_risco'] & idade_var['medio_risco'] & cirurgia_var['nao'], risco_gravidade['baixo']),
        ctrl.Rule(diagnostico['medio_risco'] & comorbidades['baixo_risco'] & idade_var['baixo_risco'] & cirurgia_var['nao'], risco_gravidade['baixo']),
        ctrl.Rule(diagnostico['baixo_risco'] & comorbidades['baixo_risco'] & idade_var['baixo_risco'] & cirurgia_var['sim'], risco_gravidade['baixo']),

        # REGRAS DE FALLBACK
        ctrl.Rule(diagnostico['baixo_risco'] & comorbidades['baixo_risco'], risco_gravidade['baixo']),
        ctrl.Rule(diagnostico['baixo_risco'] & idade_var['baixo_risco'], risco_gravidade['baixo']),
        ctrl.Rule(comorbidades['baixo_risco'] & idade_var['baixo_risco'] & cirurgia_var['nao'], risco_gravidade['baixo_moderado'])
    ]

    try:
        sistema = ctrl.ControlSystem(regras)
        calc = ctrl.ControlSystemSimulation(sistema)

        calc.input['diagnostico'] = diagnostico_valor
        calc.input['comorbidades'] = comorbidades_valor
        calc.input['idade_var'] = idade_valor
        calc.input['cirurgia_var'] = cirurgia_valor

        calc.compute()
        print(f"\n✓ SUCESSO! Risco Gravidade = {calc.output['risco_gravidade']:.2f}")
        return True

    except KeyError as e:
        print(f"\n✗✗✗ ERRO KeyError: {e}")
        print("CAUSA RAIZ: Nenhuma regra foi ativada com grau de pertinência suficiente!")
        return False
    except Exception as e:
        print(f"\n✗ ERRO: {type(e).__name__}: {e}")
        return False

# TESTES SISTEMÁTICOS PARA ENCONTRAR O CASO QUE FALHA

print("="*80)
print("PROCURANDO CASO QUE CAUSA KeyError NO SUBMÓDULO DE GRAVIDADE")
print("="*80)

# Caso 1: Tudo na transição entre baixo e médio + cirurgia na zona morta
testar_caso(0.9, 1.2, 66, 0.5, "Transições + zona morta cirurgia")

# Caso 2: Valores nas bordas superiores de "baixo" mas sem ser "médio"
testar_caso(0.85, 1.05, 66, 0.45, "Bordas superiores baixo + cirurgia zona morta")

# Caso 3: Idade 66 está exatamente entre baixo (65) e médio (60-78)
testar_caso(0.9, 1.1, 66, 0.5, "Idade 66 na transição")

# Caso 4: Todas as transições em valores críticos
testar_caso(0.85, 1.05, 66, 0.45, "Múltiplas transições críticas")

# Caso 5: Vamos tentar idades específicas próximas a 65
for idade in [65, 66, 67, 68]:
    testar_caso(0.85, 1.0, idade, 0.5, f"Idade={idade}")

print("\n" + "="*80)
print("FIM DOS TESTES")
print("="*80)
