"""
Teste para reproduzir erro reportado pelo usuário
Valores: IMC=19, perda=5, VET=50, duracao=5, PCR=6, albumina=2.8, idade=60, subfebril=1
"""

import sys
import os
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
print("TESTE DO CASO REPORTADO PELO USUÁRIO")
print("=" * 80)
print()
print("Valores de entrada:")
print("  - IMC: 19")
print("  - Perda ponderal: 5%")
print("  - Sarcopenia: 0 (não especificado, assumindo 0)")
print("  - VET: 50%")
print("  - Duração do déficit: 5 dias")
print("  - Sintomas GI: 0 (não especificado, assumindo 0)")
print("  - PCR: 6 mg/L")
print("  - Albumina: 2.8 g/dL")
print("  - Febre/Estado subfebril: 1 ponto")
print("  - Diagnóstico: 0 (não especificado, assumindo 0)")
print("  - Comorbidades: 0 (não especificado, assumindo 0)")
print("  - Idade: 60 anos")
print("  - Cirurgia: 0 (não especificado, assumindo não)")
print()

try:
    print("Calculando submodulo FENOTIPICO...")
    escore_feno = calcular_submodulo_fenotipico(19, 5, 0)
    print(f"  OK Fenotipico: {escore_feno:.2f}")
except Exception as e:
    print(f"  ERRO no Fenotipico: {e}")
    import traceback
    traceback.print_exc()

try:
    print("Calculando submodulo INGESTAO...")
    escore_ing = calcular_submodulo_ingestao(50, 5, 0)
    print(f"  OK Ingestao: {escore_ing:.2f}")
except Exception as e:
    print(f"  ERRO no Ingestao: {e}")
    import traceback
    traceback.print_exc()

try:
    print("Calculando submodulo INFLAMATORIO...")
    escore_infl = calcular_submodulo_inflamatorio(6, 2.8, 1)
    print(f"  OK Inflamatorio: {escore_infl:.2f}")
except Exception as e:
    print(f"  ERRO no Inflamatorio: {e}")
    import traceback
    traceback.print_exc()

try:
    print("Calculando submodulo GRAVIDADE...")
    escore_grav = calcular_submodulo_gravidade(0, 0, 60, 0)
    print(f"  OK Gravidade: {escore_grav:.2f}")
except Exception as e:
    print(f"  ERRO no Gravidade: {e}")
    import traceback
    traceback.print_exc()

print()
print("Calculando ESCORE FINAL integrado...")
try:
    escore_final = calcular_risco_final_integrado(escore_feno, escore_ing, escore_infl, escore_grav)
    print(f"  OK Escore Final: {escore_final:.2f}")

    categoria, cor = categorizar_risco(escore_final)
    print(f"  OK Categoria: {categoria}")
    print()
    print("[SUCESSO] Calculo concluido sem erros!")

except Exception as e:
    print(f"  ERRO ao calcular escore final: {e}")
    print()
    print("[ERRO IDENTIFICADO]")
    import traceback
    traceback.print_exc()

print()
print("=" * 80)
