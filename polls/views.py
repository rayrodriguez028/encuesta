from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.urls import reverse
from django.views import generic
from django.utils import timezone
from .models import Choice, Question


class IndexView(generic.ListView):
    template_name = 'polls/index.html'
    context_object_name = 'first_question'

    def get_queryset(self):
        """Regresa la primera pregunta por id 1"""
        return Question.objects.filter(pk=21)


class DetailView(generic.DetailView):
    model = Question
    template_name = 'polls/detail.html'

    def get_queryset(self):
        """
        Excludes any questions that aren't published yet.
        """
        return Question.objects.filter(pub_date__lte=timezone.now())


class ResultsView(generic.DetailView):
    model = Question
    template_name = 'polls/detail.html'

def vote(request, question_id):
    ultima_pregunta = 27
    question = get_object_or_404(Question, pk=question_id)
    try:
        selected_choice = question.choice_set.get(pk=request.POST['choice'])
    except (KeyError, Choice.DoesNotExist):
            # Redisplay the question voting form.
        return render(request, 'polls/detail.html', {
            'question': question,
            'error_message': "No seleccionó una opción.",
            })
    else:
        selected_choice.votes += 1
        selected_choice.save()
                # Always return an HttpResponseRedirect after successfully dealing
                # with POST data. This prevents data from being posted twice if a
                # user hits the Back button.
                #if question.id+1 ==
        if question.id == ultima_pregunta:
            return render(request, 'polls/index.html', {
            'error_message': "Sus respuestas han sido registradas.",
            })
             
        return HttpResponseRedirect(reverse('polls:detail', args=(question.id+1,)))