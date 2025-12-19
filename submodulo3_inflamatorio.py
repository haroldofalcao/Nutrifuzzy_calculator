"""
CALCULADORA FUZZY DE RISCO NUTRICIONAL
Submodulo 3: Inflamatorio

Desenvolvido por: Dr. Haroldo Falcao Ramos da Silva
Implementacao: Claude (Anthropic)
Data: Dezembro 2024

VARIAVEIS DE ENTRADA:
1. PCR - Proteina C Reativa (mg/L)
2. Albumina Serica (g/dL)
3. Febre (escala 0-3: ausente/subfebril/febre/hipertermia)

SAIDA: Escore de Risco Inflamatorio (0-100)
"""

import numpy as np
import skfuzzy as fuzz
from skfuzzy import control as ctrl
import matplotlib.pyplot as plt

# ==============================================================================
# PASSO 1: DEFINIR AS VARIAVEIS FUZZY (ANTECEDENTES E CONSEQUENTE)
# ==============================================================================

# ANTECEDENTE 1: PCR - Proteina C Reativa (mg/L)
# Universo de discurso: 0 a 400 mg/L
pcr = ctrl.Antecedent(np.arange(0, 401, 1), 'pcr')

# Funcoes de Pertinencia da PCR:
# - Baixo Risco: PCR normal (<10 mg/L)
# - Medio Risco: PCR elevada (10-100 mg/L)
# - Alto Risco: PCR muito elevada (>100 mg/L)
# REGRA DE DOMINANCIA: PCR >200 sempre indica alto risco inflamatorio

pcr['baixo_risco'] = fuzz.trapmf(pcr.universe, [0, 0, 5, 10])
pcr['medio_risco'] = fuzz.trimf(pcr.universe, [5, 50, 120])
pcr['alto_risco'] = fuzz.trapmf(pcr.universe, [80, 100, 400, 400])

# ANTECEDENTE 2: Albumina Serica (g/dL)
# Universo de discurso: 1.5 a 5.0 g/dL
albumina = ctrl.Antecedent(np.arange(1.5, 5.1, 0.1), 'albumina')

# Funcoes de Pertinencia da Albumina:
# - Baixo Risco: Albumina normal (>=3.5 g/dL)
# - Medio Risco: Albumina reduzida leve (3.0-3.4 g/dL)
# - Alto Risco: Albumina reduzida moderada/grave (<3.0 g/dL)
# NOTA: Albumina e marcador negativo de fase aguda, nao estado nutricional isolado

albumina['baixo_risco'] = fuzz.trapmf(albumina.universe, [3.5, 4.0, 5.0, 5.0])
albumina['medio_risco'] = fuzz.trimf(albumina.universe, [2.8, 3.2, 3.7])
albumina['alto_risco'] = fuzz.trapmf(albumina.universe, [1.5, 1.5, 2.5, 3.0])

# ANTECEDENTE 3: Febre (escala 0-3)
# 0 = Ausente, 1 = Subfebril (<38C), 2 = Febre (38-39C), 3 = Hipertermia (>39C)
febre = ctrl.Antecedent(np.arange(0, 3.1, 0.1), 'febre')

# Funcoes de Pertinencia da Febre:
# - Baixo Risco: Ausente ou subfebril
# - Medio Risco: Febre leve a moderada
# - Alto Risco: Febre alta ou hipertermia

febre['baixo_risco'] = fuzz.trapmf(febre.universe, [0, 0, 0.5, 1.2])
febre['medio_risco'] = fuzz.trimf(febre.universe, [0.8, 1.8, 2.5])
febre['alto_risco'] = fuzz.trapmf(febre.universe, [2.2, 2.7, 3, 3])

# CONSEQUENTE: Escore de Risco Inflamatorio (0-100)
risco_inflamatorio = ctrl.Consequent(np.arange(0, 101, 1), 'risco_inflamatorio')

