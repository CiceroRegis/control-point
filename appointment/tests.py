# import unittest
# from datetime import datetime

# from django.contrib.auth.models import User

# from appointment.models import Appointment, TypeAppointment
# from collaborator.models import Profile


# class ShowtotalPrice(unittest.TestCase):

#     def setUp(self):
#         self.type_appointment = TypeAppointment.objects.create(name='')

#     # def test_show_total_price(self):
#     #     appointments_price_total = Appointment.objects.values('type_appointment__price').annotate(
#     #         Count('type_appointment__price')).annotate(total=Sum('type_appointment__price'))
#     #     for app in appointments_price_total:
#     #         print("preço total: ", app)
#     #     return

#     # def test_listar_agendamentos_proximos_a_data_atual(self):
#     #     appointments = Appointment.objects.all().annotate(
#     #         total=Sum('type_appointment__price')).order_by(
#     #         '-date_appointment')
#     #     for app in appointments:
#     #         print('agendamentos do dia:', app.patient, "no dia:", app.date_appointment)

#     # def test_mostrar_total_de_consultas_agendadas(self):
#     #     appointments = Appointment.objects.all().count()
#     #     print('total de consultas:', appointments)

#     def test_listar_agendamentos_proximos_a_data_atual(self):
#         appointments = Appointment.objects.filter(date_appointment__lt=datetime.today())
#         for app in appointments:
#             print('agendamentos do dia:', app.pacient, "no dia:", app.date_appointment.strftime("%d-%m-%Y %H:%M:%S"))
