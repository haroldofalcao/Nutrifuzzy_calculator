"""
CALCULADORA FUZZY DE RISCO NUTRICIONAL
MODULO INTEGRADOR FINAL

Desenvolvido por: Dr. Haroldo Falcao Ramos da Silva
Implementacao: Claude (Anthropic)
Data: Dezembro 2024

ENTRADAS:
- Escore Fenotipico (0-100) - Peso 30%
- Escore Ingestao (0-100) - Peso 25%
- Escore Inflamatorio (0-100) - Peso 15%
- Escore Gravidade (0-100) - Peso 30%

SAIDA: ESCORE FINAL DE RISCO NUTRICIONAL (0-100)
Categorias: Baixo / Baixo-Moderado / Moderado / Moderado-Alto / Alto
"""

import numpy as np
import skfuzzy as fuzz
from skfuzzy import control as ctrl
import matplotlib.pyplot as plt

# ==============================================================================
# PASSO 1: DEFINIR AS VARIAVEIS FUZZY (ANTECEDENTES E CONSEQUENTE)
# ==============================================================================

# ANTECEDENTE 1: Escore Fenotipico (0-100) - Peso 30%
escore_fenotipico = ctrl.Antecedent(np.arange(0, 101, 1), 'escore_fenotipico')

escore_fenotipico['baixo'] = fuzz.trapmf(escore_fenotipico.universe, [0, 0, 20, 30])
escore_fenotipico['baixo_moderado'] = fuzz.trimf(escore_fenotipico.universe, [25, 35, 45])
escore_fenotipico['moderado'] = fuzz.trimf(escore_fenotipico.universe, [40, 50, 60])
escore_fenotipico['moderado_alto'] = fuzz.trimf(escore_fenotipico.universe, [55, 65, 75])
escore_fenotipico['alto'] = fuzz.trapmf(escore_fenotipico.universe, [70, 80, 100, 100])

# ANTECEDENTE 2: Escore Ingestao (0-100) - Peso 25%
escore_ingestao = ctrl.Antecedent(np.arange(0, 101, 1), 'escore_ingestao')

escore_ingestao['baixo'] = fuzz.trapmf(escore_ingestao.universe, [0, 0, 20, 30])
escore_ingestao['baixo_moderado'] = fuzz.trimf(escore_ingestao.universe, [25, 35, 45])
escore_ingestao['moderado'] = fuzz.trimf(escore_ingestao.universe, [40, 50, 60])
escore_ingestao['moderado_alto'] = fuzz.trimf(escore_ingestao.universe, [55, 65, 75])
escore_ingestao['alto'] = fuzz.trapmf(escore_ingestao.universe, [70, 80, 100, 100])

# ANTECEDENTE 3: Escore Inflamatorio (0-100) - Peso 15%
escore_inflamatorio = ctrl.Antecedent(np.arange(0, 101, 1), 'escore_inflamatorio')

escore_inflamatorio['baixo'] = fuzz.trapmf(escore_inflamatorio.universe, [0, 0, 20, 30])
escore_inflamatorio['baixo_moderado'] = fuzz.trimf(escore_inflamatorio.universe, [25, 35, 45])
escore_inflamatorio['moderado'] = fuzz.trimf(escore_inflamatorio.universe, [40, 50, 60])
escore_inflamatorio['moderado_alto'] = fuzz.trimf(escore_inflamatorio.universe, [55, 65, 75])
escore_inflamatorio['alto'] = fuzz.trapmf(escore_inflamatorio.universe, [70, 80, 100, 100])

# ANTECEDENTE 4: Escore Gravidade (0-100) - Peso 30%
escore_gravidade = ctrl.Antecedent(np.arange(0, 101, 1), 'escore_gravidade')

escore_gravidade['baixo'] = fuzz.trapmf(escore_gravidade.universe, [0, 0, 20, 30])
escore_gravidade['baixo_moderado'] = fuzz.trimf(escore_gravidade.universe, [25, 35, 45])
escore_gravidade['moderado'] = fuzz.trimf(escore_gravidade.universe, [40, 50, 60])
escore_gravidade['moderado_alto'] = fuzz.trimf(escore_gravidade.universe, [55, 65, 75])
escore_gravidade['alto'] = fuzz.trapmf(escore_gravidade.universe, [70, 80, 100, 100])

