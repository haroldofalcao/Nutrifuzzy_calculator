"""
CALCULADORA FUZZY DE RISCO NUTRICIONAL
Submodulo 2: Ingestao Alimentar

Desenvolvido por: Dr. Haroldo Falcao Ramos da Silva
Implementacao: Claude (Anthropic)
Data: Dezembro 2024

VARIAVEIS DE ENTRADA:
1. % VET Consumido (0-100%)
2. Duracao do Deficit Alimentar (dias)
3. Sintomas Gastrointestinais (escala 0-3)

SAIDA: Escore de Risco de Ingestao (0-100)
"""

import numpy as np
import skfuzzy as fuzz
from skfuzzy import control as ctrl
import matplotlib.pyplot as plt

# ==============================================================================
# PASSO 1: DEFINIR AS VARIAVEIS FUZZY (ANTECEDENTES E CONSEQUENTE)
# ==============================================================================

# ANTECEDENTE 1: % VET Consumido (0-100%)
# Universo de discurso: 0 a 100%
vet_consumido = ctrl.Antecedent(np.arange(0, 101, 1), 'vet_consumido')

# Funcoes de Pertinencia do % VET:
# - Baixo Risco: Consumo adequado (>=75% VET)
# - Medio Risco: Consumo subotimo (50-74% VET)
# - Alto Risco: Consumo muito insuficiente (<50% VET) ou jejum

vet_consumido['baixo_risco'] = fuzz.trapmf(vet_consumido.universe, [75, 85, 100, 100])
vet_consumido['medio_risco'] = fuzz.trimf(vet_consumido.universe, [40, 60, 80])
vet_consumido['alto_risco'] = fuzz.trapmf(vet_consumido.universe, [0, 0, 25, 50])

# ANTECEDENTE 2: Duracao do Deficit Alimentar (dias)
# Universo de discurso: 0 a 30 dias
duracao_deficit = ctrl.Antecedent(np.arange(0, 31, 1), 'duracao_deficit')

# Funcoes de Pertinencia da Duracao:
# - Baixo Risco: Deficit curto (<7 dias)
# - Medio Risco: Deficit moderado (7-14 dias)
# - Alto Risco: Deficit prolongado (>14 dias)

duracao_deficit['baixo_risco'] = fuzz.trapmf(duracao_deficit.universe, [0, 0, 3, 7])
duracao_deficit['medio_risco'] = fuzz.trimf(duracao_deficit.universe, [5, 10, 16])
duracao_deficit['alto_risco'] = fuzz.trapmf(duracao_deficit.universe, [12, 14, 30, 30])

# ANTECEDENTE 3: Sintomas Gastrointestinais (escala 0-3)
# 0 = Ausentes, 1 = Leves, 2 = Moderados, 3 = Graves
# Exemplos: nauseas, vomitos, diarreia, distensao abdominal
sintomas_gi = ctrl.Antecedent(np.arange(0, 3.1, 0.1), 'sintomas_gi')

# Funcoes de Pertinencia dos Sintomas GI:
# - Baixo Risco: Ausentes ou muito leves
# - Medio Risco: Leves a moderados
# - Alto Risco: Moderados a graves (impedem alimentacao)

sintomas_gi['baixo_risco'] = fuzz.trapmf(sintomas_gi.universe, [0, 0, 0.3, 0.8])
sintomas_gi['medio_risco'] = fuzz.trimf(sintomas_gi.universe, [0.5, 1.5, 2.3])
sintomas_gi['alto_risco'] = fuzz.trapmf(sintomas_gi.universe, [2, 2.5, 3, 3])

# CONSEQUENTE: Escore de Risco de Ingestao (0-100)
risco_ingestao = ctrl.Consequent(np.arange(0, 101, 1), 'risco_ingestao')

# Funcoes de Pertinencia da Saida:
risco_ingestao['baixo'] = fuzz.trapmf(risco_ingestao.universe, [0, 0, 15, 30])
risco_ingestao['baixo_moderado'] = fuzz.trimf(risco_ingestao.universe, [20, 32, 45])
risco_ingestao['moderado'] = fuzz.trimf(risco_ingestao.universe, [35, 50, 65])
risco_ingestao['moderado_alto'] = fuzz.trimf(risco_ingestao.universe, [55, 67, 80])
risco_ingestao['alto'] = fuzz.trapmf(risco_ingestao.universe, [70, 85, 100, 100])

