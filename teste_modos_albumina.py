"""
Script de Teste: Validação dos Modos COM e SEM Albumina
Compara resultados entre modo completo e simplificado
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from calculadora_desktop_albumina_opcional import (
    calcular_submodulo_fenotipico,
    calcular_submodulo_ingestao,
    calcular_submodulo_inflamatorio,
    calcular_submodulo_inflamatorio_simplificado,
    calcular_submodulo_gravidade,
    calcular_risco_final_integrado,
    categorizar_risco
)

print("=" * 90)
print("TESTE COMPARATIVO: MODO COMPLETO vs MODO SIMPLIFICADO")
print("=" * 90)
print()

# ==============================================================================
# CASO 1: Paciente com Risco Moderado
# ==============================================================================

print("CASO 1: PACIENTE COM RISCO MODERADO")
print("-" * 90)
print("Dados do paciente:")
print("  - IMC: 22.0, Perda ponderal: 5%, Sarcopenia: 1")
print("  - VET: 60%, Duracao: 5 dias, Sintomas GI: 1")
print("  - PCR: 50 mg/L, Albumina: 3.2 g/dL, Febre: 1 (subfebril)")
print("  - Diagnostico: 1, Comorbidades: 2, Idade: 55 anos, Cirurgia: 0")
print()

# Calcular submódulos comuns
esc_fen_1 = calcular_submodulo_fenotipico(22.0, 5, 1)
esc_ing_1 = calcular_submodulo_ingestao(60, 5, 1)
esc_grav_1 = calcular_submodulo_gravidade(1, 2, 55, 0)

# MODO COMPLETO (com albumina)
esc_inf_completo_1 = calcular_submodulo_inflamatorio(50, 3.2, 1)
esc_final_completo_1 = calcular_risco_final_integrado(
    esc_fen_1, esc_ing_1, esc_inf_completo_1, esc_grav_1, modo_completo=True
)
cat_completo_1, _ = categorizar_risco(esc_final_completo_1)

# MODO SIMPLIFICADO (sem albumina)
esc_inf_simples_1 = calcular_submodulo_inflamatorio_simplificado(50, 1)
esc_final_simples_1 = calcular_risco_final_integrado(
    esc_fen_1, esc_ing_1, esc_inf_simples_1, esc_grav_1, modo_completo=False
)
cat_simples_1, _ = categorizar_risco(esc_final_simples_1)

print("MODO COMPLETO (com albumina):")
print(f"  - Fenotipico: {esc_fen_1:.1f}, Ingestao: {esc_ing_1:.1f}, Inflamatorio: {esc_inf_completo_1:.1f}, Gravidade: {esc_grav_1:.1f}")
print(f"  - Escore Final: {esc_final_completo_1:.1f} - Categoria: {cat_completo_1}")
print()

print("MODO SIMPLIFICADO (sem albumina):")
print(f"  - Fenotipico: {esc_fen_1:.1f}, Ingestao: {esc_ing_1:.1f}, Inflamatorio: {esc_inf_simples_1:.1f}, Gravidade: {esc_grav_1:.1f}")
print(f"  - Escore Final: {esc_final_simples_1:.1f} - Categoria: {cat_simples_1}")
print()

# Análise
diferenca_inf_1 = abs(esc_inf_completo_1 - esc_inf_simples_1)
diferenca_final_1 = abs(esc_final_completo_1 - esc_final_simples_1)
concordancia_1 = "OK" if cat_completo_1 == cat_simples_1 else "DIVERGENTE"

print(f"ANALISE:")
print(f"  - Diferenca Inflam: {diferenca_inf_1:.1f} pontos")
print(f"  - Diferenca Final: {diferenca_final_1:.1f} pontos")
print(f"  - Concordancia de Categoria: {concordancia_1}")
print()
print()

# ==============================================================================
# CASO 2: Paciente Crítico (Alto Risco)
# ==============================================================================

print("CASO 2: PACIENTE CRITICO (ALTO RISCO)")
print("-" * 90)
print("Dados do paciente:")
print("  - IMC: 16.0, Perda ponderal: 15%, Sarcopenia: 3")
print("  - VET: 30%, Duracao: 14 dias, Sintomas GI: 2.5")
print("  - PCR: 150 mg/L, Albumina: 2.0 g/dL, Febre: 2.5 (febre alta)")
print("  - Diagnostico: 3, Comorbidades: 4, Idade: 75 anos, Cirurgia: 1")
print()

# Calcular submódulos comuns
esc_fen_2 = calcular_submodulo_fenotipico(16.0, 15, 3)
esc_ing_2 = calcular_submodulo_ingestao(30, 14, 2.5)
esc_grav_2 = calcular_submodulo_gravidade(3, 4, 75, 1)

# MODO COMPLETO (com albumina)
esc_inf_completo_2 = calcular_submodulo_inflamatorio(150, 2.0, 2.5)
esc_final_completo_2 = calcular_risco_final_integrado(
    esc_fen_2, esc_ing_2, esc_inf_completo_2, esc_grav_2, modo_completo=True
)
cat_completo_2, _ = categorizar_risco(esc_final_completo_2)

# MODO SIMPLIFICADO (sem albumina)
esc_inf_simples_2 = calcular_submodulo_inflamatorio_simplificado(150, 2.5)
esc_final_simples_2 = calcular_risco_final_integrado(
    esc_fen_2, esc_ing_2, esc_inf_simples_2, esc_grav_2, modo_completo=False
)
cat_simples_2, _ = categorizar_risco(esc_final_simples_2)

print("MODO COMPLETO (com albumina):")
print(f"  - Fenotipico: {esc_fen_2:.1f}, Ingestao: {esc_ing_2:.1f}, Inflamatorio: {esc_inf_completo_2:.1f}, Gravidade: {esc_grav_2:.1f}")
print(f"  - Escore Final: {esc_final_completo_2:.1f} - Categoria: {cat_completo_2}")
print()

print("MODO SIMPLIFICADO (sem albumina):")
print(f"  - Fenotipico: {esc_fen_2:.1f}, Ingestao: {esc_ing_2:.1f}, Inflamatorio: {esc_inf_simples_2:.1f}, Gravidade: {esc_grav_2:.1f}")
print(f"  - Escore Final: {esc_final_simples_2:.1f} - Categoria: {cat_simples_2}")
print()

# Análise
diferenca_inf_2 = abs(esc_inf_completo_2 - esc_inf_simples_2)
diferenca_final_2 = abs(esc_final_completo_2 - esc_final_simples_2)
concordancia_2 = "OK" if cat_completo_2 == cat_simples_2 else "DIVERGENTE"

print(f"ANALISE:")
print(f"  - Diferenca Inflam: {diferenca_inf_2:.1f} pontos")
print(f"  - Diferenca Final: {diferenca_final_2:.1f} pontos")
print(f"  - Concordancia de Categoria: {concordancia_2}")
print()
print()

# ==============================================================================
# CASO 3: Paciente Baixo Risco
# ==============================================================================

print("CASO 3: PACIENTE BAIXO RISCO")
print("-" * 90)
print("Dados do paciente:")
print("  - IMC: 24.0, Perda ponderal: 2%, Sarcopenia: 0")
print("  - VET: 85%, Duracao: 2 dias, Sintomas GI: 0")
print("  - PCR: 3 mg/L, Albumina: 4.0 g/dL, Febre: 0 (ausente)")
print("  - Diagnostico: 0, Comorbidades: 0, Idade: 45 anos, Cirurgia: 0")
print()

# Calcular submódulos comuns
esc_fen_3 = calcular_submodulo_fenotipico(24.0, 2, 0)
esc_ing_3 = calcular_submodulo_ingestao(85, 2, 0)
esc_grav_3 = calcular_submodulo_gravidade(0, 0, 45, 0)

# MODO COMPLETO (com albumina)
esc_inf_completo_3 = calcular_submodulo_inflamatorio(3, 4.0, 0)
esc_final_completo_3 = calcular_risco_final_integrado(
    esc_fen_3, esc_ing_3, esc_inf_completo_3, esc_grav_3, modo_completo=True
)
cat_completo_3, _ = categorizar_risco(esc_final_completo_3)

# MODO SIMPLIFICADO (sem albumina)
esc_inf_simples_3 = calcular_submodulo_inflamatorio_simplificado(3, 0)
esc_final_simples_3 = calcular_risco_final_integrado(
    esc_fen_3, esc_ing_3, esc_inf_simples_3, esc_grav_3, modo_completo=False
)
cat_simples_3, _ = categorizar_risco(esc_final_simples_3)

print("MODO COMPLETO (com albumina):")
print(f"  - Fenotipico: {esc_fen_3:.1f}, Ingestao: {esc_ing_3:.1f}, Inflamatorio: {esc_inf_completo_3:.1f}, Gravidade: {esc_grav_3:.1f}")
print(f"  - Escore Final: {esc_final_completo_3:.1f} - Categoria: {cat_completo_3}")
print()

print("MODO SIMPLIFICADO (sem albumina):")
print(f"  - Fenotipico: {esc_fen_3:.1f}, Ingestao: {esc_ing_3:.1f}, Inflamatorio: {esc_inf_simples_3:.1f}, Gravidade: {esc_grav_3:.1f}")
print(f"  - Escore Final: {esc_final_simples_3:.1f} - Categoria: {cat_simples_3}")
print()

# Análise
diferenca_inf_3 = abs(esc_inf_completo_3 - esc_inf_simples_3)
diferenca_final_3 = abs(esc_final_completo_3 - esc_final_simples_3)
concordancia_3 = "OK" if cat_completo_3 == cat_simples_3 else "DIVERGENTE"

print(f"ANALISE:")
print(f"  - Diferenca Inflam: {diferenca_inf_3:.1f} pontos")
print(f"  - Diferenca Final: {diferenca_final_3:.1f} pontos")
print(f"  - Concordancia de Categoria: {concordancia_3}")
print()
print()

# ==============================================================================
# CASO 4: Caso Reportado pelo Usuário (teste de regressão)
# ==============================================================================

print("CASO 4: CASO REPORTADO PELO USUARIO (Regressao)")
print("-" * 90)
print("Dados do paciente:")
print("  - IMC: 19, Perda ponderal: 5%, Sarcopenia: 0")
print("  - VET: 50%, Duracao: 5 dias, Sintomas GI: 0")
print("  - PCR: 6 mg/L, Albumina: 2.8 g/dL, Febre: 1 (subfebril)")
print("  - Diagnostico: 0, Comorbidades: 0, Idade: 60 anos, Cirurgia: 0")
print()

# Calcular submódulos comuns
esc_fen_4 = calcular_submodulo_fenotipico(19, 5, 0)
esc_ing_4 = calcular_submodulo_ingestao(50, 5, 0)
esc_grav_4 = calcular_submodulo_gravidade(0, 0, 60, 0)

# MODO COMPLETO (com albumina)
esc_inf_completo_4 = calcular_submodulo_inflamatorio(6, 2.8, 1)
esc_final_completo_4 = calcular_risco_final_integrado(
    esc_fen_4, esc_ing_4, esc_inf_completo_4, esc_grav_4, modo_completo=True
)
cat_completo_4, _ = categorizar_risco(esc_final_completo_4)

# MODO SIMPLIFICADO (sem albumina)
esc_inf_simples_4 = calcular_submodulo_inflamatorio_simplificado(6, 1)
esc_final_simples_4 = calcular_risco_final_integrado(
    esc_fen_4, esc_ing_4, esc_inf_simples_4, esc_grav_4, modo_completo=False
)
cat_simples_4, _ = categorizar_risco(esc_final_simples_4)

print("MODO COMPLETO (com albumina):")
print(f"  - Fenotipico: {esc_fen_4:.1f}, Ingestao: {esc_ing_4:.1f}, Inflamatorio: {esc_inf_completo_4:.1f}, Gravidade: {esc_grav_4:.1f}")
print(f"  - Escore Final: {esc_final_completo_4:.1f} - Categoria: {cat_completo_4}")
print()

print("MODO SIMPLIFICADO (sem albumina):")
print(f"  - Fenotipico: {esc_fen_4:.1f}, Ingestao: {esc_ing_4:.1f}, Inflamatorio: {esc_inf_simples_4:.1f}, Gravidade: {esc_grav_4:.1f}")
print(f"  - Escore Final: {esc_final_simples_4:.1f} - Categoria: {cat_simples_4}")
print()

# Análise
diferenca_inf_4 = abs(esc_inf_completo_4 - esc_inf_simples_4)
diferenca_final_4 = abs(esc_final_completo_4 - esc_final_simples_4)
concordancia_4 = "OK" if cat_completo_4 == cat_simples_4 else "DIVERGENTE"

print(f"ANALISE:")
print(f"  - Diferenca Inflam: {diferenca_inf_4:.1f} pontos")
print(f"  - Diferenca Final: {diferenca_final_4:.1f} pontos")
print(f"  - Concordancia de Categoria: {concordancia_4}")
print()
print()

# ==============================================================================
# RESUMO GERAL
# ==============================================================================

print("=" * 90)
print("RESUMO GERAL DOS TESTES")
print("=" * 90)

diferenca_media_inf = (diferenca_inf_1 + diferenca_inf_2 + diferenca_inf_3 + diferenca_inf_4) / 4
diferenca_media_final = (diferenca_final_1 + diferenca_final_2 + diferenca_final_3 + diferenca_final_4) / 4

concordancias = [concordancia_1, concordancia_2, concordancia_3, concordancia_4]
taxa_concordancia = (concordancias.count("OK") / len(concordancias)) * 100

print(f"\nDiferenca Media Escore Inflamatorio: {diferenca_media_inf:.1f} pontos")
print(f"Diferenca Media Escore Final: {diferenca_media_final:.1f} pontos")
print(f"Taxa de Concordancia de Categoria: {taxa_concordancia:.0f}% ({concordancias.count('OK')}/{len(concordancias)} casos)")
print()

print("Detalhamento:")
print(f"  - Caso 1 (Moderado): Diferenca {diferenca_final_1:.1f} pts - {concordancia_1}")
print(f"  - Caso 2 (Critico):  Diferenca {diferenca_final_2:.1f} pts - {concordancia_2}")
print(f"  - Caso 3 (Baixo):    Diferenca {diferenca_final_3:.1f} pts - {concordancia_3}")
print(f"  - Caso 4 (Usuario):  Diferenca {diferenca_final_4:.1f} pts - {concordancia_4}")
print()

# Validação final
if taxa_concordancia >= 75 and diferenca_media_final <= 15:
    print("[SUCESSO] Sistema validado! Modo simplificado tem performance aceitavel.")
    print("          - Concordancia >= 75%")
    print("          - Diferenca media <= 15 pontos")
else:
    print("[ATENCAO] Sistema precisa de ajustes.")
    if taxa_concordancia < 75:
        print(f"          - Concordancia {taxa_concordancia:.0f}% < 75%")
    if diferenca_media_final > 15:
        print(f"          - Diferenca media {diferenca_media_final:.1f} > 15 pontos")

print()
print("=" * 90)
