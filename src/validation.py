class FlightValidationError(Exception):
    """Exceção lançada quando um agendamento fere as regras de negócio."""
    pass

class FlightValidationModule:
    """Aplica as regras de elegibilidade operacional da AeroLog."""

    def __init__(self, db_manager):
        self.db_manager = db_manager

    def validar_aeronave_liberada(self, aeronave_id: int) -> None:
        """Verifica se a aeronave possui status LIBERADO."""
        query = "SELECT status_manutencao FROM aeronaves WHERE id = ?"
        resultado = self.db_manager.execute_query(query, (aeronave_id,))

        if not resultado:
            raise FlightValidationError(f"Aeronave ID {aeronave_id} não encontrada.")

        status = resultado[0]["status_manutencao"]
        if status != "LIBERADO":
            raise FlightValidationError(
                f"Aeronave não está liberada para voo. Status atual: {status}"
            )

    def validar_conflito_horario(self, aeronave_id: int, data_hora: str) -> None:
        """Verifica se a aeronave já possui missão cadastrada no mesmo horário."""
        query = """
            SELECT id FROM agendamentos 
            WHERE aeronave_id = ? AND data_hora = ? AND status = 'AGENDADO'
        """
        resultado = self.db_manager.execute_query(query, (aeronave_id, data_hora))

        if resultado:
            raise FlightValidationError(
                f"Aeronave ID {aeronave_id} já possui agendamento confirmado em {data_hora}."
            )

    def validar_agendamento(self, aeronave_id: int, data_hora: str) -> None:
        """Executa a suíte de validações para o agendamento."""
        self.validar_aeronave_liberada(aeronave_id)
        self.validar_conflito_horario(aeronave_id, data_hora)