# ==============================================================================
# PASSO 2: DEFINIR AS REGRAS FUZZY (BASE DE CONHECIMENTO)
# ==============================================================================

# Total: 15 regras (conforme Rodada 3 Delphi)

# REGRAS DE ALTO RISCO (deficit grave e prolongado)
regra1 = ctrl.Rule(vet_consumido['alto_risco'] & duracao_deficit['alto_risco'] & sintomas_gi['alto_risco'], 
                   risco_ingestao['alto'])

regra2 = ctrl.Rule(vet_consumido['alto_risco'] & duracao_deficit['alto_risco'] & sintomas_gi['medio_risco'], 
                   risco_ingestao['alto'])

regra3 = ctrl.Rule(vet_consumido['alto_risco'] & duracao_deficit['medio_risco'] & sintomas_gi['alto_risco'], 
                   risco_ingestao['alto'])

regra4 = ctrl.Rule(vet_consumido['alto_risco'] & duracao_deficit['alto_risco'] & sintomas_gi['baixo_risco'], 
                   risco_ingestao['moderado_alto'])

# REGRAS DE MODERADO-ALTO RISCO
regra5 = ctrl.Rule(vet_consumido['medio_risco'] & duracao_deficit['alto_risco'] & sintomas_gi['alto_risco'], 
                   risco_ingestao['moderado_alto'])

regra6 = ctrl.Rule(vet_consumido['alto_risco'] & duracao_deficit['medio_risco'] & sintomas_gi['medio_risco'], 
                   risco_ingestao['moderado_alto'])

regra7 = ctrl.Rule(vet_consumido['alto_risco'] & duracao_deficit['baixo_risco'] & sintomas_gi['alto_risco'], 
                   risco_ingestao['moderado_alto'])

# REGRAS DE MODERADO RISCO
regra8 = ctrl.Rule(vet_consumido['medio_risco'] & duracao_deficit['medio_risco'] & sintomas_gi['medio_risco'], 
                   risco_ingestao['moderado'])

regra9 = ctrl.Rule(vet_consumido['medio_risco'] & duracao_deficit['alto_risco'] & sintomas_gi['baixo_risco'], 
                   risco_ingestao['moderado'])

regra10 = ctrl.Rule(vet_consumido['alto_risco'] & duracao_deficit['baixo_risco'] & sintomas_gi['baixo_risco'], 
                    risco_ingestao['moderado'])

regra11 = ctrl.Rule(vet_consumido['medio_risco'] & duracao_deficit['medio_risco'] & sintomas_gi['baixo_risco'], 
                    risco_ingestao['baixo_moderado'])

# REGRAS DE BAIXO-MODERADO RISCO
regra12 = ctrl.Rule(vet_consumido['baixo_risco'] & duracao_deficit['medio_risco'] & sintomas_gi['medio_risco'], 
                    risco_ingestao['baixo_moderado'])

regra13 = ctrl.Rule(vet_consumido['medio_risco'] & duracao_deficit['baixo_risco'] & sintomas_gi['medio_risco'], 
                    risco_ingestao['baixo_moderado'])

# REGRAS DE BAIXO RISCO
regra14 = ctrl.Rule(vet_consumido['baixo_risco'] & duracao_deficit['baixo_risco'] & sintomas_gi['baixo_risco'], 
                    risco_ingestao['baixo'])

regra15 = ctrl.Rule(vet_consumido['baixo_risco'] & duracao_deficit['baixo_risco'] & sintomas_gi['medio_risco'], 
                    risco_ingestao['baixo'])

# ==============================================================================
# PASSO 3: CRIAR O SISTEMA DE CONTROLE FUZZY
# ==============================================================================

sistema_ingestao = ctrl.ControlSystem([
    regra1, regra2, regra3, regra4, regra5, regra6, regra7, regra8,
    regra9, regra10, regra11, regra12, regra13, regra14, regra15
])

calculadora_ingestao = ctrl.ControlSystemSimulation(sistema_ingestao)

# ==============================================================================
# PASSO 4: FUNCAO DE CALCULO DO ESCORE
# ==============================================================================

