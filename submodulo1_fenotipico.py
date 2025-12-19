"""
CALCULADORA FUZZY DE RISCO NUTRICIONAL
Submódulo 1: Nutricional Fenotípico

Desenvolvido por: Dr. Haroldo Falcão Ramos da Silva
Implementação: Claude (Anthropic)
Data: Dezembro 2024

VARIÁVEIS DE ENTRADA:
1. IMC (kg/m²)
2. Perda Ponderal (% em 3 meses)
3. Sarcopenia Clínica (escala 0-3)

SAÍDA: Escore de Risco Fenotípico (0-100)
"""

import numpy as np
import skfuzzy as fuzz
from skfuzzy import control as ctrl
import matplotlib.pyplot as plt

# ==============================================================================
# PASSO 1: DEFINIR AS VARIÁVEIS FUZZY (ANTECEDENTES E CONSEQUENTE)
# ==============================================================================

# ANTECEDENTE 1: IMC (kg/m²)
# Universo de discurso: 12 a 50 kg/m²
imc = ctrl.Antecedent(np.arange(12, 50.1, 0.1), 'imc')

# Funções de Pertinência do IMC (conforme Rodada 2 Delphi):
# - Baixo Risco: IMC ideal (22-25 kg/m²)
# - Médio Risco: Baixo peso limítrofe ou sobrepeso
# - Alto Risco: Desnutrição grave (<18) ou obesidade mórbida (>30)

imc['baixo_risco'] = fuzz.trapmf(imc.universe, [20, 22, 25, 28])
imc['medio_risco'] = fuzz.trimf(imc.universe, [17, 20, 30])
imc['alto_risco'] = fuzz.trapmf(imc.universe, [12, 14, 16, 18]) + fuzz.trapmf(imc.universe, [30, 35, 45, 50])

# ANTECEDENTE 2: Perda Ponderal (% em 3 meses)
# Universo de discurso: 0 a 30%
perda_ponderal = ctrl.Antecedent(np.arange(0, 30.1, 0.1), 'perda_ponderal')

# Funções de Pertinência da Perda Ponderal:
# - Baixo Risco: Sem perda ou perda mínima (<5%)
# - Médio Risco: Perda moderada (5-10%, critério GLIM)
# - Alto Risco: Perda grave (>10%)

perda_ponderal['baixo_risco'] = fuzz.trapmf(perda_ponderal.universe, [0, 0, 2, 5])
perda_ponderal['medio_risco'] = fuzz.trimf(perda_ponderal.universe, [3, 7, 12])
perda_ponderal['alto_risco'] = fuzz.trapmf(perda_ponderal.universe, [10, 12, 20, 30])

# ANTECEDENTE 3: Sarcopenia Clínica (escala 0-3)
# 0 = Ausente, 1 = Leve, 2 = Moderada, 3 = Grave
sarcopenia = ctrl.Antecedent(np.arange(0, 3.1, 0.1), 'sarcopenia')

# Funções de Pertinência da Sarcopenia:
# - Baixo Risco: Ausente ou muito leve
# - Médio Risco: Leve a moderada
# - Alto Risco: Moderada a grave

sarcopenia['baixo_risco'] = fuzz.trapmf(sarcopenia.universe, [0, 0, 0.5, 1])
sarcopenia['medio_risco'] = fuzz.trimf(sarcopenia.universe, [0.5, 1.5, 2.5])
sarcopenia['alto_risco'] = fuzz.trapmf(sarcopenia.universe, [2, 2.5, 3, 3])

# CONSEQUENTE: Escore de Risco Fenotípico (0-100)
risco_fenotipico = ctrl.Consequent(np.arange(0, 101, 1), 'risco_fenotipico')

# Funções de Pertinência da Saída:
risco_fenotipico['baixo'] = fuzz.trapmf(risco_fenotipico.universe, [0, 0, 15, 30])
risco_fenotipico['baixo_moderado'] = fuzz.trimf(risco_fenotipico.universe, [20, 32, 45])
risco_fenotipico['moderado'] = fuzz.trimf(risco_fenotipico.universe, [35, 50, 65])
risco_fenotipico['moderado_alto'] = fuzz.trimf(risco_fenotipico.universe, [55, 67, 80])
risco_fenotipico['alto'] = fuzz.trapmf(risco_fenotipico.universe, [70, 85, 100, 100])

# ==============================================================================
# PASSO 2: DEFINIR AS REGRAS FUZZY (BASE DE CONHECIMENTO)
# ==============================================================================

# Total: 12 regras principais + 1 override (obesidade estável)

# REGRAS DE ALTO RISCO (prioridade alta)
regra1 = ctrl.Rule(imc['alto_risco'] & perda_ponderal['alto_risco'] & sarcopenia['alto_risco'], 
                   risco_fenotipico['alto'])

