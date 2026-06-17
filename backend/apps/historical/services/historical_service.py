from .models import HistoricalForm


class HistoricalService:
    @staticmethod
    def find_by_modern(modern_form: str):
        return HistoricalForm.objects.filter(modern_form__iexact=modern_form).order_by('-confidence_score')
