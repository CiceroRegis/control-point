# # Create your tests here.
# import unittest

# from django.contrib.auth.models import User

# from collaborator.models import Profile
# from patient.models import Patient


# class PacientesEusuarios(unittest.TestCase):

#     def setUp(self):
#         # """User"""
#         # self.user1 = User.objects.create_user(first_name='usuario Teste1',
#         #                                       username='usuarioteste1',
#         #                                       is_staff='1',
#         #                                       email=None,
#         #                                       password='admin')
#         #
#         # self.user2 = User.objects.create_user(first_name='usuario Teste2',
#         #                                       username='usuarioteste2',
#         #                                       is_staff='1',
#         #                                       email=None,
#         #                                       password='admin')
#         #
#         # self.user3 = User.objects.create_user(first_name='usuario Teste3',
#         #                                       username='usuarioteste3',
#         #                                       is_staff='1',
#         #                                       email=None,
#         #                                       password='admin')
#         #
#         # """Profile"""
#         # self.profile = Profile.objects.create(user_id='22',
#         #                                       nome='admin',
#         #                                       )

#         """Patient"""
#         self.pacient1 = Patient.objects.create(name='patient 1',
#                                                email='ciceroregis25@mail.com',
#                                                date_of_birth='2020-03-20',
#                                                sexo='M')

#         self.pacient2 = Patient.objects.create(name='patient 2',
#                                                email='ciceroregis25@mail.com',
#                                                date_of_birth='2020-03-20',
#                                                sexo='M')

#         self.pacient3 = Patient.objects.create(name='patient 3',
#                                                email='ciceroregis25@mail.com',
#                                                date_of_birth='2020-03-20',
#                                                sexo='M')
#         self.pacient4 = Patient.objects.create(name='patient 4',
#                                                email='ciceroregis25@mail.com',
#                                                date_of_birth='2020-03-20',
#                                                sexo='M')

#         self.pacient5 = Patient.objects.create(name='patient 5',
#                                                email='ciceroregis25@mail.com',
#                                                date_of_birth='2020-03-20',
#                                                sexo='M')

#         # print('User', self.users)
#         print('pacient1', self.pacient1)
#         print('pacient2', self.pacient2)
#         print('pacient3', self.pacient3)
#         print('pacient4', self.pacient4)
#         print('pacient5', self.pacient5)

#     def test_lista_dados_pacient_usuario(self):
#         self.user = Profile.objects.all()

#         if self.user:
#             print('usuarios', self.user)
