"""
Script de teste para diagnosticar o problema no submódulo de gravidade
"""
import sys
import io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

import numpy as np
import skfuzzy as fuzz
from skfuzzy import control as ctrl

def testar_gravidade(diagnostico_valor, comorbidades_valor, idade_valor, cirurgia_valor):
    """Testa o submódulo de gravidade com debug detalhado"""

    # Criar variáveis fuzzy EXATAMENTE como no código original
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

    # Calcular graus de pertinência para os valores de entrada
    print("\n" + "="*70)
    print("ANÁLISE DE PERTINÊNCIA DAS ENTRADAS")
    print("="*70)

    print(f"\nDiagnóstico = {diagnostico_valor}:")
    diag_baixo = fuzz.interp_membership(diagnostico.universe, diagnostico['baixo_risco'].mf, diagnostico_valor)
    diag_medio = fuzz.interp_membership(diagnostico.universe, diagnostico['medio_risco'].mf, diagnostico_valor)
    diag_alto = fuzz.interp_membership(diagnostico.universe, diagnostico['alto_risco'].mf, diagnostico_valor)
    print(f"  - Baixo risco: {diag_baixo:.3f}")
    print(f"  - Médio risco: {diag_medio:.3f}")
    print(f"  - Alto risco:  {diag_alto:.3f}")

    print(f"\nComorbidades = {comorbidades_valor}:")
    comorb_baixo = fuzz.interp_membership(comorbidades.universe, comorbidades['baixo_risco'].mf, comorbidades_valor)
    comorb_medio = fuzz.interp_membership(comorbidades.universe, comorbidades['medio_risco'].mf, comorbidades_valor)
    comorb_alto = fuzz.interp_membership(comorbidades.universe, comorbidades['alto_risco'].mf, comorbidades_valor)
    print(f"  - Baixo risco: {comorb_baixo:.3f}")
    print(f"  - Médio risco: {comorb_medio:.3f}")
    print(f"  - Alto risco:  {comorb_alto:.3f}")

    print(f"\nIdade = {idade_valor}:")
    idade_baixo = fuzz.interp_membership(idade_var.universe, idade_var['baixo_risco'].mf, idade_valor)
    idade_medio = fuzz.interp_membership(idade_var.universe, idade_var['medio_risco'].mf, idade_valor)
    idade_alto = fuzz.interp_membership(idade_var.universe, idade_var['alto_risco'].mf, idade_valor)
    print(f"  - Baixo risco: {idade_baixo:.3f}")
    print(f"  - Médio risco: {idade_medio:.3f}")
    print(f"  - Alto risco:  {idade_alto:.3f}")

    print(f"\nCirurgia = {cirurgia_valor}:")
    cirurg_nao = fuzz.interp_membership(cirurgia_var.universe, cirurgia_var['nao'].mf, cirurgia_valor)
    cirurg_sim = fuzz.interp_membership(cirurgia_var.universe, cirurgia_var['sim'].mf, cirurgia_valor)
    print(f"  - Não: {cirurg_nao:.3f}")
    print(f"  - Sim: {cirurg_sim:.3f}")

    # 38 regras originais
    regras = [
        # ALTO RISCO (múltiplos fatores graves)
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

    print("\n" + "="*70)
    print("TESTANDO SISTEMA FUZZY")
    print("="*70)

    try:
        sistema = ctrl.ControlSystem(regras)
        calc = ctrl.ControlSystemSimulation(sistema)

        calc.input['diagnostico'] = diagnostico_valor
        calc.input['comorbidades'] = comorbidades_valor
        calc.input['idade_var'] = idade_valor
        calc.input['cirurgia_var'] = cirurgia_valor

        calc.compute()

        print(f"\n✓ SUCESSO! Risco Gravidade = {calc.output['risco_gravidade']:.2f}")
        return calc.output['risco_gravidade']

    except KeyError as e:
        print(f"\n✗ ERRO KeyError: {e}")
        print("\nCAUSA: Nenhuma regra foi ativada com grau de pertinência suficiente!")
        print("\nCombinação problemática detectada:")
        print(f"  diagnostico={diagnostico_valor}, comorbidades={comorbidades_valor},")
        print(f"  idade={idade_valor}, cirurgia={cirurgia_valor}")
        return None
    except Exception as e:
        print(f"\n✗ ERRO: {type(e).__name__}: {e}")
        return None

# Casos de teste
print("\n" + "="*70)
print("TESTES DO SUBMÓDULO DE GRAVIDADE")
print("="*70)

# Teste 1: Caso comum (deve funcionar)
print("\n### TESTE 1: Caso baixo risco típico")
testar_gravidade(diagnostico_valor=0.0, comorbidades_valor=0.0, idade_valor=50.0, cirurgia_valor=0.0)

# Teste 2: Caso alto risco típico
print("\n### TESTE 2: Caso alto risco típico")
testar_gravidade(diagnostico_valor=3.0, comorbidades_valor=4.0, idade_valor=80.0, cirurgia_valor=1.0)

# Teste 3: Valores intermediários (pode falhar)
print("\n### TESTE 3: Valores intermediários críticos")
testar_gravidade(diagnostico_valor=1.0, comorbidades_valor=1.5, idade_valor=68.0, cirurgia_valor=0.5)

# Teste 4: Zona de transição
print("\n### TESTE 4: Zona de transição entre classes")
testar_gravidade(diagnostico_valor=0.8, comorbidades_valor=1.0, idade_valor=65.0, cirurgia_valor=0.4)

# Teste 5: Outro caso intermediário
print("\n### TESTE 5: Valores baixos mas não zero")
testar_gravidade(diagnostico_valor=0.5, comorbidades_valor=0.5, idade_valor=60.0, cirurgia_valor=0.0)

# Teste 6: Idade média com valores mistos
print("\n### TESTE 6: Idade média com valores mistos")
testar_gravidade(diagnostico_valor=1.5, comorbidades_valor=2.0, idade_valor=70.0, cirurgia_valor=0.0)

print("\n" + "="*70)
print("FIM DOS TESTES")
print("="*70)
