from clinica import database, app
from clinica.models import Medico

with app.app_context():
    medico1 = Medico(nome="Dr. Luiz costa", especialidade="Clínica Geral", crm="123564-SP")
    medico2 = Medico(nome="Dra. Fernanda barros", especialidade="Pediatria", crm="633221-SP")
    medico3 = Medico(nome="Dr. Matheus ferreira", especialidade="Neurologia", crm="987894-SP")

    database.session.add_all([medico1, medico2, medico3])
    database.session.commit()

    print("Médicos adicionados com sucesso!")
