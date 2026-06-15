# Simulador Copa do Mundo 2026 🏆

Este projeto é um simulador interativo da Copa do Mundo 2026, desenvolvido em Python utilizando o framework **Flask** para a interface web. Ele permite gerenciar seleções e simular todo o torneio, desde a fase de grupos até a grande final.

## 🚀 Como Executar o Projeto

### 1. Pré-requisitos
Certifique-se de ter o Python instalado em sua máquina.

### 2. Instalar Dependências
O projeto utiliza o Flask para servir a interface web. Instale-o via pip:

```bash
pip install flask
```

### 3. Rodar a Aplicação
Execute o arquivo `app.py`:

```bash
python app.py
```

Após executar, abra o seu navegador e acesse:
**[http://localhost:5000](http://localhost:5000)**

---

## 📂 Funcionalidades

### 🎮 Simulador (Aba Principal)
*   **Botão Simular!**: Gera resultados aleatórios para todos os jogos da Copa.
*   **Fase de Grupos**: Exibe os placares e a tabela de classificação atualizada de cada grupo.
*   **Mata-Mata**: Mostra o chaveamento desde os 16-avos até a Final, incluindo disputa de 3º lugar e pênaltis em caso de empate.

### ⚙️ Gerenciamento (CRUD)
*   **Listar**: Visualize todas as seleções carregadas do arquivo `selecoes_copa_2026.csv`.
*   **Adicionar**: Insira novas seleções informando nome, sigla e grupo.
*   **Editar**: Altere o nome ou o grupo de uma seleção existente diretamente na tabela.
*   *As alterações são persistidas automaticamente no arquivo CSV.*

---

## 🏗️ Estrutura do Código (POO)
O projeto segue os pilares da Programação Orientada a Objetos:
*   **Encapsulamento**: Atributos protegidos nas classes `Selecao`, `Grupo` e `Partida`.
*   **Herança/Abstração**: Classe abstrata `Partida` com especializações `PartidaGrupo` e `PartidaMataMata`.
*   **Polimorfismo**: Diferentes comportamentos para o método `jogar()` dependendo da fase do torneio.
*   **Repositório**: Classe `RepositorioSelecao` isola a lógica de manipulação de arquivos (CSV).

---
*Desenvolvido para a disciplina de Programação Orientada a Objetos.*
