from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from models import Question
from django.template import loader
from django.http import Http404
from django.views import generic

from rest_framework.renderers import JSONRenderer
from rest_framework.parsers import JSONParser
from models import Snippet
from models import SnippetSerializer

# Create your views here.
def index(request):
    latest_question_list = Question.objects.order_by('-pub_date')[:5]

    context = {'latest_question_list': latest_question_list}
    return render(request, 'polls/index.html', context)

    template = loader.get_template('polls/index.html')

    context = {
        'latest_question_list': latest_question_list,
    }
    return HttpResponse(template.render(context, request))

    output = ', '.join([q.question_text for q in latest_question_list])
    return HttpResponse(output)
    return HttpResponse("Hello, world. You're at the polls index.")

def detail(request, question_id):
    try:
        question = Question.objects.get(pk=question_id)
    except Question.DoesNotExist:
        raise Http404("Question does not exist")
    return render(request, 'polls/detail.html', {'question': question})

    return HttpResponse("You're looking at question %s." % question_id)

def results(request, question_id):
    response = "You're looking at the results of question %s."
    return HttpResponse(response % question_id)

def vote(request, question_id):
    return HttpResponse("You're voting on question %s." % question_id)


class DetailView(generic.DetailView):
    model = Question
    template_name = 'polls/detail.html'


def snippet_list(request):
    """
    List all code snippets, or create a new snippet.
    """
    if request.method == 'GET':
        snippets = Snippet.objects.all()
        serializer = SnippetSerializer(snippets, many=True)
        return JsonResponse(serializer.data, safe=False)

    elif request.method == 'POST':
        data = JSONParser().parse(request)
        serializer = SnippetSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data, status=201)
        return JsonResponse(serializer.errors, status=400)