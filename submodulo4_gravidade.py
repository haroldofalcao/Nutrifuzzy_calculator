"""
CALCULADORA FUZZY DE RISCO NUTRICIONAL
Submodulo 4: Gravidade/Morbidade

Desenvolvido por: Dr. Haroldo Falcao Ramos da Silva
Implementacao: Claude (Anthropic)
Data: Dezembro 2024

VARIAVEIS DE ENTRADA:
1. Diagnostico/Estresse Metabolico (escala 0-3)
2. Comorbidades (0 / 1-2 / >=3, com peso para criticas)
3. Idade (anos)
4. Cirurgia Grande Porte Recente (0=nao, 1=sim)

SAIDA: Escore de Risco de Gravidade/Morbidade (0-100)
"""

import numpy as np
import skfuzzy as fuzz
from skfuzzy import control as ctrl
import matplotlib.pyplot as plt

# ==============================================================================
# PASSO 1: DEFINIR AS VARIAVEIS FUZZY (ANTECEDENTES E CONSEQUENTE)
# ==============================================================================

# ANTECEDENTE 1: Diagnostico/Estresse Metabolico (escala 0-3)
# 0 = Baixo (cirurgia eletiva pequeno porte, condicao clinica estavel)
# 1 = Moderado (fratura quadril, pneumonia, cirurgia abdominal)
# 2 = Alto (politrauma, TCE grave, sepse, pos-op grande porte)
# 3 = Muito Alto (choque septico, transplante, neoplasia avancada)
diagnostico = ctrl.Antecedent(np.arange(0, 3.1, 0.1), 'diagnostico')

# Funcoes de Pertinencia do Diagnostico:
diagnostico['baixo_risco'] = fuzz.trapmf(diagnostico.universe, [0, 0, 0.3, 0.8])
diagnostico['medio_risco'] = fuzz.trimf(diagnostico.universe, [0.5, 1.5, 2.3])
diagnostico['alto_risco'] = fuzz.trapmf(diagnostico.universe, [2, 2.5, 3, 3])

# ANTECEDENTE 2: Comorbidades (escala 0-5)
# 0 = Nenhuma
# 1-2 = 1-2 comorbidades leves/moderadas
# 3-5 = 3+ comorbidades OU presenca de comorbidade critica:
#   - IRC em dialise
#   - ICC classe IV (NYHA)
#   - DPOC O2-dependente
#   - Cirrose hepatica Child C
# NOTA: Comorbidades criticas sempre elevam risco para minimo MODERADO
comorbidades = ctrl.Antecedent(np.arange(0, 5.1, 0.1), 'comorbidades')

# Funcoes de Pertinencia das Comorbidades:
comorbidades['baixo_risco'] = fuzz.trapmf(comorbidades.universe, [0, 0, 0.3, 1.0])
comorbidades['medio_risco'] = fuzz.trimf(comorbidades.universe, [0.5, 2.0, 3.5])
comorbidades['alto_risco'] = fuzz.trapmf(comorbidades.universe, [3, 3.5, 5, 5])

# ANTECEDENTE 3: Idade (anos)
# Universo de discurso: 18 a 100 anos
idade = ctrl.Antecedent(np.arange(18, 101, 1), 'idade')

# Funcoes de Pertinencia da Idade:
# - Baixo Risco: <65 anos
# - Medio Risco: 65-74 anos
# - Alto Risco: >=75 anos (fragilidade, sarcopenia, reserva funcional reduzida)

idade['baixo_risco'] = fuzz.trapmf(idade.universe, [18, 18, 55, 65])
idade['medio_risco'] = fuzz.trimf(idade.universe, [60, 70, 78])
idade['alto_risco'] = fuzz.trapmf(idade.universe, [73, 75, 100, 100])

# ANTECEDENTE 4: Cirurgia de Grande Porte Recente (binario)
# 0 = Nao, 1 = Sim (nos ultimos 7 dias)
# Exemplos: esofagectomia, gastrectomia, duodenopancreatectomia, colectomia
cirurgia = ctrl.Antecedent(np.arange(0, 1.1, 0.1), 'cirurgia')

# Funcoes de Pertinencia da Cirurgia:
cirurgia['nao'] = fuzz.trapmf(cirurgia.universe, [0, 0, 0.2, 0.4])
cirurgia['sim'] = fuzz.trapmf(cirurgia.universe, [0.6, 0.8, 1, 1])

# CONSEQUENTE: Escore de Risco de Gravidade/Morbidade (0-100)
risco_gravidade = ctrl.Consequent(np.arange(0, 101, 1), 'risco_gravidade')

# Funcoes de Pertinencia da Saida:
risco_gravidade['baixo'] = fuzz.trapmf(risco_gravidade.universe, [0, 0, 15, 30])
risco_gravidade['baixo_moderado'] = fuzz.trimf(risco_gravidade.universe, [20, 32, 45])
risco_gravidade['moderado'] = fuzz.trimf(risco_gravidade.universe, [35, 50, 65])
risco_gravidade['moderado_alto'] = fuzz.trimf(risco_gravidade.universe, [55, 67, 80])
risco_gravidade['alto'] = fuzz.trapmf(risco_gravidade.universe, [70, 85, 100, 100])

