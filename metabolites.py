# -*- coding: ascii -*-
# ==============================================================================
# Script: metabolitos.py
# Descricao: Rotina automatizada para deteccao de picos e anotacao de
#            metabolitos primarios e secundarios em espectros de RMN (TopSpin).
# Autora: Debora Fioravante da Silveira
# Afiliacao: Universidade Federal de Santa Maria (UFSM)
# Ano: 2026
# Licenca: CC BY-NC 4.0 (Atribuicao-NaoComercial 4.0 Internacional)
# ==============================================================================

import os
import re

# ==========================================================
# CONFIGURACOES (Ajuste o caminho da tabela CSV abaixo)
# ==========================================================
CAMINHO_CSV = "data/metabolitos.csv"  # Exemplo Windows: "C:/Users/debor/Downloads/metabolitos.csv"
TOL_IDEAL = 0.02                      # Tolerancia ideal para 1H (ppm)
TOL_MAX   = 0.05                      # Tolerancia maxima para 1H (ppm)
# ==========================================================

def carregar_metabolitos(caminho):
    metabolitos = []
    if not os.path.exists(caminho):
        MSG("Arquivo CSV nao encontrado em:\n" + caminho)
        return None
    f = open(caminho, 'r')
    linhas = f.readlines()
    f.close()
    for i, linha in enumerate(linhas):
        linha = linha.strip()
        if not linha or i == 0:
            continue
        sep = ';' if ';' in linha else ','
        partes = linha.split(sep)
        if len(partes) >= 2:
            nome = partes[0].strip()
            try:
                ppm = float(partes[1].strip().replace(',', '.'))
                metabolitos.append((nome, ppm))
            except:
                pass
    return metabolitos

curdat = CURDATA()
if not curdat:
    MSG("Abra um espectro processado (1r) antes de executar.")
    EXIT()

metabolitos = carregar_metabolitos(CAMINHO_CSV)

if metabolitos:
    exp_dir = os.path.join(curdat[3], curdat[0], curdat[1], "pdata", curdat[2])
    xml_path = os.path.join(exp_dir, "peaklist.xml")

    # 1. Executa o peak picking nativo do TopSpin
    XCMD("delp")
    XCMD("pp")

    if not os.path.exists(xml_path):
        MSG("Nenhum pico detectado. Diminua o parametro MI em 'edp' e tente novamente.")
        EXIT()

    f_xml = open(xml_path, 'r')
    conteudo_xml = f_xml.read()
    f_xml.close()

    encontrados = 0

    def buscar_metabolito(ppm_pico):
        melhor = None
        menor_diff = TOL_MAX + 1.0
        for nome, ppm_ref in metabolitos:
            diff = abs(ppm_pico - ppm_ref)
            if diff <= TOL_IDEAL and diff < menor_diff:
                menor_diff = diff
                melhor = nome
        if not melhor:
            for nome, ppm_ref in metabolitos:
                diff = abs(ppm_pico - ppm_ref)
                if diff <= TOL_MAX and diff < menor_diff:
                    menor_diff = diff
                    melhor = nome
        return melhor

    def anotar_tag(match):
        global encontrados
        tag = match.group(0)
        m_f1 = re.search(r'F1="([^"]+)"', tag)
        if not m_f1:
            return tag
        nome_match = buscar_metabolito(float(m_f1.group(1)))
        if nome_match:
            encontrados += 1
            tag_limpa = re.sub(r'\s*annotation="[^"]*"', '', tag)
            if tag_limpa.endswith('/>'):
                return tag_limpa[:-2] + ' annotation="' + nome_match + '"/>'
            return tag_limpa[:-1] + ' annotation="' + nome_match + '">'
        return tag

    novo_xml = re.sub(r'<Peak1D\b[^>]*>', anotar_tag, conteudo_xml)

    f_out = open(xml_path, 'w')
    f_out.write(novo_xml)
    f_out.close()

    # 2. Forca o TopSpin a importar o peaklist.xml modificado para a interface
    CLOSEWIN(curdat)
    RE(curdat)
    XCMD("peaks")
    XCMD("peaklist_import")

    MSG("Concluido! Metabolitos preenchidos em Annotation: " + str(encontrados))