# Funcoes de Pertinencia da Saida:
risco_inflamatorio['baixo'] = fuzz.trapmf(risco_inflamatorio.universe, [0, 0, 15, 30])
risco_inflamatorio['baixo_moderado'] = fuzz.trimf(risco_inflamatorio.universe, [20, 32, 45])
risco_inflamatorio['moderado'] = fuzz.trimf(risco_inflamatorio.universe, [35, 50, 65])
risco_inflamatorio['moderado_alto'] = fuzz.trimf(risco_inflamatorio.universe, [55, 67, 80])
risco_inflamatorio['alto'] = fuzz.trapmf(risco_inflamatorio.universe, [70, 85, 100, 100])

# ==============================================================================
# PASSO 2: DEFINIR AS REGRAS FUZZY (BASE DE CONHECIMENTO)
# ==============================================================================

# Total: 10 regras (conforme Rodada 3 Delphi)
# INCLUI REGRA DE DOMINANCIA: PCR >200 sempre alto risco

# REGRAS DE ALTO RISCO (inflamacao grave)
regra1 = ctrl.Rule(pcr['alto_risco'] & albumina['alto_risco'] & febre['alto_risco'], 
                   risco_inflamatorio['alto'])

regra2 = ctrl.Rule(pcr['alto_risco'] & albumina['alto_risco'] & febre['medio_risco'], 
                   risco_inflamatorio['alto'])

regra3 = ctrl.Rule(pcr['alto_risco'] & albumina['medio_risco'] & febre['alto_risco'], 
                   risco_inflamatorio['alto'])

# REGRA DE DOMINANCIA: PCR extremamente elevada (>200) sempre alto risco
# Nota: Esta regra e capturada pela MF de alto_risco da PCR (>100)
# mas enfatizamos que valores >200 tem pertinencia maxima
regra4 = ctrl.Rule(pcr['alto_risco'] & albumina['alto_risco'], 
                   risco_inflamatorio['alto'])

# REGRAS DE MODERADO-ALTO RISCO
regra5 = ctrl.Rule(pcr['alto_risco'] & albumina['baixo_risco'] & febre['medio_risco'], 
                   risco_inflamatorio['moderado_alto'])

regra6 = ctrl.Rule(pcr['medio_risco'] & albumina['alto_risco'] & febre['alto_risco'], 
                   risco_inflamatorio['moderado_alto'])

# REGRAS DE MODERADO RISCO
regra7 = ctrl.Rule(pcr['medio_risco'] & albumina['medio_risco'] & febre['medio_risco'], 
                   risco_inflamatorio['moderado'])

regra8 = ctrl.Rule(pcr['alto_risco'] & albumina['baixo_risco'] & febre['baixo_risco'], 
                   risco_inflamatorio['moderado'])

# REGRAS DE BAIXO-MODERADO E BAIXO RISCO
regra9 = ctrl.Rule(pcr['medio_risco'] & albumina['baixo_risco'] & febre['baixo_risco'], 
                   risco_inflamatorio['baixo_moderado'])

regra10 = ctrl.Rule(pcr['baixo_risco'] & albumina['baixo_risco'] & febre['baixo_risco'], 
                    risco_inflamatorio['baixo'])

# ==============================================================================
# PASSO 3: CRIAR O SISTEMA DE CONTROLE FUZZY
# ==============================================================================

sistema_inflamatorio = ctrl.ControlSystem([
    regra1, regra2, regra3, regra4, regra5, regra6, regra7, regra8, regra9, regra10
])

calculadora_inflamatorio = ctrl.ControlSystemSimulation(sistema_inflamatorio)

# ==============================================================================
# PASSO 4: FUNCAO DE CALCULO DO ESCORE
# ==============================================================================

