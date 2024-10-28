from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils import timezone
from prescriptions.models import Prescription
from .models import PrescriptionLog

@receiver(post_save, sender=Prescription)
def log_creation(sender, instance, created, **kwargs):
    print("Creating PrescriptionLog for:", instance)
    if created:
        print("Creating PrescriptionLog for:", instance)
        now = timezone.now()
        PrescriptionLog.objects.create(
            pharmacist_name = instance.created_by,  # May need to later be adjusted to 'filled_by'
            prescription_number = instance.id,
            patient_name = instance.patient,
            date = now.date(),
            time = now.time(),
            # drug_type = instance.drug_type, # Need to add 'type' field to prescriptions model
            # quantity = instance.quantity # Same as dosage?
        )