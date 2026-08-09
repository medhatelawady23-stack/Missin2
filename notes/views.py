from django.views import View
from django.http import JsonResponse
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Note


class NotesAPIView(LoginRequiredMixin, View):
    def get(self, request):
        location_id = request.GET.get('location')
        if location_id:
            notes = Note.objects.filter(
                is_active=True,
                locations__id=location_id
            ).distinct()
        else:
            notes = Note.objects.filter(is_active=True)
        data = [{'id': n.id, 'text': n.text} for n in notes]
        return JsonResponse({'notes': data})
