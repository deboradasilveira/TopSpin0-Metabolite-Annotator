# Anotação Automatizada de Metabólitos de Soja (*Glycine max*) por RMN de ¹H

[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.24290248.svg)](https://doi.org/10.5281/zenodo.24290248)
[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](https://opensource.org/licenses/MIT)
[![Python](https://img.shields.io/badge/Python-3.x-blue.svg)](https://www.python.org/)
[![Bruker TopSpin](https://img.shields.io/badge/Bruker%20TopSpin-4.5.0-005A9C.svg)](https://www.bruker.com/)

Pipeline e scripts em Python desenvolvidos para automatizar a identificação, anotação espectral (`peaklist.xml`) e construção de matrizes de dados de metabólitos primários e secundários de soja (*Glycine max*) a partir de espectros processados de Ressonância Magnética Nuclear de Hidrogênio (RMN de ¹H) no **Bruker TopSpin 4.5.0**.

---

## 📋 Funcionalidades

* **Anotação por tolerância de deslocamento químico ($\delta$):** Compara os sinais espectrais com uma biblioteca de referência (`metabolitos.csv`) dentro de uma janela configurável (0,02 a 0,05 ppm).
* **Integração com Bruker TopSpin 4.5.0:** Leitura direta dos arquivos espectrais processados (`1r` e `procs`) e geração automática de listas de picos compatíveis com o esquema XML nativo do TopSpin (`peaklist.xml`) para rotulagem visual nos espectros.
* **Geração de Matriz Quimiométrica:** Consolidação automática das intensidades/áreas dos metabólitos anotados em tabela (`matriz_metabolitos_soja.csv`), pronta para análises multivariadas (PCA, PLS-DA) no SOLO / PLS_Toolbox.

---

## 🗂️ Estrutura do Repositório

```text
├── scripts/                  # Scripts Python para leitura de espectros e geração de XML/CSV
├── data/
│   └── metabolitos.csv       # Tabela de referência com deslocamentos químicos (ppm) de metabólitos de soja
├── CITATION.cff              # Metadados padronizados para citação acadêmica
├── LICENSE                   # Licença MIT
└── README.md                 # Documentação do projeto