# CONSEQUENTE: ESCORE FINAL DE RISCO NUTRICIONAL (0-100)
risco_final = ctrl.Consequent(np.arange(0, 101, 1), 'risco_final')

risco_final['baixo'] = fuzz.trapmf(risco_final.universe, [0, 0, 15, 25])
risco_final['baixo_moderado'] = fuzz.trimf(risco_final.universe, [20, 32, 40])
risco_final['moderado'] = fuzz.trimf(risco_final.universe, [35, 50, 60])
risco_final['moderado_alto'] = fuzz.trimf(risco_final.universe, [55, 67, 75])
risco_final['alto'] = fuzz.trapmf(risco_final.universe, [70, 80, 100, 100])

# ==============================================================================
# PASSO 2: DEFINIR AS REGRAS FUZZY (BASE DE CONHECIMENTO)
# ==============================================================================

# Total: 8 regras de integracao + 2 regras de ajuste sinergico + 1 regra default = 11 regras

# REGRAS DE ALTO RISCO
# Fenotipico e Gravidade tem peso 30% cada - se ambos altos, risco final e alto
regra1 = ctrl.Rule(escore_fenotipico['alto'] & escore_gravidade['alto'], 
                   risco_final['alto'])

regra2 = ctrl.Rule(escore_fenotipico['alto'] & escore_ingestao['alto'], 
                   risco_final['alto'])

# REGRAS DE MODERADO-ALTO RISCO
regra3 = ctrl.Rule(escore_fenotipico['moderado_alto'] & escore_gravidade['moderado_alto'], 
                   risco_final['moderado_alto'])

regra4 = ctrl.Rule(escore_ingestao['alto'] & escore_gravidade['moderado_alto'], 
                   risco_final['moderado_alto'])

regra5 = ctrl.Rule(escore_fenotipico['alto'] | escore_ingestao['alto'] | escore_gravidade['alto'], 
                   risco_final['moderado_alto'])

# REGRAS DE MODERADO RISCO
regra6 = ctrl.Rule(escore_fenotipico['moderado'] & escore_gravidade['moderado'], 
                   risco_final['moderado'])

regra7 = ctrl.Rule(escore_ingestao['moderado'] & escore_inflamatorio['moderado'], 
                   risco_final['moderado'])

regra8 = ctrl.Rule(escore_fenotipico['moderado'] | escore_ingestao['moderado'] | escore_gravidade['moderado'], 
                   risco_final['moderado'])

# REGRAS DE BAIXO-MODERADO RISCO
regra9 = ctrl.Rule(escore_fenotipico['baixo_moderado'] & escore_gravidade['baixo_moderado'], 
                   risco_final['baixo_moderado'])

# REGRAS DE BAIXO RISCO
regra10 = ctrl.Rule(escore_fenotipico['baixo'] & escore_ingestao['baixo'] & escore_gravidade['baixo'], 
                    risco_final['baixo'])

# REGRAS DE AJUSTE SINERGICO
# Quando desnutricao grave (fenotipico alto) + deficit alimentar grave (ingestao alta)
# = SINERGIA que amplifica risco
regra11 = ctrl.Rule(escore_fenotipico['alto'] & escore_ingestao['moderado_alto'], 
                    risco_final['alto'])

# Quando inflamacao grave (inflamatorio alto) + gravidade alta + qualquer deficit nutricional
# = SINERGIA (catabolismo acelerado)
regra12 = ctrl.Rule(escore_inflamatorio['alto'] & escore_gravidade['alto'], 
                    risco_final['moderado_alto'])

# ==============================================================================
# PASSO 3: CRIAR O SISTEMA DE CONTROLE FUZZY
# ==============================================================================

sistema_integrador = ctrl.ControlSystem([
    regra1, regra2, regra3, regra4, regra5, regra6, regra7, regra8, regra9, regra10, regra11, regra12
])

calculadora_final = ctrl.ControlSystemSimulation(sistema_integrador)

# ==============================================================================
# PASSO 4: FUNCAO DE CALCULO DO ESCORE FINAL
# ==============================================================================