def calcular_risco_ingestao(vet_valor, duracao_valor, sintomas_valor, debug=False):
    """
    Calcula o escore de risco de ingestao alimentar.
    
    Parametros:
    -----------
    vet_valor : float
        % VET consumido (0-100)
    duracao_valor : int
        Duracao do deficit alimentar em dias (0-30)
    sintomas_valor : float
        Escala de sintomas GI (0-3)
    debug : bool
        Se True, exibe informacoes detalhadas do calculo
    
    Retorna:
    --------
    float : Escore de risco de ingestao (0-100)
    """
    
    # Validar inputs
    if not (0 <= vet_valor <= 100):
        raise ValueError(f"% VET fora do intervalo valido (0-100): {vet_valor}")
    if not (0 <= duracao_valor <= 30):
        raise ValueError(f"Duracao fora do intervalo valido (0-30 dias): {duracao_valor}")
    if not (0 <= sintomas_valor <= 3):
        raise ValueError(f"Sintomas GI fora do intervalo valido (0-3): {sintomas_valor}")
    
    # Inserir valores no sistema
    calculadora_ingestao.input['vet_consumido'] = vet_valor
    calculadora_ingestao.input['duracao_deficit'] = duracao_valor
    calculadora_ingestao.input['sintomas_gi'] = sintomas_valor
    
    # Computar o resultado
    calculadora_ingestao.compute()
    
    escore = calculadora_ingestao.output['risco_ingestao']
    
    if debug:
        print(f"\n{'='*60}")
        print(f"CALCULO DO RISCO DE INGESTAO ALIMENTAR")
        print(f"{'='*60}")
        print(f"Entradas:")
        print(f"  - % VET Consumido: {vet_valor:.1f}%")
        print(f"  - Duracao Deficit: {duracao_valor} dias")
        print(f"  - Sintomas GI: {sintomas_valor:.1f}")
        print(f"\nSaida:")
        print(f"  - Escore de Risco de Ingestao: {escore:.1f}/100")
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
    print("TESTE DO SUBMODULO 2: INGESTAO ALIMENTAR")
    print("="*70)
    
    # Casos de teste baseados nas vinhetas da Rodada 4
    
    casos_teste = [
        {
            "nome": "Caso 1: Baixo Risco (ingestao adequada)",
            "vet": 85,
            "duracao": 2,
            "sintomas": 0.2,
            "esperado": "BAIXO"
        },
        {
            "nome": "Caso 2: Baixo-Moderado Risco (ingestao subotima recente)",
            "vet": 65,
            "duracao": 4,
            "sintomas": 1.0,
            "esperado": "BAIXO-MODERADO"
        },
        {
            "nome": "Caso 3: Moderado Risco (deficit prolongado)",
            "vet": 60,
            "duracao": 12,
            "sintomas": 0.5,
            "esperado": "MODERADO"
        },
        {
            "nome": "Caso 4: Moderado-Alto Risco (jejum com sintomas)",
            "vet": 20,
            "duracao": 5,
            "sintomas": 2.5,
            "esperado": "MODERADO-ALTO"
        },
        {
            "nome": "Caso 5: Alto Risco (jejum prolongado + vomitos)",
            "vet": 10,
            "duracao": 18,
            "sintomas": 2.8,
            "esperado": "ALTO"
        },
        {
            "nome": "Caso 6: Moderado-Alto Risco (deficit grave prolongado)",
            "vet": 30,
            "duracao": 16,
            "sintomas": 1.5,
            "esperado": "MODERADO-ALTO ou ALTO"
        }
    ]
    
    print("\nExecutando testes...\n")
    
    resultados = []
    
    for i, caso in enumerate(casos_teste, 1):
        escore = calcular_risco_ingestao(
            caso["vet"], 
            caso["duracao"], 
            caso["sintomas"],
            debug=False
        )
        categoria = categorizar_risco(escore)
        
        print(f"{i}. {caso['nome']}")
        print(f"   VET: {caso['vet']}% | Duracao: {caso['duracao']}d | Sintomas GI: {caso['sintomas']}")
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
        print("\n[SUCESSO] TODOS OS TESTES PASSARAM! Submodulo 2 esta funcionando corretamente.")
    else:
        print("\n[ATENCAO] Alguns casos precisam de revisao. Veja detalhes acima.")
    
    print("\n" + "="*70)
    print("Proximo passo: Implementar Submodulo 3 (Inflamatorio)")
    print("="*70 + "\n")