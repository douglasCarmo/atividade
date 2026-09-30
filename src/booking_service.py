from src.database import DatabaseManager
from src.validation import FlightValidationModule, FlightValidationError

class BookingService:
    """Orquestra as validações e persiste o agendamento de voos."""

    def __init__(self, db_manager: DatabaseManager, validator: FlightValidationModule):
        self.db_manager = db_manager
        self.validator = validator

    def agendar_voo(self, aeronave_id: int, data_hora: str) -> int:
        """Valida e registra um novo agendamento com o status AGENDADO."""
        # Executa validações de negócio
        self.validator.validar_agendamento(aeronave_id, data_hora)

        # Persistência no banco de dados
        query = """
            INSERT INTO agendamentos (aeronave_id, data_hora, status)
            VALUES (?, ?, 'AGENDADO')
        """
        agendamento_id = self.db_manager.execute_statement(query, (aeronave_id, data_hora))
        return agendamento_id