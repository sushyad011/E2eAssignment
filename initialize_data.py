import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE','covid.settings')

import django
django.setup()

from covid_hospitals.models import Bed

class InitializeData:

    def __init__(self):
        total_beds=self.get_total_bed()
        self.add_beds(total_beds)

    def get_total_bed(self):
        total_beds = int(input('Please enter total number of beds '))
        return total_beds

    def add_beds(self,total_beds):

        for pk in range(0,total_beds,2):
            self.insert_general_bed(pk)

        for pk in range(1,total_beds,4):
            self.insert_semi_private_bed(pk)

        for pk in range(3,total_beds,4):
            self.insert_private_bed(pk)

    def insert_general_bed(self,pk):
        Bed.objects.create(bed_id=pk,type='general',status='empty')

    def insert_semi_private_bed(self,pk):
        Bed.objects.create(bed_id=pk,type='semi-private',status='empty')

    def insert_private_bed(self,pk):
        Bed.objects.create(bed_id=pk,type='private',status='empty')

if __name__=='__main__':
    InitializeData()