"""
Teste para identificar zonas mortas nas funções de pertinência
"""
import sys
import io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

import numpy as np
import skfuzzy as fuzz
from skfuzzy import control as ctrl

def testar_zona_morta():
    """Testa valores na zona morta de cirurgia"""

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

    print("="*70)
    print("ANÁLISE DE ZONAS MORTAS - VARIÁVEL CIRURGIA")
    print("="*70)

    for cirurgia_val in np.arange(0, 1.1, 0.1):
        cirurg_nao = fuzz.interp_membership(cirurgia_var.universe, cirurgia_var['nao'].mf, cirurgia_val)
        cirurg_sim = fuzz.interp_membership(cirurgia_var.universe, cirurgia_var['sim'].mf, cirurgia_val)
        max_pert = max(cirurg_nao, cirurg_sim)

        status = "OK" if max_pert > 0 else "*** ZONA MORTA ***"
        print(f"Cirurgia={cirurgia_val:.1f}: Não={cirurg_nao:.3f}, Sim={cirurg_sim:.3f} | {status}")

    print("\n" + "="*70)
    print("ANÁLISE DE ZONAS MORTAS - OUTRAS VARIÁVEIS")
    print("="*70)

    # Diagnostico
    print("\nDiagnóstico (0.0 a 3.0):")
    zona_morta_diag = []
    for val in np.arange(0, 3.1, 0.1):
        baixo = fuzz.interp_membership(diagnostico.universe, diagnostico['baixo_risco'].mf, val)
        medio = fuzz.interp_membership(diagnostico.universe, diagnostico['medio_risco'].mf, val)
        alto = fuzz.interp_membership(diagnostico.universe, diagnostico['alto_risco'].mf, val)
        max_pert = max(baixo, medio, alto)
        if max_pert == 0:
            zona_morta_diag.append(val)

    if zona_morta_diag:
        print(f"  ZONAS MORTAS: {zona_morta_diag}")
    else:
        print("  ✓ Sem zonas mortas")

    # Comorbidades
    print("\nComorbidades (0.0 a 5.0):")
    zona_morta_comorb = []
    for val in np.arange(0, 5.1, 0.1):
        baixo = fuzz.interp_membership(comorbidades.universe, comorbidades['baixo_risco'].mf, val)
        medio = fuzz.interp_membership(comorbidades.universe, comorbidades['medio_risco'].mf, val)
        alto = fuzz.interp_membership(comorbidades.universe, comorbidades['alto_risco'].mf, val)
        max_pert = max(baixo, medio, alto)
        if max_pert == 0:
            zona_morta_comorb.append(round(val, 1))

    if zona_morta_comorb:
        print(f"  ZONAS MORTAS: {zona_morta_comorb}")
    else:
        print("  ✓ Sem zonas mortas")

    # Idade
    print("\nIdade (18 a 100):")
    zona_morta_idade = []
    for val in range(18, 101):
        baixo = fuzz.interp_membership(idade_var.universe, idade_var['baixo_risco'].mf, val)
        medio = fuzz.interp_membership(idade_var.universe, idade_var['medio_risco'].mf, val)
        alto = fuzz.interp_membership(idade_var.universe, idade_var['alto_risco'].mf, val)
        max_pert = max(baixo, medio, alto)
        if max_pert == 0:
            zona_morta_idade.append(val)

    if zona_morta_idade:
        print(f"  ZONAS MORTAS: {zona_morta_idade}")
    else:
        print("  ✓ Sem zonas mortas")

    print("\n" + "="*70)
    print("TENTANDO REPRODUZIR O ERRO COM VALORES NA ZONA MORTA")
    print("="*70)

    # Agora vamos testar com valor na zona morta de cirurgia
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

        # REGRAS DE FALLBACK (garantir cobertura 100%)
        ctrl.Rule(diagnostico['baixo_risco'] & comorbidades['baixo_risco'], risco_gravidade['baixo']),
        ctrl.Rule(diagnostico['baixo_risco'] & idade_var['baixo_risco'], risco_gravidade['baixo']),
        ctrl.Rule(comorbidades['baixo_risco'] & idade_var['baixo_risco'] & cirurgia_var['nao'], risco_gravidade['baixo_moderado'])
    ]

    sistema = ctrl.ControlSystem(regras)
    calc = ctrl.ControlSystemSimulation(sistema)

    # TESTE COM VALOR NA ZONA MORTA DE CIRURGIA
    print("\nTeste 1: diagnostico=1.0, comorbidades=1.5, idade=68, cirurgia=0.5 (ZONA MORTA)")
    try:
        calc.input['diagnostico'] = 1.0
        calc.input['comorbidades'] = 1.5
        calc.input['idade_var'] = 68
        calc.input['cirurgia_var'] = 0.5
        calc.compute()
        print(f"  ✓ Resultado: {calc.output['risco_gravidade']:.2f}")
    except KeyError as e:
        print(f"  ✗ KeyError: {e}")
        print("  CAUSA: Nenhuma regra ativada - valor de cirurgia na zona morta!")

    # TESTE COM TODOS OS VALORES NA ZONA MORTA (pior cenário)
    print("\nTeste 2: Tentando encontrar combinação que falha...")

    # Valor na zona morta de cirurgia (0.5) + valores que dependem de cirurgia
    print("  diagnostico=1.0, comorbidades=1.0, idade=66, cirurgia=0.5")
    try:
        calc.input['diagnostico'] = 1.0
        calc.input['comorbidades'] = 1.0
        calc.input['idade_var'] = 66
        calc.input['cirurgia_var'] = 0.5
        calc.compute()
        print(f"  ✓ Resultado: {calc.output['risco_gravidade']:.2f}")
    except KeyError as e:
        print(f"  ✗ KeyError: {e}")
        print("  ESTE É O PROBLEMA!")

if __name__ == "__main__":
    testar_zona_morta()
