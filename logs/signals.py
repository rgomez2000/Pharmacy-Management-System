from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils import timezone
from prescriptions.models import Prescription
from .models import PrescriptionLog

@receiver(post_save, sender=Prescription)
def log_creation(sender, instance, created, **kwargs):
    if instance.is_filled:
        now = timezone.now()
        PrescriptionLog.objects.create(
            pharmacist_name = instance.created_by,
            prescription_number = instance.id,
            patient_name = instance.patient,
            date = now.date(),
            time = now.time(),
            drug_type = instance.medication.drug_class,
            quantity = instance.dosage
        )