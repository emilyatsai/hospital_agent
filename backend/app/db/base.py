# Import all the models, so that Base has them before being
# imported by Alembic
from app.db.base_class import Base  # noqa
from app.models.user import User  # noqa
from app.models.patient import Patient  # noqa
from app.models.doctor import Doctor  # noqa
from app.models.appointment import Appointment  # noqa
from app.models.medical_record import MedicalRecord  # noqa
from app.models.ai_insight import AIInsight  # noqa