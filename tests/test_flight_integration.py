import pytest
from src.validation import FlightValidationError

def test_cenario_1_agendamento_valido_caminho_feliz(db_manager, booking_service):
    """Cenário 1: Solicitar agendamento com helicóptero liberado e horário disponível."""
    # Setup: Inserir aeronave LIBERADA
    aeronave_id = db_manager.execute_statement(
        "INSERT INTO aeronaves (codigo, modelo, status_manutencao) VALUES (?, ?, ?)",
        ("PR-AER", "Airbus H145", "LIBERADO")
    )
    data_hora = "2026-10-15T08:00:00"

    # Ação
    agendamento_id = booking_service.agendar_voo(aeronave_id, data_hora)

    # Validação
    res = db_manager.execute_query(
        "SELECT * FROM agendamentos WHERE id = ?", (agendamento_id,)
    )
    assert len(res) == 1
    assert res[0]["aeronave_id"] == aeronave_id
    assert res[0]["data_hora"] == data_hora
    assert res[0]["status"] == "AGENDADO"


def test_cenario_2_conflito_de_horario(db_manager, booking_service):
    """Cenário 2: Tentar agendar voo para helicóptero no mesmo horário já ocupado."""
    # Setup: Inserir aeronave e primeiro agendamento
    aeronave_id = db_manager.execute_statement(
        "INSERT INTO aeronaves (codigo, modelo, status_manutencao) VALUES (?, ?, ?)",
        ("PR-OFF", "Sikorsky S-92", "LIBERADO")
    )
    data_hora = "2026-10-15T10:00:00"
    booking_service.agendar_voo(aeronave_id, data_hora)

    # Ação e Validação de Exceção
    with pytest.raises(FlightValidationError) as exc_info:
        booking_service.agendar_voo(aeronave_id, data_hora)

    assert "já possui agendamento confirmado" in str(exc_info.value)

    # Validação de consistência do banco (somente 1 agendamento inserido)
    agendamentos = db_manager.execute_query(
        "SELECT * FROM agendamentos WHERE aeronave_id = ?", (aeronave_id,)
    )
    assert len(agendamentos) == 1


def test_cenario_3_aeronave_em_manutencao(db_manager, booking_service):
    """Cenário 3: Tentar agendar aeronave com status EM_INSPECAO."""
    # Setup: Aeronave em inspeção
    aeronave_id = db_manager.execute_statement(
        "INSERT INTO aeronaves (codigo, modelo, status_manutencao) VALUES (?, ?, ?)",
        ("PR-MNT", "AW139", "EM_INSPECAO")
    )
    data_hora = "2026-10-15T14:00:00"

    # Ação e Validação de Exceção
    with pytest.raises(FlightValidationError) as exc_info:
        booking_service.agendar_voo(aeronave_id, data_hora)

    assert "não está liberada para voo" in str(exc_info.value)

    # Validação: Nenhuma alteração registrada no banco
    agendamentos = db_manager.execute_query(
        "SELECT * FROM agendamentos WHERE aeronave_id = ?", (aeronave_id,)
    )
    assert len(agendamentos) == 0


def test_cenario_4_isolamento_de_banco_fixture_a(db_manager, booking_service):
    """Cenário 4 (Parte A): Insere registro para testar isolamento entre testes."""
    aeronave_id = db_manager.execute_statement(
        "INSERT INTO aeronaves (codigo, modelo, status_manutencao) VALUES (?, ?, ?)",
        ("PR-ISO1", "Bell 429", "LIBERADO")
    )
    booking_service.agendar_voo(aeronave_id, "2026-10-20T09:00:00")

    agendamentos = db_manager.execute_query("SELECT * FROM agendamentos")
    assert len(agendamentos) == 1


def test_cenario_4_isolamento_de_banco_fixture_b(db_manager):
    """Cenário 4 (Parte B): Garante que a base em memória foi resetada completamente."""
    agendamentos = db_manager.execute_query("SELECT * FROM agendamentos")
    aeronaves = db_manager.execute_query("SELECT * FROM aeronaves")

    assert len(agendamentos) == 0
    assert len(aeronaves) == 0