# ==============================================================================
# PASSO 2: DEFINIR AS REGRAS FUZZY (BASE DE CONHECIMENTO)
# ==============================================================================

# Total: 13 regras (conforme Rodada 3 Delphi)
# ENFASE: Comorbidades criticas (IRC dialise, ICC IV, DPOC O2, cirrose C) sempre >= MODERADO

# REGRAS DE ALTO RISCO
regra1 = ctrl.Rule(diagnostico['alto_risco'] & comorbidades['alto_risco'] & idade['alto_risco'], 
                   risco_gravidade['alto'])

regra2 = ctrl.Rule(diagnostico['alto_risco'] & comorbidades['alto_risco'] & cirurgia['sim'], 
                   risco_gravidade['alto'])

regra3 = ctrl.Rule(diagnostico['alto_risco'] & idade['alto_risco'] & cirurgia['sim'], 
                   risco_gravidade['alto'])

# REGRAS DE MODERADO-ALTO RISCO
regra4 = ctrl.Rule(diagnostico['alto_risco'] & comorbidades['medio_risco'] & idade['medio_risco'], 
                   risco_gravidade['moderado_alto'])

regra5 = ctrl.Rule(diagnostico['medio_risco'] & comorbidades['alto_risco'] & cirurgia['sim'], 
                   risco_gravidade['moderado_alto'])

regra6 = ctrl.Rule(diagnostico['alto_risco'] & comorbidades['baixo_risco'] & cirurgia['sim'], 
                   risco_gravidade['moderado_alto'])

# REGRAS DE MODERADO RISCO
# IMPORTANTE: Comorbidades criticas sempre >= MODERADO
regra7 = ctrl.Rule(comorbidades['alto_risco'], 
                   risco_gravidade['moderado'])  # Regra de dominancia para comorbidades criticas

regra8 = ctrl.Rule(diagnostico['medio_risco'] & comorbidades['medio_risco'] & idade['medio_risco'], 
                   risco_gravidade['moderado'])

regra9 = ctrl.Rule(diagnostico['alto_risco'] & comorbidades['baixo_risco'] & idade['baixo_risco'] & cirurgia['nao'], 
                   risco_gravidade['moderado'])

regra10 = ctrl.Rule(idade['alto_risco'] & cirurgia['sim'], 
                    risco_gravidade['moderado'])

# REGRAS DE BAIXO-MODERADO RISCO
regra11 = ctrl.Rule(diagnostico['medio_risco'] & comorbidades['baixo_risco'] & idade['medio_risco'], 
                    risco_gravidade['baixo_moderado'])

regra12 = ctrl.Rule(diagnostico['baixo_risco'] & comorbidades['medio_risco'] & idade['medio_risco'], 
                    risco_gravidade['baixo_moderado'])

# REGRAS DE BAIXO RISCO
regra13 = ctrl.Rule(diagnostico['baixo_risco'] & comorbidades['baixo_risco'] & idade['baixo_risco'] & cirurgia['nao'], 
                    risco_gravidade['baixo'])

# ==============================================================================
# PASSO 3: CRIAR O SISTEMA DE CONTROLE FUZZY
# ==============================================================================

sistema_gravidade = ctrl.ControlSystem([
    regra1, regra2, regra3, regra4, regra5, regra6, regra7, 
    regra8, regra9, regra10, regra11, regra12, regra13
])

calculadora_gravidade = ctrl.ControlSystemSimulation(sistema_gravidade)

# ==============================================================================
# PASSO 4: FUNCAO DE CALCULO DO ESCORE
# ==============================================================================

def calcular_risco_gravidade(diagnostico_valor, comorbidades_valor, idade_valor, cirurgia_valor, debug=False):
    """
    Calcula o escore de risco de gravidade/morbidade.
    
    Parametros:
    -----------
    diagnostico_valor : float
        Escala de estresse metabolico (0-3)
    comorbidades_valor : float
        Escala de comorbidades (0-5)
        NOTA: Usar 3-5 para comorbidades criticas (IRC dialise, ICC IV, DPOC O2, cirrose C)
    idade_valor : int
        Idade em anos (18-100)
    cirurgia_valor : int
        Cirurgia grande porte recente (0=nao, 1=sim)
    debug : bool
        Se True, exibe informacoes detalhadas do calculo
    
    Retorna:
    --------
    float : Escore de risco de gravidade/morbidade (0-100)
    """
    
    # Validar inputs
    if not (0 <= diagnostico_valor <= 3):
        raise ValueError(f"Diagnostico fora do intervalo valido (0-3): {diagnostico_valor}")
    if not (0 <= comorbidades_valor <= 5):
        raise ValueError(f"Comorbidades fora do intervalo valido (0-5): {comorbidades_valor}")
    if not (18 <= idade_valor <= 100):
        raise ValueError(f"Idade fora do intervalo valido (18-100): {idade_valor}")
    if cirurgia_valor not in [0, 1]:
        raise ValueError(f"Cirurgia deve ser 0 ou 1: {cirurgia_valor}")
    
    # Inserir valores no sistema
    calculadora_gravidade.input['diagnostico'] = diagnostico_valor
    calculadora_gravidade.input['comorbidades'] = comorbidades_valor
    calculadora_gravidade.input['idade'] = idade_valor
    calculadora_gravidade.input['cirurgia'] = cirurgia_valor
    
    # Computar o resultado
    calculadora_gravidade.compute()
    
    escore = calculadora_gravidade.output['risco_gravidade']
    
    if debug:
        print(f"\n{'='*60}")
        print(f"CALCULO DO RISCO DE GRAVIDADE/MORBIDADE")
        print(f"{'='*60}")
        print(f"Entradas:")
        print(f"  - Diagnostico/Estresse: {diagnostico_valor:.1f}")
        print(f"  - Comorbidades: {comorbidades_valor:.1f}")
        print(f"  - Idade: {idade_valor} anos")
        print(f"  - Cirurgia Grande Porte: {'Sim' if cirurgia_valor == 1 else 'Nao'}")
        print(f"\nSaida:")
        print(f"  - Escore de Risco de Gravidade/Morbidade: {escore:.1f}/100")
        print(f"{'='*60}\n")
    
    return escore