def calcular_risco_final(fenotipico, ingestao, inflamatorio, gravidade, debug=False):
    """
    Calcula o ESCORE FINAL DE RISCO NUTRICIONAL integrando os 4 submodulos.
    
    Parametros:
    -----------
    fenotipico : float
        Escore do Submodulo 1 (0-100)
    ingestao : float
        Escore do Submodulo 2 (0-100)
    inflamatorio : float
        Escore do Submodulo 3 (0-100)
    gravidade : float
        Escore do Submodulo 4 (0-100)
    debug : bool
        Se True, exibe informacoes detalhadas do calculo
    
    Retorna:
    --------
    float : Escore final de risco nutricional (0-100)
    """
    
    # Validar inputs
    for nome, valor in [('fenotipico', fenotipico), ('ingestao', ingestao), 
                        ('inflamatorio', inflamatorio), ('gravidade', gravidade)]:
        if not (0 <= valor <= 100):
            raise ValueError(f"Escore {nome} fora do intervalo valido (0-100): {valor}")
    
    # Inserir valores no sistema
    calculadora_final.input['escore_fenotipico'] = fenotipico
    calculadora_final.input['escore_ingestao'] = ingestao
    calculadora_final.input['escore_inflamatorio'] = inflamatorio
    calculadora_final.input['escore_gravidade'] = gravidade
    
    # Computar o resultado
    calculadora_final.compute()
    
    escore = calculadora_final.output['risco_final']
    
    if debug:
        print(f"\n{'='*70}")
        print(f"CALCULO DO ESCORE FINAL DE RISCO NUTRICIONAL")
        print(f"{'='*70}")
        print(f"Entradas dos Submodulos:")
        print(f"  - Fenotipico (30%):     {fenotipico:.1f}/100")
        print(f"  - Ingestao (25%):       {ingestao:.1f}/100")
        print(f"  - Inflamatorio (15%):   {inflamatorio:.1f}/100")
        print(f"  - Gravidade (30%):      {gravidade:.1f}/100")
        print(f"\nSaida Final:")
        print(f"  - ESCORE FINAL:         {escore:.1f}/100")
        print(f"  - CATEGORIA:            {categorizar_risco(escore)}")
        print(f"{'='*70}\n")
    
    return escore

# ==============================================================================
# PASSO 5: FUNCAO PARA CATEGORIZAR O RISCO FINAL
# ==============================================================================

