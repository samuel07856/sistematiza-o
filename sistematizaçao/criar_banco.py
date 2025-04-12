from clinica import database, app
from clinica.models import Usuario, Medico, Agendamento  # <-- Aqui está a diferença!

with app.app_context():
    database.create_all()
