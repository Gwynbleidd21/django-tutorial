from django.core.cache import cache
from django.http import HttpResponseRedirect, JsonResponse
from django.shortcuts import render, get_object_or_404
from django.urls import reverse
from django.utils import timezone
from django.views import generic

from .models import Answer, Question, Choice, Poll


class IndexView(generic.ListView):
    template_name = "polls/index.html"
    context_object_name = "latest_question_list"

    def get_queryset(self):
        return Question.objects.filter(
            pub_date__lte=timezone.now(),
            poll__isnull=False
        ).order_by("-pub_date")[:25]


class DetailView(generic.DetailView):
    model = Question
    template_name = "polls/detail.html"

    def get_queryset(self):
        return Question.objects.filter(pub_date__lte=timezone.now())


class ResultsView(generic.DetailView):
    model = Poll
    template_name = "polls/results.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        poll = self.get_object()
        questions = poll.question_set.all()
        context['questions'] = questions
        return context


def vote(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    try:
        selected_choice = question.choice_set.get(pk=request.POST['choice'])
    except (KeyError, Choice.DoesNotExist):
        # Redisplay the question voting form with an error message
        return render(request, 'polls/detail.html', {
            'question': question,
            'error_message': "You didn't select a choice.",
        })
    else:
        # Create an Answer record for the selected choice
        Answer.objects.create(choice=selected_choice, timestamp=timezone.now())
        return HttpResponseRedirect(reverse('polls:results', args=(question.poll_id,)))


def poll_results_api(request, poll_id):
    poll = get_object_or_404(Poll, pk=poll_id)

    # Try to get results from cache
    cache_key = f'poll_results_{poll_id}'
    results_data = cache.get(cache_key)

    # If not in cache, calculate the results
    if not results_data:
        results_data = []
        for question in poll.question_set.all():
            choices_data = []
            for choice in question.choice_set.all():
                choices_data.append({
                    'choice_text': choice.choice_text,
                    'votes': choice.answer_set.count()
                })
            results_data.append({
                'question_text': question.question_text,
                'choices': choices_data,
                'question_id': question.id
            })
        # Store results in cache
        cache.set(cache_key, results_data, timeout=3600)  # Cache for 1 hour, adjust as needed

    return JsonResponse({'poll_id': poll.id, 'results': results_data})