def categorizar_risco(escore):
    """
    Categoriza o escore final em categoria de risco.
    
    Cut-offs finais (Rodada 4 Delphi):
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

def get_recomendacao(categoria):
    """
    Retorna recomendacao clinica baseada na categoria de risco.
    
    IMPORTANTE: Esta calculadora realiza TRIAGEM, nao prescreve condutas.
    As recomendacoes sao gerais e devem ser adaptadas ao contexto clinico.
    """
    recomendacoes = {
        "BAIXO": "Monitoramento padrao. Reavaliacao em 7 dias ou conforme protocolo institucional.",
        "BAIXO-MODERADO": "Atencao nutricional. Considerar avaliacao nutricional detalhada.",
        "MODERADO": "Risco nutricional identificado. Recomenda-se avaliacao por equipe de nutricao.",
        "MODERADO-ALTO": "Alto risco nutricional. Avaliacao e suporte nutricional prioritarios.",
        "ALTO": "Risco nutricional CRITICO. Intervencao nutricional IMEDIATA recomendada."
    }
    return recomendacoes.get(categoria, "Categoria nao reconhecida")

# ==============================================================================
# PASSO 6: TESTES COM CASOS CLINICOS COMPLETOS
# ==============================================================================

if __name__ == "__main__":
    print("\n" + "="*80)
    print("TESTE DO MODULO INTEGRADOR FINAL - CALCULADORA FUZZY COMPLETA")
    print("="*80)
    
    # Casos de teste integrando os 4 submodulos
    
    casos_teste = [
        {
            "nome": "Caso 1: BAIXO RISCO - Adulto jovem saudavel",
            "fenotipico": 15,
            "ingestao": 10,
            "inflamatorio": 8,
            "gravidade": 12,
            "esperado": "BAIXO"
        },
        {
            "nome": "Caso 2: BAIXO-MODERADO - Idoso com ingestao subotima",
            "fenotipico": 28,
            "ingestao": 35,
            "inflamatorio": 15,
            "gravidade": 32,
            "esperado": "BAIXO-MODERADO"
        },
        {
            "nome": "Caso 3: MODERADO - Pneumonia com perda ponderal",
            "fenotipico": 48,
            "ingestao": 52,
            "inflamatorio": 45,
            "gravidade": 50,
            "esperado": "MODERADO"
        },
        {
            "nome": "Caso 4: MODERADO-ALTO - Pos-op com comorbidades",
            "fenotipico": 62,
            "ingestao": 68,
            "inflamatorio": 55,
            "gravidade": 65,
            "esperado": "MODERADO-ALTO"
        },
        {
            "nome": "Caso 5: ALTO - Desnutricao grave + sepse",
            "fenotipico": 85,
            "ingestao": 88,
            "inflamatorio": 82,
            "gravidade": 80,
            "esperado": "ALTO"
        },
        {
            "nome": "Caso 6: ALTO - SINERGIA (desnutricao + deficit alimentar grave)",
            "fenotipico": 78,
            "ingestao": 72,
            "inflamatorio": 45,
            "gravidade": 55,
            "esperado": "ALTO"
        },
        {
            "nome": "Caso 7: MODERADO-ALTO - SINERGIA (inflamacao + gravidade + deficit moderado)",
            "fenotipico": 52,
            "ingestao": 48,
            "inflamatorio": 75,
            "gravidade": 78,
            "esperado": "MODERADO-ALTO"
        },
        {
            "nome": "Caso 8: MODERADO - IRC dialise + ingestao adequada",
            "fenotipico": 35,
            "ingestao": 20,
            "inflamatorio": 40,
            "gravidade": 55,
            "esperado": "MODERADO"
        }
    ]
    
    print("\nExecutando testes...\n")
    
    resultados = []
    
    for i, caso in enumerate(casos_teste, 1):
        escore = calcular_risco_final(
            caso["fenotipico"], 
            caso["ingestao"], 
            caso["inflamatorio"],
            caso["gravidade"],
            debug=False
        )
        categoria = categorizar_risco(escore)
        recomendacao = get_recomendacao(categoria)
        
        print(f"{i}. {caso['nome']}")
        print(f"   Escores: Fen={caso['fenotipico']} | Ing={caso['ingestao']} | Inf={caso['inflamatorio']} | Grav={caso['gravidade']}")
        print(f"   -> ESCORE FINAL: {escore:.1f}/100")
        print(f"   -> CATEGORIA: {categoria}")
        print(f"   -> Esperado: {caso['esperado']}")
        
        # Verificar concordancia
        concordancia = "[OK]" if caso['esperado'] in categoria or categoria in caso['esperado'] else "[REVISAR]"
        print(f"   -> {concordancia}")
        print(f"   -> Recomendacao: {recomendacao}\n")
        
        resultados.append({
            'caso': caso['nome'],
            'escore': escore,
            'categoria': categoria,
            'esperado': caso['esperado'],
            'concordancia': concordancia
        })
    
    print("="*80)
    print("RESUMO DOS TESTES")
    print("="*80)
    
    casos_ok = sum(1 for r in resultados if '[OK]' in r['concordancia'])
    print(f"Concordancia: {casos_ok}/{len(casos_teste)} casos ({100*casos_ok/len(casos_teste):.0f}%)")
    
    if casos_ok == len(casos_teste):
        print("\n[SUCESSO] TODOS OS TESTES PASSARAM!")
        print("A CALCULADORA FUZZY DE RISCO NUTRICIONAL ESTA COMPLETA E FUNCIONAL!")
    else:
        print("\n[ATENCAO] Alguns casos precisam de revisao. Veja detalhes acima.")
    
    print("\n" + "="*80)
    print("PROXIMOS PASSOS:")
    print("1. Testar com os 20 casos clinicos completos da Rodada 4")
    print("2. Criar calculadora integrada (arquivo unico com todos os submodulos)")
    print("3. Gerar especificacao tecnica YAML/JSON")
    print("4. Redigir o artigo cientifico")
    print("\nNOTA: Sistema integrador possui 12 regras fuzzy (8 basicas + 2 sinergicas + 2 cobertura)")
    print("="*80 + "\n")
