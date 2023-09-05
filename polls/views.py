from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.shortcuts import get_object_or_404, render
from django.urls import reverse
from django.views import generic

from .models import Choice, Question


"""generic.ListView abstracts a concept of "Display a list of objects" """
class IndexView(generic.ListView):
    template_name = "polls/index.html"
    context_object_name = "latest_question_list"

    def get_queryset(self):
        """Return the last five published questions."""
        return Question.objects.order_by("-pub_date")[:5]


"""
generic.DetailView abstracts a concept of
"Display a detail page for a partivular type of object."
"""
class DetailView(generic.DetailView):
    model = Question
    template_name = "polls/detail.html"


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
    
