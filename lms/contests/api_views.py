from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

from contests.models import Contest, Option, Question
from contests.serializers import QuestionSerializer, OptionSerializer
from users.models import Profile
from users.permissions import decode_token


@csrf_exempt
def get_questions(request):
    if request.method == 'GET':
        try:
            id = request.GET.get('id')
            token = request.headers.get('x-api-key')
            username = decode_token(token)
            if username == -1:
                return JsonResponse({'success': False, 'message': 'Token expired'}, status=403)
            contest = Contest.objects.filter(id=id, created_by__user__username=username)
            if contest.exists():
                contest = contest[0]
            else:
                return JsonResponse({'success': False, 'message': 'Unauthorised Access'}, status=403)
            # options = Option.objects.filter(question__contest=contest)

            questions = contest.question_set.all()
            data = QuestionSerializer(questions, many=True).data
            # data = OptionSerializer(options,many=True).data
            return JsonResponse({'success': True, 'data': data})
        except Exception as e:
            print(e)
            return JsonResponse({'success': False, 'message': 'Server Error'}, status=500)

    elif request.method == 'POST':
        try:
            id = request.POST.get('id')
            token = request.headers.get('x-api-key')
            username = decode_token(token)
            print(username)
            if username == -1:
                return JsonResponse({'success': False, 'message': 'Token expired'}, status=403)
            contest = Contest.objects.filter(id=id, created_by__user__username=username)
            print(contest)
            if contest.exists():
                contest = contest[0]
            else:
                return JsonResponse({'success': False, 'message': 'Unauthorised Access'}, status=403)
            stmt = request.POST.get('statement')
            img = request.FILES.get('image')
            difficulty_level = int(request.POST.get('difficulty_level'))
            question = Question.objects.create(contest=contest, statement=stmt, image=img,
                                               difficulty_level=difficulty_level)
            try:
                i = 1
                while True:
                    option_text = request.POST[f'option_{i}_text']
                    option_value = request.POST[f'option_{i}_value'] == 'true'
                    option = Option.objects.create(statement=option_text, is_correct=option_value, choice_number=i)
                    question.options.add(option)
                    i += 1
            except:
                question.save()
                return JsonResponse({'success': True, 'data': QuestionSerializer(question).data})
        except Exception as e:
            print(e)
            return JsonResponse({'success': False, 'message': 'Server Error'}, status=500)
    else:
        return JsonResponse({'success': False, 'message': 'Method not allowed.'}, status=405)


@csrf_exempt
def delete_question(request, id):
    if request.method == 'POST':
        try:
            token = request.headers.get('x-api-key')
            username = decode_token(token)
            print(username)
            if username == -1:
                return JsonResponse({'success': False, 'message': 'Token expired'}, status=403)
            profile = Profile.objects.get(user__username=username)
            question = Question.objects.filter(id=id, contest__created_by=profile)
            print(question)
            if question.exists():
                Option.objects.filter(question=question.first()).delete()
                question.first().delete()
                return JsonResponse({'success': True})
            else:
                return JsonResponse({'success': False, 'message': 'Unauthorised Access'}, status=403)
        except Exception as e:
            print(e)
            return JsonResponse({'success': False, 'message': 'Server Error'}, status=500)


