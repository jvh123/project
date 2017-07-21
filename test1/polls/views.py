from polls.models import Choice,Question
from django.shortcuts import render,get_object_or_404
from django.core.urlresolvers import reverse
from django.views.generic import ListView,DetailView
import logging
from django.http import HttpResponseRedirect
logger=logging.getLogger(__name__)
class IndexView(ListView):
    template_name= 'polls/index.html'
    context_object_name='latest_question_list'
    def get_queryset(self):
        return Question.objects.order_by('-pub_date')[:5]
class DetailView(DetailView):
    model=Question
    template_name='polls/detail.html'
class ResultsView(DetailView):
    model=Question
    template_name='polls/results.html'
def vote(request,question_id):
    logger.debug('vote().question_id:%s'%question_id)
    p=get_object_or_404(Question,pk=question_id)
    try:
        selected_choice=p.choice_set.get(pk=request.POST['choice'])
    except(KeyError,Choice.DoesNotExist):
        return render(request, 'polls/detail.html', {
            'question':p,
            'error_message':"You didn't select a choice",
        })
    else:
        selected_choice.votes+=1
        selected_choice.save()
        return HttpResponseRedirect(reverse('polls:results',args=(p.id)))
# Create your views here.
