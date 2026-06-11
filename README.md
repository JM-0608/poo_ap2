# Simulador Copa do Mundo 2026 (Refatoração POO)

Este projeto é um simulador algorítmico do chaveamento e dos jogos da Copa do Mundo FIFA de 2026. O objetivo principal deste repositório é demonstrar a aplicação prática de diversos conceitos fundamentais de **Programação Orientada a Objetos (POO)** em Python, transformando um script procedural em uma arquitetura de software modular, limpa e expansível.

O sistema carrega os dados reais das seleções a partir de um arquivo CSV, organiza os grupos, simula resultados de partidas utilizando distribuições estatísticas (incluindo critérios de desempate e disputa de pênaltis) e avança pelas fases de grupos e mata-mata até a coroação do time campeão.

## 🛠️ Conceitos de POO Aplicados

O projeto foi inteiramente refatorado para contemplar os seguintes conceitos:

*   **Classes e Objetos (Instâncias):** Separação de responsabilidades em entidades lógicas (`Selecao`, `Grupo`, `Partida`).
*   **Atributos de Instância e de Classe:** Uso de atributos globais da classe (ex: contador `total_selecoes`) em contraste com o estado individual de cada objeto.
*   **Encapsulamento (`@property` e setters):** Proteção do estado interno das instâncias. Os atributos de classe usam a convenção de visibilidade privada (prefixo `_`) e são acessados/modificados de forma segura, garantindo regras de negócio durante atribuições.
*   **Métodos de Classe (`@classmethod`):** Implementação do padrão Factory Method (`from_dict`) para instanciar objetos `Selecao` a partir de dicionários brutos extraídos do CSV.
*   **Métodos Estáticos (`@staticmethod`):** Extração de lógicas utilitárias e independentes do estado do objeto (ex: `simular_gols()` na classe abstrata de partidas).
*   **Exceções Customizadas:** Criação de uma hierarquia de erros herdando de `Exception` (ex: `ArquivoNaoEncontradoError`, `NomeInvalidoError`) em conjunto com blocos `try/except` para tratamento robusto e semântico de falhas na leitura e validação dos dados.
*   **Método Mágico `__str__`:** Representação string customizada dos objetos para outputs amigáveis no console de instâncias de domínios.
*   **Classes Abstratas (ABC) e Polimorfismo:** Implementação do módulo `abc`. A superclasse abstrata `Partida` obriga suas filhas (`PartidaGrupo` e `PartidaMataMata`) a implementarem o método `jogar()`. O motor do jogo executa as partidas ignorando as particularidades de implementação (se acumula pontos ou se decide nos pênaltis), evidenciando o polimorfismo.

## 📁 Estrutura do Projeto

A arquitetura do código está dividida em domínios para facilitar a manutenção:

```text
poo_ap2/
│
├── domain/                      # Entidades de regra de negócio
│   ├── grupo.py                 # Gerencia coleções de seleções e tabela de classificação
│   ├── partida.py               # Motor abstrato e implementações concretas de jogos
│   └── selecao.py               # Molde principal contendo os dados dos times
│
├── exceptions/                  # Tratamento de erros
│   └── copa_exceptions.py       # Exceções customizadas para validações
│
├── main.py                      # Ponto de entrada (Entrypoint) e maestro do simulador
├── selecoes_copa_2026.csv       # Base de dados (Data source)
└── README.md                    # Documentação do projeto
```

## 🚀 Como Executar

### Pré-requisitos
*   **Python 3.8+** instalado na máquina.
*   O arquivo `selecoes_copa_2026.csv` deve estar presente no diretório raiz do projeto.

### Passos
1. Faça o clone do repositório ou baixe os arquivos para o seu computador.
2. Navegue via terminal até o diretório raiz do projeto (`poo_ap2`).
3. Execute o script principal:

```bash
python main.py
```

O console exibirá todo o andamento do campeonato, desde a fase de grupos, classificação detalhada, até as emocionantes disputas de pênaltis nas fases finais, coroando o grande campeão ao final da execução.

## 🎨 Frontend baseado no backend

Para abrir a interface visual:

1. Abra o arquivo `index.html` no navegador.
2. O CSS está em `styles.css`.
3. A tela é estática, mas foi desenhada para representar as entidades e o fluxo do backend em Python.

## Git: branch `dev` e merge em `main`

```bash
git checkout -b dev
git add index.html styles.css README.md
git commit -m "Refactor frontend to match backend"
git push -u origin dev
```

Depois, crie um Pull Request de `dev` para `main` no GitHub e finalize com merge. Se preferir pela linha de comando:

```bash
git checkout main
git pull origin main
git merge dev
git push origin main
```
