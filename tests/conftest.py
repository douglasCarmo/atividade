import pytest
from src.database import DatabaseManager
from src.validation import FlightValidationModule
from src.booking_service import BookingService

@pytest.fixture
def db_manager():
    """Fixture para criar um banco de dados SQLite em memória limpo a cada teste."""
    manager = DatabaseManager(":memory:")
    manager.connect()
    manager.create_tables()
    yield manager
    manager.close()

@pytest.fixture
def booking_service(db_manager):
    """Fixture que fornece a instância completa do serviço integrado."""
    validator = FlightValidationModule(db_manager)
    return BookingService(db_manager, validator)