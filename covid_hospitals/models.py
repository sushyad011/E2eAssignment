from django.db import models

# Create your models here.

class Bed(models.Model):

    bed_types = (
        ('general', 'general'),
        ('semi-private','semi-private'),
        ('private', 'private')
    )

    bed_status = [
        ('empty', 'empty'),
        ('full','full'),
        ('defective', 'defective'),
    ]

    bed_id = models.IntegerField(primary_key=True,editable=False)
    type = models.CharField(max_length=255, choices=bed_types)
    status = models.CharField(max_length=255, choices=bed_status, default='empty')

    def __str__(self):
        return self.type

    def __repr__(self):
        return '<Bed(id: %d,type: %s)>' %(self.id,self.type)


class Patient(models.Model):

    name = models.CharField(max_length=255)
    assigned_bed = models.ForeignKey(Bed, on_delete=models.CASCADE,null=True, blank=True,db_column='bed_id')
    active = models.BooleanField(default=True)

    def __str__(self):
        return self.name