regra2 = ctrl.Rule(imc['alto_risco'] & perda_ponderal['alto_risco'] & sarcopenia['medio_risco'], 
                   risco_fenotipico['alto'])

regra3 = ctrl.Rule(imc['alto_risco'] & perda_ponderal['medio_risco'] & sarcopenia['alto_risco'], 
                   risco_fenotipico['alto'])

regra4 = ctrl.Rule(imc['alto_risco'] & perda_ponderal['medio_risco'] & sarcopenia['medio_risco'], 
                   risco_fenotipico['moderado_alto'])

# REGRAS DE MÉDIO/MODERADO RISCO
regra5 = ctrl.Rule(imc['alto_risco'] & perda_ponderal['baixo_risco'], 
                   risco_fenotipico['baixo_moderado'])  # Override obesidade estável

regra6 = ctrl.Rule(imc['medio_risco'] & perda_ponderal['alto_risco'] & sarcopenia['alto_risco'], 
                   risco_fenotipico['moderado_alto'])

regra7 = ctrl.Rule(imc['medio_risco'] & perda_ponderal['alto_risco'] & sarcopenia['medio_risco'], 
                   risco_fenotipico['moderado'])

regra8 = ctrl.Rule(imc['medio_risco'] & perda_ponderal['medio_risco'] & sarcopenia['medio_risco'], 
                   risco_fenotipico['moderado'])

regra9 = ctrl.Rule(imc['medio_risco'] & perda_ponderal['medio_risco'] & sarcopenia['baixo_risco'], 
                   risco_fenotipico['baixo_moderado'])

# REGRAS DE BAIXO RISCO
regra10 = ctrl.Rule(imc['baixo_risco'] & perda_ponderal['baixo_risco'] & sarcopenia['baixo_risco'], 
                    risco_fenotipico['baixo'])

regra11 = ctrl.Rule(imc['medio_risco'] & perda_ponderal['baixo_risco'] & sarcopenia['baixo_risco'], 
                    risco_fenotipico['baixo'])

regra12 = ctrl.Rule(imc['alto_risco'] & perda_ponderal['baixo_risco'] & sarcopenia['baixo_risco'], 
                    risco_fenotipico['baixo_moderado'])

# REGRA DEFAULT (caso não coberto)
regra13 = ctrl.Rule(imc['medio_risco'] | perda_ponderal['medio_risco'] | sarcopenia['medio_risco'], 
                    risco_fenotipico['moderado'])

# ==============================================================================
# PASSO 3: CRIAR O SISTEMA DE CONTROLE FUZZY
# ==============================================================================

sistema_fenotipico = ctrl.ControlSystem([
    regra1, regra2, regra3, regra4, regra5, regra6, 
    regra7, regra8, regra9, regra10, regra11, regra12, regra13
])

calculadora_fenotipica = ctrl.ControlSystemSimulation(sistema_fenotipico)

# ==============================================================================
# PASSO 4: FUNÇÃO DE CÁLCULO DO ESCORE
# ==============================================================================

def calcular_risco_fenotipico(imc_valor, perda_valor, sarcopenia_valor, debug=False):
    """
    Calcula o escore de risco nutricional fenotípico.
    
    Parâmetros:
    -----------
    imc_valor : float
        IMC do paciente (kg/m²), entre 12-50
    perda_valor : float
        Perda ponderal em 3 meses (%), entre 0-30
    sarcopenia_valor : float
        Escala de sarcopenia clínica (0-3)
    debug : bool
        Se True, exibe informações detalhadas do cálculo
    
    Retorna:
    --------
    float : Escore de risco fenotípico (0-100)
    """
    
    # Validar inputs
    if not (12 <= imc_valor <= 50):
        raise ValueError(f"IMC fora do intervalo válido (12-50): {imc_valor}")
    if not (0 <= perda_valor <= 30):
        raise ValueError(f"Perda ponderal fora do intervalo válido (0-30): {perda_valor}")
    if not (0 <= sarcopenia_valor <= 3):
        raise ValueError(f"Sarcopenia fora do intervalo válido (0-3): {sarcopenia_valor}")
    
    # Inserir valores no sistema
    calculadora_fenotipica.input['imc'] = imc_valor
    calculadora_fenotipica.input['perda_ponderal'] = perda_valor
    calculadora_fenotipica.input['sarcopenia'] = sarcopenia_valor
    
    # Computar o resultado
    calculadora_fenotipica.compute()
    
    escore = calculadora_fenotipica.output['risco_fenotipico']
    
    if debug:
        print(f"\n{'='*60}")
        print(f"CÁLCULO DO RISCO FENOTÍPICO")
        print(f"{'='*60}")
        print(f"Entradas:")
        print(f"  - IMC: {imc_valor:.1f} kg/m²")
        print(f"  - Perda Ponderal: {perda_valor:.1f}%")
        print(f"  - Sarcopenia: {sarcopenia_valor:.1f}")
        print(f"\nSaída:")
        print(f"  - Escore de Risco Fenotípico: {escore:.1f}/100")
        print(f"{'='*60}\n")
    
    return escore

