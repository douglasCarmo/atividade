# Sistema de Agendamento de Helicópteros (AeroLog) - Testes de Integração

Projeto desenvolvido para validação prática das regras de negócio de agendamento de voos offshore e táxi aéreo com persistência em banco de dados SQLite.

## Estrutura do Projeto
- `src/database.py`: Gerenciamento e conexão com SQLite.
- `src/validation.py`: Validação de regras operacionais da aeronave.
- `src/booking_service.py`: Serviço central de agendamento.
- `tests/`: Suíte de testes de integração e fixtures do Pytest.

## Como Executar

1. Instalar dependências:
   ```bash
   pip install -r requirements.txt