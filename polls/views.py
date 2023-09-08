from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.shortcuts import get_object_or_404, render
from django.urls import reverse
from django.views import generic
from django.utils import timezone

from .models import Choice, Question


"""generic.ListView abstracts a concept of "Display a list of objects" """
class IndexView(generic.ListView):
    template_name = "polls/index.html"
    context_object_name = "latest_question_list"

    def get_queryset(self):
        """
        Return the last five published questions (not including those set
        to be published in the future).
        """
        # less than or equal to - that is, earlier than or equal to - timezone.now
        return Question.objects.filter(pub_date__lte=timezone.now()).order_by("-pub_date")[:5]


"""
generic.DetailView abstracts a concept of
"Display a detail page for a particular type of object."
"""
class DetailView(generic.DetailView):
    model = Question
    template_name = "polls/detail.html"

    def get_queryset(self):
        """
        Excludes any questions that aren't published yet.
        """
        return Question.objects.filter(pub_date__lte=timezone.now())


class ResultsView(generic.DetailView):
    model = Question
    template_name = "polls/results.html"


def vote(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    try:
        selected_choice = question.choice_set.get(pk=request.POST["choice"])
        # request.POST['choice'] will raise KeyError if choice wasn't provided
        # in POST data.
    except (KeyError, Choice.DoesNotExist):
        return render(
            request,
            "polls/detail.html",
            {
                "question": question,
                "error_message": "You didn't select a choice.",
            },
        )
    else:
        # The else clause is useful for code that must be executed if
        # the try clause does not raise an exception. The use of the else
        # clause is better than adding additional code to the try clause
        # because it avoids accidentally catching an exception that wasn't
        # raised by the code being protected by the try ... except statement.
        selected_choice.votes += 1
        selected_choice.save()
        # Always return an HttpResponseRedirect after successfully dealing
        # with POST data. This prevents data from being posted twice if a
        # user hits the Back button.
        return HttpResponseRedirect(
            # reverse() in this case produces "/polls/3/results/",
            # where the 3 is the value of question.id
            reverse("polls:results", args=(question.id,))
        )
    
