# 🎮 SenacMon - Jogo de Tabuleiro Pokémon

![Python](https://img.shields.io/badge/Python-3.14-blue)
![Django](https://img.shields.io/badge/Django-5.x-green)
![License](https://img.shields.io/badge/License-MIT-yellow)

SenacMon é um jogo de tabuleiro inspirado em Pokémon, combinando mecânicas de rolagem de dados, batalhas estratégicas e apostas. Desenvolvido como projeto educacional usando Django e Python.

## 📋 Índice

- [Sobre o Projeto](#sobre-o-projeto)
- [Funcionalidades](#funcionalidades)
- [Tecnologias Utilizadas](#tecnologias-utilizadas)
- [Instalação](#instalação)
- [Como Jogar](#como-jogar)
- [Estrutura do Projeto](#estrutura-do-projeto)
- [Mecânicas do Jogo](#mecânicas-do-jogo)
- [Roadmap](#roadmap)
- [Contribuindo](#contribuindo)

## 🎯 Sobre o Projeto

SenacMon é um jogo roguelike de tabuleiro onde você escolhe um Pokémon inicial e percorre um mapa enfrentando batalhas, coletando berries (moeda do jogo) e evitando a captura pela Equipe Rocket. O objetivo é completar o máximo de rodadas possível maximizando seus ganhos.

### 🎲 Conceito Principal

- **Tabuleiro Circular**: Movimento baseado em rolagem de dados
- **Sistema de Apostas**: Aposte em números durante batalhas para multiplicar ganhos
- **Gestão de Recursos**: Administre seus berries para sobreviver até o final
- **Elementos Pokémon**: Sistema de vantagem/desvantagem baseado em tipos

## ✨ Funcionalidades

### MVP Completo ✅

- ✅ Sistema de autenticação de usuários
- ✅ Seleção de Pokémon inicial
- ✅ Tabuleiro com 5 tipos de zonas:
  - 🎲 **Batalha**: Enfrente Pokémon selvagens
  - 💰 **Bônus**: Ganhe berries extras
  - 💸 **Perda**: Perca berries
  - 🚨 **Captura**: Equipe Rocket te prende por 2 rodadas
  - 😐 **Neutra**: Nada acontece
- ✅ Sistema de batalhas com apostas
- ✅ Mecânica de vantagem elemental
- ✅ Sistema de carteira (wallet) para gerenciar berries
- ✅ Histórico detalhado de eventos
- ✅ Resumo final de partida com estatísticas
- ✅ Validação de batalhas pendentes
- ✅ Encerramento automático (rodadas ou saldo zerado)

### 🎯 Próximas Funcionalidades

**Fase 1: Experiência do Usuário**
- Interface visual do tabuleiro (canvas/SVG)
- Animações de rolagem de dado
- Sprites dos Pokémon nas telas
- Sons e efeitos visuais
- Tutorial interativo

**Fase 2: Gamificação**
- Sistema de conquistas
- Ranking global
- Histórico de partidas
- Níveis de dificuldade
- Sistema de progressão

**Fase 3: Social e Competitivo**
- Modo multiplayer
- Compartilhamento social
- Torneios e eventos
- Sistema de clãs
- Chat entre jogadores

## 🛠️ Tecnologias Utilizadas

### Backend
- **Python 3.14**
- **Django 5.x** - Framework web
- **SQLite** - Banco de dados (desenvolvimento)
- **Django Admin** - Interface administrativa

### Estrutura
- **MTV Pattern** (Model-Template-View)
- **Service Layer** - Lógica de negócio separada
- **Domain-Driven Design** - Organização por domínios

## 🚀 Instalação

### Pré-requisitos

- Python 3.14+
- pip
- virtualenv (recomendado)

### Passo a Passo

1. **Clone o repositório**
```bash
git clone https://github.com/seu-usuario/senacmon.git
cd senacmon
```

2. **Crie e ative o ambiente virtual**
```bash
python -m venv .venv

# Windows
.venv\Scripts\activate

# Linux/Mac
source .venv/bin/activate
```

3. **Instale as dependências**
```bash
pip install -r requirements/requirements.txt
```

4. **Execute as migrações**
```bash
cd src
python manage.py migrate
```

5. **Carregue os dados iniciais**
```bash
python manage.py seed_senacmon
python manage.py seed_extras_senacmon
```

6. **Crie um superusuário (opcional)**
```bash
python manage.py createsuperuser
```

7. **Inicie o servidor**
```bash
python manage.py runserver
```

8. **Acesse o jogo**
```
http://localhost:8000
```

## 🎮 Como Jogar

### 1. Registro e Login
- Crie sua conta ou faça login
- Acesse a página inicial

### 2. Iniciar Partida
- Clique em "🎮 Nova Partida"
- Escolha seu Pokémon inicial (Fogo, Água ou Planta)
- Defina os berries iniciais e limite de rodadas

### 3. Gameplay

#### Rolagem de Dados
- Clique em "🎲 Rolar Dado" para se mover pelo tabuleiro
- Você avançará de 1 a 6 casas

#### Zonas do Tabuleiro
- **💰 Bônus**: Receba berries gratuitamente
- **💸 Perda**: Perca berries
- **🚨 Captura**: Fique 2 rodadas sem jogar
- **😐 Neutra**: Continue jogando
- **⚔️ Batalha**: Enfrente um Pokémon selvagem

#### Sistema de Batalha
1. Um Pokémon aleatório aparece
2. Escolha 1 ou 2 números (0-9)
3. Defina o valor da aposta (ou 0 para simular)
4. Um número aleatório é sorteado
5. Se acertar, ganhe berries multiplicados!

#### Multiplicadores
- **1 número**: 2.8x base
- **2 números**: 1.3x base
- **Vantagem elemental**: +50% no multiplicador
- **Desvantagem elemental**: -50% no multiplicador

### 4. Fim de Partida

A partida encerra quando:
- Atingir o limite de rodadas
- Ficar sem berries
- Abandonar a partida

Visualize seu resumo final com:
- Total de rodadas jogadas
- Vitórias e derrotas
- Lucro/prejuízo
- Posição final

## 📁 Estrutura do Projeto

```
senacmon/
├── src/
│   ├── accounts/           # Autenticação e perfis
│   ├── common/             # Código compartilhado
│   │   ├── management/
│   │   │   └── commands/   # Comandos de seed
│   │   └── utils/          # Utilitários (RNG)
│   ├── config/             # Configurações Django
│   ├── game/               # Lógica principal do jogo
│   │   ├── admin/          # Interface admin customizada
│   │   ├── domain/         # Regras de negócio
│   │   │   ├── dto.py      # Data Transfer Objects
│   │   │   ├── excecoes.py # Exceções customizadas
│   │   │   ├── regras.py   # Regras do jogo
│   │   │   └── validadores.py
│   │   ├── models/         # Modelos do banco
│   │   │   ├── batalha.py
│   │   │   ├── eventos.py
│   │   │   ├── mapa.py
│   │   │   ├── partida.py
│   │   │   └── pokemon.py
│   │   ├── services/       # Lógica de negócio
│   │   │   ├── aposta_service.py
│   │   │   ├── batalha_service.py
│   │   │   ├── mapa_service.py
│   │   │   ├── partida_service.py
│   │   │   └── zona_service.py
│   │   └── views/          # Controllers
│   │       ├── abandon.py
│   │       ├── battle.py
│   │       ├── roll.py
│   │       ├── start.py
│   │       └── state.py
│   ├── wallet/             # Sistema de moedas
│   ├── static/             # Arquivos estáticos
│   └── templates/          # Templates HTML
├── requirements/           # Dependências
└── README.md
```

## 🎲 Mecânicas do Jogo

### Sistema de RNG (Random Number Generator)
- Seed determinística: `hash(partida_id + rodada_atual)`
- Garante reprodutibilidade e auditoria
- Evita manipulação de resultados

### Sistema Elemental
```
Fogo > Planta > Água > Fogo
```

**Vantagens:**
- Vantagem: +50% multiplicador
- Neutro: multiplicador normal
- Desvantagem: -50% multiplicador

### Sistema de Apostas

#### Aposta Simples (1 número)
- Custo mínimo: 5 berries
- Multiplicador base: 2.8x
- Chance: 10% (1/10)

#### Aposta Dupla (2 números)
- Custo mínimo: 8 berries
- Multiplicador base: 1.3x
- Chance: 20% (2/10)

### Captura pela Equipe Rocket
- Duração: 2 rodadas sem jogar
- Não perde berries durante captura
- As rodadas capturadas contam no limite total

## 📊 Roadmap

### ✅ MVP (Concluído)
- [x] Sistema base do jogo
- [x] Batalhas e apostas
- [x] Sistema de wallet
- [x] Histórico de eventos
- [x] Resumo final

### 🚧 Em Desenvolvimento
- [ ] Interface visual do tabuleiro
- [ ] Animações e efeitos
- [ ] Sistema de conquistas

### 📅 Planejado
- [ ] Modo multiplayer
- [ ] Ranking global
- [ ] Torneios e eventos
- [ ] Sistema social

## 🤝 Contribuindo

Contribuições são bem-vindas! Para contribuir:

1. Fork o projeto
2. Crie uma branch para sua feature (`git checkout -b feature/AmazingFeature`)
3. Commit suas mudanças (`git commit -m 'Add some AmazingFeature'`)
4. Push para a branch (`git push origin feature/AmazingFeature`)
5. Abra um Pull Request

### Padrões de Código

- Siga PEP 8 para Python
- Use type hints quando possível
- Escreva docstrings para funções complexas
- Mantenha a separação de responsabilidades (services, models, views)

## 📝 Licença

Este projeto está sob a licença MIT. Veja o arquivo `LICENSE` para mais detalhes.

## 👥 Autores

- **Equipe SenacMon** - Projeto Educacional

## 🙏 Agradecimentos

- SENAC pela oportunidade de aprendizado
- Comunidade Pokémon pela inspiração
- Django pela excelente documentação

---

**Divirta-se jogando SenacMon! 🎮✨**

Para reportar bugs ou sugerir features, abra uma [issue](https://github.com/lpjunior/senacmon/issues).
