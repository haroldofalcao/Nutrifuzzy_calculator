"""
Script de teste para validar correções no sistema fuzzy
Testa casos severos que deveriam resultar em ALTO risco
"""

import sys
import os

# Adiciona o diretório ao path para importar o módulo
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from calculadora_desktop import (
    calcular_submodulo_fenotipico,
    calcular_submodulo_ingestao,
    calcular_submodulo_inflamatorio,
    calcular_submodulo_gravidade,
    calcular_risco_final_integrado,
    categorizar_risco
)

print("=" * 80)
print("TESTE DE CORREÇÕES - SISTEMA FUZZY DE RISCO NUTRICIONAL")
print("=" * 80)
print()

# Caso 1: Paciente com desnutrição severa
print("CASO 1: DESNUTRIÇÃO SEVERA")
print("-" * 80)
print("Inputs:")
print("  - IMC: 15.0 kg/m² (muito baixo)")
print("  - Perda Ponderal: 15% (alta)")
print("  - Sarcopenia: 3.0 (severa)")
print("  - VET: 30% (baixo)")
print("  - Duração Déficit: 14 dias (prolongado)")
print("  - Sintomas GI: 2.5 (severos)")
print("  - PCR: 150 mg/L (elevado)")
print("  - Albumina: 2.0 g/dL (baixa)")
print("  - Febre: 2.5 (alta)")
print("  - Diagnóstico: 3.0 (grave)")
print("  - Comorbidades: 4.5 (múltiplas)")
print("  - Idade: 75 anos (idoso)")
print("  - Cirurgia: Sim")
print()

# Calcular submódulos
escore_feno = calcular_submodulo_fenotipico(15.0, 15, 3.0)
escore_ing = calcular_submodulo_ingestao(30, 14, 2.5)
escore_infl = calcular_submodulo_inflamatorio(150, 2.0, 2.5)
escore_grav = calcular_submodulo_gravidade(3.0, 4.5, 75, 1)

print(f"Escores dos Submódulos:")
print(f"  - Fenotípico: {escore_feno:.2f}")
print(f"  - Ingestão: {escore_ing:.2f}")
print(f"  - Inflamatório: {escore_infl:.2f}")
print(f"  - Gravidade: {escore_grav:.2f}")
print()

# Calcular risco final
escore_final = calcular_risco_final_integrado(escore_feno, escore_ing, escore_infl, escore_grav)
categoria, cor = categorizar_risco(escore_final)

print(f"Escore Final: {escore_final:.2f}")
print(f"Categoria: {categoria}")
print(f"ESPERADO: ALTO ou MODERADO-ALTO")
print()

# Validação
if escore_final >= 70:
    print("[OK] SUCESSO - Score >= 70, categoria correta!")
else:
    print(f"[FALHA] Score {escore_final:.2f} muito baixo para caso severo!")
print()
print()

# Caso 2: Paciente crítico com múltiplos fatores de risco
print("CASO 2: PACIENTE CRÍTICO")
print("-" * 80)
print("Inputs:")
print("  - IMC: 16.5 kg/m²")
print("  - Perda Ponderal: 12%")
print("  - Sarcopenia: 2.8")
print("  - VET: 25%")
print("  - Duração Déficit: 20 dias")
print("  - Sintomas GI: 3.0")
print("  - PCR: 200 mg/L")
print("  - Albumina: 1.8 g/dL")
print("  - Febre: 3.0")
print("  - Diagnóstico: 2.8")
print("  - Comorbidades: 5.0")
print("  - Idade: 82 anos")
print("  - Cirurgia: Sim")
print()

escore_feno2 = calcular_submodulo_fenotipico(16.5, 12, 2.8)
escore_ing2 = calcular_submodulo_ingestao(25, 20, 3.0)
escore_infl2 = calcular_submodulo_inflamatorio(200, 1.8, 3.0)
escore_grav2 = calcular_submodulo_gravidade(2.8, 5.0, 82, 1)

print(f"Escores dos Submódulos:")
print(f"  - Fenotípico: {escore_feno2:.2f}")
print(f"  - Ingestão: {escore_ing2:.2f}")
print(f"  - Inflamatório: {escore_infl2:.2f}")
print(f"  - Gravidade: {escore_grav2:.2f}")
print()

escore_final2 = calcular_risco_final_integrado(escore_feno2, escore_ing2, escore_infl2, escore_grav2)
categoria2, cor2 = categorizar_risco(escore_final2)

print(f"Escore Final: {escore_final2:.2f}")
print(f"Categoria: {categoria2}")
print(f"ESPERADO: ALTO")
print()

if escore_final2 >= 70:
    print("[OK] SUCESSO - Score >= 70, categoria ALTO!")
else:
    print(f"[FALHA] Score {escore_final2:.2f} muito baixo!")
print()
print()

# Caso 3: Paciente moderado (para validar que casos intermediários funcionam)
print("CASO 3: RISCO MODERADO (CONTROLE)")
print("-" * 80)
print("Inputs:")
print("  - IMC: 22.0 kg/m²")
print("  - Perda Ponderal: 5%")
print("  - Sarcopenia: 1.5")
print("  - VET: 60%")
print("  - Duração Déficit: 5 dias")
print("  - Sintomas GI: 1.5")
print("  - PCR: 50 mg/L")
print("  - Albumina: 3.2 g/dL")
print("  - Febre: 1.0")
print("  - Diagnóstico: 1.5")
print("  - Comorbidades: 2.0")
print("  - Idade: 55 anos")
print("  - Cirurgia: Não")
print()

escore_feno3 = calcular_submodulo_fenotipico(22.0, 5, 1.5)
escore_ing3 = calcular_submodulo_ingestao(60, 5, 1.5)
escore_infl3 = calcular_submodulo_inflamatorio(50, 3.2, 1.0)
escore_grav3 = calcular_submodulo_gravidade(1.5, 2.0, 55, 0)

print(f"Escores dos Submódulos:")
print(f"  - Fenotípico: {escore_feno3:.2f}")
print(f"  - Ingestão: {escore_ing3:.2f}")
print(f"  - Inflamatório: {escore_infl3:.2f}")
print(f"  - Gravidade: {escore_grav3:.2f}")
print()

escore_final3 = calcular_risco_final_integrado(escore_feno3, escore_ing3, escore_infl3, escore_grav3)
categoria3, cor3 = categorizar_risco(escore_final3)

print(f"Escore Final: {escore_final3:.2f}")
print(f"Categoria: {categoria3}")
print(f"ESPERADO: MODERADO ou BAIXO-MODERADO")
print()

if 40 <= escore_final3 <= 65:
    print("[OK] SUCESSO - Score no range esperado para moderado!")
else:
    print(f"[AVISO] Score {escore_final3:.2f} fora do range esperado (40-65)")
print()
print()

# Resumo
print("=" * 80)
print("RESUMO DOS TESTES")
print("=" * 80)
print(f"Caso 1 (Severo): {escore_final:.2f} - {categoria} {'[OK]' if escore_final >= 70 else '[FALHA]'}")
print(f"Caso 2 (Critico): {escore_final2:.2f} - {categoria2} {'[OK]' if escore_final2 >= 70 else '[FALHA]'}")
print(f"Caso 3 (Moderado): {escore_final3:.2f} - {categoria3} {'[OK]' if 40 <= escore_final3 <= 65 else '[AVISO]'}")
print("=" * 80)
