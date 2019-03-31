#https://simpleisbetterthancomplex.com/tutorial/2018/08/13/how-to-use-bootstrap-4-forms-with-django.html

from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404
from django.urls import reverse
from django.views import generic
from django.utils import timezone
from .forms import SuggestionForm
from .models import Choice, Question, Suggestion

class IndexView(generic.ListView):
    template_name = 'polls/index.html'
    context_object_name = 'latest_question_list'

    def get_queryset(self):
        """Return the last five published questions."""
        return Question.objects.filter(
            pub_date__lte=timezone.now()
        ).order_by('-pub_date')[:5]

class DetailView(generic.DetailView):
    model = Question
    template_name = 'polls/detail.html'
    def get_queryset(self):
        """ Excludes any questions that arent published yet"""
        return Question.objects.filter(pub_date__lte=timezone.now())

class ResultsView(generic.DetailView):
    model = Question
    template_name = 'polls/results.html'

from django.shortcuts import redirect 

def sugg(request):
    if request.method == "POST":
        form = SuggestionForm(request.POST)
        if form.is_valid():
            suggestion = form.save()
            suggestion.save()
            return suggestionlist(request)
    else:
        form = SuggestionForm()
    return render(request, 'polls/sugg.html',{'form':form})

def suggestionlist(request):
    context = {
        'posts' : Suggestion.objects.all()
    }
    return render(request, 'polls/suggestionlist.html',context)

def vote(request, question_id):
    question = get_object_or_404(Question, pk = question_id)
    try:
        selected_choice = question.choice_set.get(pk=request.POST['choice'])
    except(KeyError,Chocie.DoesNotExist):
        return render(request, 'polls/detail.html', {
            'question':question,
            'error_message': "You didn't select a choice."
        })
    else:
        selected_choice.votes += 1
        selected_choice.save()
        return HttpResponseRedirect(reverse('polls:results', args=(question.id,)))