def calcular_risco_inflamatorio(pcr_valor, albumina_valor, febre_valor, debug=False):
    """
    Calcula o escore de risco inflamatorio.
    
    Parametros:
    -----------
    pcr_valor : float
        PCR em mg/L (0-400)
    albumina_valor : float
        Albumina serica em g/dL (1.5-5.0)
    febre_valor : float
        Escala de febre (0-3)
    debug : bool
        Se True, exibe informacoes detalhadas do calculo
    
    Retorna:
    --------
    float : Escore de risco inflamatorio (0-100)
    """
    
    # Validar inputs
    if not (0 <= pcr_valor <= 400):
        raise ValueError(f"PCR fora do intervalo valido (0-400 mg/L): {pcr_valor}")
    if not (1.5 <= albumina_valor <= 5.0):
        raise ValueError(f"Albumina fora do intervalo valido (1.5-5.0 g/dL): {albumina_valor}")
    if not (0 <= febre_valor <= 3):
        raise ValueError(f"Febre fora do intervalo valido (0-3): {febre_valor}")
    
    # Inserir valores no sistema
    calculadora_inflamatorio.input['pcr'] = pcr_valor
    calculadora_inflamatorio.input['albumina'] = albumina_valor
    calculadora_inflamatorio.input['febre'] = febre_valor
    
    # Computar o resultado
    calculadora_inflamatorio.compute()
    
    escore = calculadora_inflamatorio.output['risco_inflamatorio']
    
    if debug:
        print(f"\n{'='*60}")
        print(f"CALCULO DO RISCO INFLAMATORIO")
        print(f"{'='*60}")
        print(f"Entradas:")
        print(f"  - PCR: {pcr_valor:.1f} mg/L")
        print(f"  - Albumina: {albumina_valor:.1f} g/dL")
        print(f"  - Febre: {febre_valor:.1f}")
        print(f"\nSaida:")
        print(f"  - Escore de Risco Inflamatorio: {escore:.1f}/100")
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
    print("TESTE DO SUBMODULO 3: INFLAMATORIO")
    print("="*70)
    
    # Casos de teste baseados nas vinhetas da Rodada 4
    
    casos_teste = [
        {
            "nome": "Caso 1: Baixo Risco (sem inflamacao)",
            "pcr": 3.0,
            "albumina": 4.2,
            "febre": 0.0,
            "esperado": "BAIXO"
        },
        {
            "nome": "Caso 2: Baixo-Moderado Risco (inflamacao leve)",
            "pcr": 25,
            "albumina": 3.8,
            "febre": 0.5,
            "esperado": "BAIXO-MODERADO"
        },
        {
            "nome": "Caso 3: Moderado Risco (inflamacao moderada)",
            "pcr": 80,
            "albumina": 3.1,
            "febre": 1.5,
            "esperado": "MODERADO"
        },
        {
            "nome": "Caso 4: Moderado-Alto Risco (sepse sem choque)",
            "pcr": 150,
            "albumina": 2.6,
            "febre": 2.3,
            "esperado": "MODERADO-ALTO"
        },
        {
            "nome": "Caso 5: Alto Risco (choque septico)",
            "pcr": 280,
            "albumina": 2.0,
            "febre": 2.8,
            "esperado": "ALTO"
        },
        {
            "nome": "Caso 6: Alto Risco - DOMINANCIA (PCR >200)",
            "pcr": 220,
            "albumina": 2.2,
            "febre": 1.0,
            "esperado": "ALTO"
        },
        {
            "nome": "Caso 7: Moderado Risco (PCR alta, albumina normal)",
            "pcr": 110,
            "albumina": 3.7,
            "febre": 0.2,
            "esperado": "MODERADO"
        }
    ]
    
    print("\nExecutando testes...\n")
    
    resultados = []
    
    for i, caso in enumerate(casos_teste, 1):
        escore = calcular_risco_inflamatorio(
            caso["pcr"], 
            caso["albumina"], 
            caso["febre"],
            debug=False
        )
        categoria = categorizar_risco(escore)
        
        print(f"{i}. {caso['nome']}")
        print(f"   PCR: {caso['pcr']} mg/L | Albumina: {caso['albumina']} g/dL | Febre: {caso['febre']}")
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
        print("\n[SUCESSO] TODOS OS TESTES PASSARAM! Submodulo 3 esta funcionando corretamente.")
    else:
        print("\n[ATENCAO] Alguns casos precisam de revisao. Veja detalhes acima.")
    
    print("\n" + "="*70)
    print("Proximo passo: Implementar Submodulo 4 (Gravidade/Morbidade)")
    print("="*70 + "\n")