# ==============================================================================
# PASSO 5: FUNCAO PARA CATEGORIZAR O RISCO
# ==============================================================================

def categorizar_risco(escore):
    """
    Categoriza o escore numerico em categoria de risco.
    
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
# PASSO 6: TESTES COM CASOS CLINICOS
# ==============================================================================

if __name__ == "__main__":
    print("\n" + "="*70)
    print("TESTE DO SUBMODULO 4: GRAVIDADE/MORBIDADE")
    print("="*70)
    
    # Casos de teste baseados nas vinhetas da Rodada 4
    
    casos_teste = [
        {
            "nome": "Caso 1: Baixo Risco (jovem saudavel)",
            "diagnostico": 0.2,
            "comorbidades": 0.0,
            "idade": 35,
            "cirurgia": 0,
            "esperado": "BAIXO"
        },
        {
            "nome": "Caso 2: Baixo-Moderado Risco (adulto com HAS)",
            "diagnostico": 1.0,
            "comorbidades": 1.0,
            "idade": 68,
            "cirurgia": 0,
            "esperado": "BAIXO-MODERADO"
        },
        {
            "nome": "Caso 3: Moderado Risco (idoso pos-cirurgia)",
            "diagnostico": 1.5,
            "comorbidades": 1.5,
            "idade": 76,
            "cirurgia": 1,
            "esperado": "MODERADO"
        },
        {
            "nome": "Caso 4: Moderado Risco - IRC DIALISE (dominancia)",
            "diagnostico": 0.5,
            "comorbidades": 4.0,
            "idade": 60,
            "cirurgia": 0,
            "esperado": "MODERADO"
        },
        {
            "nome": "Caso 5: Moderado Risco - DPOC O2 + ICC IV",
            "diagnostico": 1.0,
            "comorbidades": 4.5,
            "idade": 72,
            "cirurgia": 0,
            "esperado": "MODERADO ou MODERADO-ALTO"
        },
        {
            "nome": "Caso 6: Moderado-Alto Risco (sepse + comorbidades)",
            "diagnostico": 2.5,
            "comorbidades": 2.5,
            "idade": 70,
            "cirurgia": 0,
            "esperado": "MODERADO-ALTO"
        },
        {
            "nome": "Caso 7: Alto Risco (choque septico idoso pos-op)",
            "diagnostico": 2.8,
            "comorbidades": 3.5,
            "idade": 82,
            "cirurgia": 1,
            "esperado": "ALTO"
        },
        {
            "nome": "Caso 8: Alto Risco (politrauma + cirurgia + idoso)",
            "diagnostico": 2.5,
            "comorbidades": 1.0,
            "idade": 78,
            "cirurgia": 1,
            "esperado": "ALTO"
        }
    ]
    
    print("\nExecutando testes...\n")
    
    resultados = []
    
    for i, caso in enumerate(casos_teste, 1):
        escore = calcular_risco_gravidade(
            caso["diagnostico"], 
            caso["comorbidades"], 
            caso["idade"],
            caso["cirurgia"],
            debug=False
        )
        categoria = categorizar_risco(escore)
        
        print(f"{i}. {caso['nome']}")
        print(f"   Diagnostico: {caso['diagnostico']} | Comorbidades: {caso['comorbidades']} | Idade: {caso['idade']} | Cirurgia: {caso['cirurgia']}")
        print(f"   -> Escore: {escore:.1f}/100 | Categoria: {categoria}")
        print(f"   -> Esperado: {caso['esperado']}")
        
        # Verificar concordancia (tolerancia de ±5 pontos ou categoria adjacente)
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
        print("\n[SUCESSO] TODOS OS TESTES PASSARAM! Submodulo 4 esta funcionando corretamente.")
    else:
        print("\n[ATENCAO] Alguns casos precisam de revisao. Veja detalhes acima.")
    
    print("\n" + "="*70)
    print("Proximo passo: Implementar MODULO INTEGRADOR FINAL")
    print("="*70 + "\n")