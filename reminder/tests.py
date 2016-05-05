from django.test import TestCase

import datetime

from reminder.models import DoctorProfile, PatientProfile, LogHistory


# Create your tests here.
class DoctorMethodTests(TestCase):
    def test_ensure_num_of_patients_are_positive(self):
        '''
        test_ensure_num_of_patients_are_positive should results True 
        for Doctor where num_of_patients are zero or positive
        '''
        doctor = DoctorProfile(username='test_num_of_patients', is_doctor=True, num_of_patients=-1)
        doctor.save()
        self.assertEqual(doctor.is_doctor, True)
        self.assertEqual((doctor.num_of_patients>=0), True)

    def test_default_is_doctor(self):
        '''
        test_default_is_doctor should results True for Doctor where is_doctor is default.
        '''
        doctor = DoctorProfile(username='test_is_doctor')
        doctor.save()
        self.assertEqual(doctor.is_doctor, False)
        self.assertEqual((doctor.num_of_patients>=0), True)

class PatientMethodTests(TestCase):
    def test_null_dob_email_cell(self):
        '''
        test_null_dob_email_cell should results True for NULL date_of_birth, email and cell_phone.
        '''
        doctor = DoctorProfile(username='test_doctor')
        doctor.save()
        patient = PatientProfile(name="test_patient", doctor=doctor)
        patient.save()
        self.assertEqual((patient.date_of_birth==None), True)
        self.assertEqual((patient.email==None), True)
        self.assertEqual((patient.cell_phone==None), True)

    def test_all_fields(self):
        '''
        test_all_fields should results True for SAVE all fields.
        '''
        doctor = DoctorProfile(username='test_doctor')
        doctor.save()
        today = datetime.date.today().strftime("%Y-%m-%d")
        patient = PatientProfile(
            name="test_patient", 
            doctor=doctor, 
            date_of_birth=today, 
            email='test@test.com', 
            cell_phone='1234567890'
        )
        patient.save()
        self.assertEqual((patient.date_of_birth==None), False)
        self.assertEqual((patient.email==None), False)
        self.assertEqual((patient.cell_phone==None), False)

        self.assertEqual((patient.name=="test_patient"), True)
        self.assertEqual((patient.doctor==doctor), True)
        self.assertEqual((patient.date_of_birth==today), True)
        self.assertEqual((patient.email=='test@test.com'), True)
        self.assertEqual((patient.cell_phone=='1234567890'), True)


class LogHistoryMethodTests(TestCase):
    def test_birthday_message(self):
        '''
        test_birthday_message should results True for SAVE Birthday Message history.
        '''
        doctor = DoctorProfile(username='test_doctor')
        doctor.save()
        now = datetime.datetime.now()
        patients_name = ['AAA BBB', 'CCC DDD', 'EEE FFF']
        log = LogHistory(
            time=now, 
            doctor=doctor, 
            patients=', '.join(patients_name), 
            birthday_message=True, 
            subject=None, 
            message_path=None
        )
        log.save()
        self.assertEqual((log.time==now), True)
        self.assertEqual((log.doctor==doctor), True)
        self.assertEqual((log.patients=='AAA BBB, CCC DDD, EEE FFF'), True)
        self.assertEqual(log.birthday_message, True)
        self.assertEqual((log.subject==None), True)
        self.assertEqual((log.message_path==None), True)

    def test_custom_message(self):
        '''
        test_all_fields should results True for SAVE Custom Message history.
        '''
        doctor = DoctorProfile(username='test_doctor')
        doctor.save()
        now = datetime.datetime.now()
        patients_name = ['AAA BBB', 'CCC DDD', 'EEE FFF']
        subject = 'SUBJECT'
        message_path = 'MESSAGE_PATH'
        log = LogHistory(
            time=now, 
            doctor=doctor, 
            patients=', '.join(patients_name), 
            birthday_message=False, 
            subject=subject, 
            message_path=message_path
        )
        log.save()
        self.assertEqual((log.time==now), True)
        self.assertEqual((log.doctor==doctor), True)
        self.assertEqual((log.patients=='AAA BBB, CCC DDD, EEE FFF'), True)
        self.assertEqual(log.birthday_message, False)
        self.assertEqual((log.subject=='SUBJECT'), True)
        self.assertEqual((log.message_path=='MESSAGE_PATH'), True)

        







