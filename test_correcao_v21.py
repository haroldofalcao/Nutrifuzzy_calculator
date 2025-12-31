"""
Teste de validação da correção v2.1 do submódulo de gravidade
"""
import sys
import io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

import numpy as np
import skfuzzy as fuzz
from skfuzzy import control as ctrl

def testar_submodulo_gravidade_v21(diagnostico_valor, comorbidades_valor, idade_valor, cirurgia_valor, descricao=""):
    """Testa o submódulo de gravidade com as correções v2.1"""

    # Definições CORRIGIDAS
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

    # CORREÇÃO CRÍTICA: Zona morta eliminada
    cirurgia_var = ctrl.Antecedent(np.arange(0, 1.1, 0.1), 'cirurgia_var')
    cirurgia_var['nao'] = fuzz.trapmf(cirurgia_var.universe, [0, 0, 0.3, 0.5])   # Estendido
    cirurgia_var['sim'] = fuzz.trapmf(cirurgia_var.universe, [0.5, 0.7, 1, 1])   # Começa em 0.5

    risco_gravidade = ctrl.Consequent(np.arange(0, 101, 1), 'risco_gravidade')
    risco_gravidade['baixo'] = fuzz.trapmf(risco_gravidade.universe, [0, 0, 15, 30])
    risco_gravidade['baixo_moderado'] = fuzz.trimf(risco_gravidade.universe, [20, 32, 45])
    risco_gravidade['moderado'] = fuzz.trimf(risco_gravidade.universe, [35, 50, 65])
    risco_gravidade['moderado_alto'] = fuzz.trimf(risco_gravidade.universe, [55, 67, 80])
    risco_gravidade['alto'] = fuzz.trapmf(risco_gravidade.universe, [70, 85, 100, 100])

    # 47 regras com fallbacks universais
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

        # REGRAS DE FALLBACK UNIVERSAIS (12 regras)
        ctrl.Rule(diagnostico['baixo_risco'] & comorbidades['baixo_risco'], risco_gravidade['baixo']),
        ctrl.Rule(diagnostico['baixo_risco'] & idade_var['baixo_risco'], risco_gravidade['baixo']),
        ctrl.Rule(comorbidades['baixo_risco'] & idade_var['baixo_risco'], risco_gravidade['baixo_moderado']),

        ctrl.Rule(diagnostico['medio_risco'] & comorbidades['medio_risco'], risco_gravidade['moderado']),
        ctrl.Rule(diagnostico['medio_risco'] & idade_var['medio_risco'], risco_gravidade['moderado']),
        ctrl.Rule(comorbidades['medio_risco'] & idade_var['medio_risco'], risco_gravidade['moderado']),

        ctrl.Rule(diagnostico['alto_risco'] & comorbidades['alto_risco'], risco_gravidade['alto']),
        ctrl.Rule(diagnostico['alto_risco'] & idade_var['alto_risco'], risco_gravidade['moderado_alto']),
        ctrl.Rule(comorbidades['alto_risco'] & idade_var['alto_risco'], risco_gravidade['moderado_alto']),

        ctrl.Rule(diagnostico['alto_risco'], risco_gravidade['moderado_alto']),
        ctrl.Rule(comorbidades['alto_risco'], risco_gravidade['moderado']),
        ctrl.Rule(idade_var['alto_risco'], risco_gravidade['baixo_moderado'])
    ]

    print(f"\n{'='*80}")
    print(f"TESTE v2.1: {descricao}")
    print(f"Valores: diag={diagnostico_valor}, comorb={comorbidades_valor}, idade={idade_valor}, cirurg={cirurgia_valor}")
    print(f"{'='*80}")

    try:
        sistema = ctrl.ControlSystem(regras)
        calc = ctrl.ControlSystemSimulation(sistema)

        calc.input['diagnostico'] = diagnostico_valor
        calc.input['comorbidades'] = comorbidades_valor
        calc.input['idade_var'] = idade_valor
        calc.input['cirurgia_var'] = cirurgia_valor

        calc.compute()

        print(f"✓ SUCESSO! Risco Gravidade = {calc.output['risco_gravidade']:.2f}")
        return True, calc.output['risco_gravidade']

    except KeyError as e:
        print(f"✗ FALHOU! KeyError: {e}")
        return False, None
    except Exception as e:
        print(f"✗ ERRO: {type(e).__name__}: {e}")
        return False, None

# BATERIA DE TESTES
print("="*80)
print("VALIDAÇÃO DA CORREÇÃO v2.1 - SUBMÓDULO DE GRAVIDADE")
print("="*80)
print("\nTotal de regras: 47 (35 originais + 12 fallbacks universais)")
print("Correção: Zona morta em cirurgia eliminada (0.4-0.6)")
print("="*80)

testes = [
    # Casos que falhavam antes
    (0.9, 1.2, 66, 0.5, "Zona morta cirurgia + transições médias"),
    (0.85, 1.05, 66, 0.45, "Múltiplas transições críticas"),
    (1.0, 1.5, 68, 0.5, "Todos em médio + zona morta cirurgia"),

    # Casos extremos
    (0.0, 0.0, 50, 0.0, "Tudo em baixo risco"),
    (3.0, 4.0, 80, 1.0, "Tudo em alto risco"),
    (1.5, 2.0, 70, 0.0, "Tudo em médio risco"),

    # Zonas de transição
    (0.8, 1.0, 65, 0.4, "Bordas superiores de baixo"),
    (0.5, 0.5, 60, 0.5, "Limites inferiores"),
    (2.3, 3.5, 78, 0.3, "Limites entre médio e alto"),

    # Valores na antiga zona morta de cirurgia
    (1.0, 1.0, 65, 0.4, "Cirurgia 0.4 (antiga zona morta)"),
    (1.0, 1.0, 65, 0.45, "Cirurgia 0.45 (antiga zona morta)"),
    (1.0, 1.0, 65, 0.5, "Cirurgia 0.5 (exato no overlap)"),
    (1.0, 1.0, 65, 0.55, "Cirurgia 0.55 (antiga zona morta)"),
    (1.0, 1.0, 65, 0.6, "Cirurgia 0.6 (antiga zona morta)"),
]

sucessos = 0
falhas = 0

for diag, comorb, idade, cirurg, desc in testes:
    sucesso, resultado = testar_submodulo_gravidade_v21(diag, comorb, idade, cirurg, desc)
    if sucesso:
        sucessos += 1
    else:
        falhas += 1

print("\n" + "="*80)
print("RESUMO DOS TESTES")
print("="*80)
print(f"Total de testes: {len(testes)}")
print(f"✓ Sucessos: {sucessos}")
print(f"✗ Falhas: {falhas}")

if falhas == 0:
    print("\n🎉 PARABÉNS! Todos os testes passaram!")
    print("A correção v2.1 eliminou completamente o problema de KeyError!")
else:
    print(f"\n⚠️ ATENÇÃO: {falhas} teste(s) falharam. Revisar implementação.")

print("="*80)