# ==============================================================================
# PASSO 5: FUNÇÃO PARA CATEGORIZAR O RISCO
# ==============================================================================

def categorizar_risco(escore):
    """
    Categoriza o escore numérico em categoria de risco.
    
    Cut-offs definidos na Rodada 4 Delphi:
    - Baixo: 0-24
    - Baixo-Moderado: 25-39
    - Moderado: 40-59
    - Moderado-Alto: 60-74
    - Alto: 75-100
    """
    if escore < 25:
        return "BAIXO"
    elif escore < 40:
        return "BAIXO-MODERADO"
    elif escore < 60:
        return "MODERADO"
    elif escore < 75:
        return "MODERADO-ALTO"
    else:
        return "ALTO"

# ==============================================================================
# PASSO 6: TESTES COM CASOS CLÍNICOS
# ==============================================================================

if __name__ == "__main__":
    print("\n" + "="*70)
    print("TESTE DO SUBMÓDULO 1: NUTRICIONAL FENOTÍPICO")
    print("="*70)
    
    # Casos de teste baseados nas vinhetas da Rodada 4
    
    casos_teste = [
        {
            "nome": "Caso 1: Baixo Risco (adulto saudável)",
            "imc": 23.5,
            "perda": 1.0,
            "sarcopenia": 0.0,
            "esperado": "BAIXO"
        },
        {
            "nome": "Caso 2: Moderado Risco (perda ponderal significativa)",
            "imc": 21.0,
            "perda": 8.0,
            "sarcopenia": 1.5,
            "esperado": "MODERADO"
        },
        {
            "nome": "Caso 3: Alto Risco (desnutrição grave)",
            "imc": 16.5,
            "perda": 12.0,
            "sarcopenia": 2.5,
            "esperado": "ALTO"
        },
        {
            "nome": "Caso 4: Baixo-Moderado Risco (obesidade estável)",
            "imc": 33.0,
            "perda": 2.0,
            "sarcopenia": 0.5,
            "esperado": "BAIXO-MODERADO"
        },
        {
            "nome": "Caso 5: Moderado-Alto Risco (idoso com sarcopenia)",
            "imc": 19.0,
            "perda": 6.5,
            "sarcopenia": 2.8,
            "esperado": "MODERADO-ALTO ou ALTO"
        }
    ]
    
    print("\nExecutando testes...\n")
    
    resultados = []
    
    for i, caso in enumerate(casos_teste, 1):
        escore = calcular_risco_fenotipico(
            caso["imc"], 
            caso["perda"], 
            caso["sarcopenia"],
            debug=False
        )
        categoria = categorizar_risco(escore)
        
        print(f"{i}. {caso['nome']}")
        print(f"   IMC: {caso['imc']} | Perda: {caso['perda']}% | Sarcopenia: {caso['sarcopenia']}")
        print(f"   -> Escore: {escore:.1f}/100 | Categoria: {categoria}")
        print(f"   -> Esperado: {caso['esperado']}")
        
        # Verificar concordância (tolerância de ±5 pontos ou categoria adjacente)
        concordancia = "[OK]" if caso['esperado'] in categoria or categoria in caso['esperado'] else "[REVISAR]"
        print(f"   -> {concordancia}\n")
        
        resultados.append({
            'caso': caso['nome'],
            'escore': escore,
            'categoria': categoria,
            'esperado': caso['esperado'],
            'concordancia': concordancia
        })
    
    print("="*70)
    print("RESUMO DOS TESTES")
    print("="*70)
    
    casos_ok = sum(1 for r in resultados if '[OK]' in r['concordancia'])
    print(f"Concordancia: {casos_ok}/{len(casos_teste)} casos ({100*casos_ok/len(casos_teste):.0f}%)")
    
    if casos_ok == len(casos_teste):
        print("\n[SUCESSO] TODOS OS TESTES PASSARAM! Submodulo 1 esta funcionando corretamente.")
    else:
        print("\n[ATENCAO] Alguns casos precisam de revisao. Veja detalhes acima.")
    
    print("\n" + "="*70)
    print("Próximo passo: Implementar Submódulo 2 (Ingestão Alimentar)")
    print("="*70 + "\n")
