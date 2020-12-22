import os
from datetime import datetime

import numpy as np
from django.contrib import messages
from django.contrib.auth.decorators import login_required, user_passes_test
from django.shortcuts import render, redirect
from django.utils import timezone

from contests.models import Contest, Domain, Option, TotalScore, AttendedQuestion, Question, Section
from users.permissions import check_staff, check_student, sign_token

import joblib
from lms.settings import BASE_DIR


def index(request):
    return render(request, 'base.html')


@login_required
@user_passes_test(check_staff)
def manage_contests(request):
    contests = Contest.objects.filter(created_by=request.user.profile).order_by('-created_at')
    return render(request, 'contests/all_contests.html',
                  {'contests': contests, 'title': 'Manage Contests', 'heading': 'Manage Contests'})


@login_required
@user_passes_test(check_staff)
def create_contest(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        starts_at = datetime.strptime(request.POST.get('starts_at'), '%Y-%m-%dT%H:%M')
        ends_at = request.POST.get('ends_at')
        domains = request.POST.get('domains').split(';')
        if ends_at == '':
            ends_at = None
        else:
            ends_at = datetime.strptime(request.POST.get('ends_at'), '%Y-%m-%dT%H:%M')
        is_private = request.POST.get('is_private') == '1'
        contest_code = name[:10].lower() + '-' + str(
            Contest.objects.filter(created_by=request.user.profile).count() + 1)
        contest = Contest.objects.create(name=name, starts_at=starts_at, ends_at=ends_at, is_private=is_private,
                                         created_by=request.user.profile, contest_code=contest_code)
        for domain in domains:
            contest.domains.add(Domain.objects.get(name=domain))
        contest.save()
        messages.success(request, 'Contest created with contest code ' + contest.contest_code)
        return redirect('view-contests')
    return render(request, 'contests/create.html', {'heading': 'Add Contest', 'title': 'Create Contest'})


@login_required
@user_passes_test(check_staff)
def delete_contest(request, pk):
    if request.method == 'POST':
        try:
            contest = Contest.objects.filter(id=pk, created_by=request.user.profile)
            if contest.exists():
                contest = contest.first()
                for question in contest.question_set.all():
                    Option.objects.filter(question=question).delete()
                    question.delete()
                contest.delete()
        except:
            messages.error(request, 'Error in deleting contest.')
    return redirect(manage_contests)


@login_required
@user_passes_test(check_staff)
def edit_contest(request, pk):
    if request.method == 'POST':
        name = request.POST.get('name')
        starts_at = datetime.strptime(request.POST.get('starts_at'), '%Y-%m-%dT%H:%M')
        ends_at = request.POST.get('ends_at')
        domains = request.POST.get('domains').split(';')
        if ends_at == '':
            ends_at = None
        else:
            ends_at = datetime.strptime(request.POST.get('ends_at'), '%Y-%m-%dT%H:%M')
        is_private = request.POST.get('is_private') == '1'
        try:
            print(pk)
            contest = Contest.objects.get(created_by=request.user.profile, pk=pk)
            contest.name = name
            contest.ends_at = ends_at
            contest.starts_at = starts_at
            contest.is_private = is_private
            contest.domains.clear()
            for domain in domains:
                contest.domains.add(Domain.objects.get(name=domain))
            contest.save()
            messages.success(request, 'Contest edited successfully')
        except Exception as e:
            print(e)
        return redirect('view-contests')
    else:
        try:
            contest = Contest.objects.get(created_by=request.user.profile, id=pk)
            return render(request, 'contests/edit.html',
                          {'title': 'Edit Contest Details', 'heading': 'Edit Contest Details', 'contest': contest,
                           'domains': ';'.join(contest.domains.values_list('name', flat=True)),
                           'starts_at': datetime.strftime(contest.starts_at, '%Y-%m-%dT%H:%M'),
                           'ends_at': datetime.strftime(contest.ends_at,
                                                        '%Y-%m-%dT%H:%M') if contest.ends_at else None})
        except:
            return redirect('view-contests')


@login_required
@user_passes_test(check_staff)
def view_questions(request, id):
    if request.method == 'GET':
        token = sign_token(request.user)
        return render(request, 'contests/view_questions.html',
                      {'title': 'Manage Questions', 'heading': 'Manage Questions', 'id': id, 'token': token})


@login_required
@user_passes_test(check_student)
def view_contests(request):
    if request.method == 'GET':
        all_contests = Contest.objects.filter(is_private=False,
                                              domains__in=request.user.profile.domains.all()).order_by(
            '-created_at')
        if not all_contests.exists():
            all_contests = Contest.objects.filter(is_private=False)
        if all_contests.count() > 100:
            all_contests = all_contests[:100]
        return render(request, 'contests/view_contests.html',
                      {'contests': all_contests, 'title': 'All Contests', 'heading': 'All Contests'})


@login_required
@user_passes_test(check_student)
def view_contest_detail(request, id):
    if request.method == 'GET':
        try:
            contest = Contest.objects.get(id=id)
            attempts = request.user.profile.totalscore_set.filter(contest=contest)
            best_score = None
            if attempts.exists():
                count = attempts.count()
                best_score = max(attempts.values_list('score', flat=True))
            else:
                count = 0
            end_date_string = '' if not contest.ends_at else datetime.strftime(contest.ends_at, '%Y-%m-%dT%H:%M:%S')
            start_date_string = datetime.strftime(contest.starts_at, '%Y-%m-%dT%H:%M:%S')
            return render(request, 'contests/contest_detail.html',
                          {'contest': contest, 'title': contest.name, 'heading': contest.name, 'count': count,
                           'attempts': attempts, 'best_score': best_score, 'start': start_date_string,
                           'end': end_date_string})
        except Exception as e:
            print(e)
            return redirect(view_contests)


def choose_random_questions(available_questions, count):
    from random import sample
    available_questions_list = list(available_questions.values_list('id', flat=True))
    new_list = sample(available_questions_list, count)
    return Question.objects.filter(pk__in=new_list)


def get_questions(user, contest, new_difficulty):
    questions_set = user.profile.attendedquestion_set.all().values_list('question', flat=True)
    available_questions = contest.question_set.exclude(pk__in=questions_set).filter(difficulty_level=new_difficulty)
    if available_questions.count() > 5:
        questions = choose_random_questions(available_questions, 5)
    else:
        new_questions = available_questions
        new_questions_list = new_questions.values_list('id', flat=True)
        remaining_required = 5 - new_questions.count()
        old_available_questions = contest.question_set.filter(difficulty_level=new_difficulty).exclude(
            pk__in=new_questions_list)
        old_questions = choose_random_questions(old_available_questions, remaining_required)
        questions = new_questions.union(old_questions)
    return questions


def get_new_difficulty(mode, expected, actual, correct):
    model_path = os.path.join(BASE_DIR, 'knn.pkl')
    knn_model = joblib.load(model_path)
    data = np.array([mode, expected, actual, correct]).reshape(1, -1)
    return knn_model.predict(data)[0]


@login_required
@user_passes_test(check_student)
def start_contest(request, id):
    contest = Contest.objects.get(id=id)
    time_vector = [300, 750, 1000]
    if request.method == 'POST':
        section = Section.objects.get(id=request.POST['section'])
        time = int(request.POST['time'])
        questions = section.questions.all()
        for question in questions:
            q_id = question.id
            selected_option = request.POST.get(f'question_{q_id}')
            score_set = {Question.EASY: 1, Question.MEDIUM: 2, Question.HARD: 5}
            if selected_option is not None:
                question.option = Option.objects.get(question=question.question, choice_number=selected_option)
                question.save()
                if question.option.is_correct:
                    section.section_correct_options += 1
                    section.section_score += score_set[question.question.difficulty_level]

        section.time = 2 * time_vector[section.difficulty_level] - time
        messages.success(request,
                         f'You solved the previous section in {section.time} seconds. You got {section.section_correct_options} answers right.')
        section.save()
        profile = request.user.profile
        score_card = profile.totalscore_set.filter(contest=contest).order_by('finish_time')
        if score_card.exists():
            score_card = score_card.last()
            score_card.final_section = section
            if score_card.score <= section.section_score:
                score_card.score = section.section_score
                score_card.finish_time = timezone.now()
            score_card.save()
        else:
            score_card = TotalScore.objects.create(score=section.section_score, contest=contest, student=profile,
                                                   finish_time=timezone.now(), final_section=section)

        if section.difficulty_level == Question.HARD and section.section_correct_options == 5 and section.time < \
                time_vector[Question.HARD]:
            messages.success(request,
                             'Congratulations you have completed the contest with the maximum possible score.')
            return redirect('view-contest-student',id)

    flag = False
    if contest.starts_at > timezone.now():
        flag = True
    if contest.ends_at is not None:
        if contest.ends_at < timezone.now():
            flag = True
    if flag:
        print(contest.ends_at, contest.starts_at)
        return redirect('view-contest-student', id=id)
    else:
        score_set = request.user.profile.totalscore_set.filter(contest=contest).order_by('finish_time')
        if score_set.exists():
            last_section = score_set.last().final_section
            last_difficulty = last_section.difficulty_level
            last_correct = last_section.section_correct_options
            last_time = last_section.time
            expected_time = time_vector[last_difficulty]
            new_difficulty = get_new_difficulty(last_difficulty, expected_time, last_time, last_correct)
        else:
            new_difficulty = 0

        final_questions = get_questions(request.user, contest, new_difficulty)
        section = Section.objects.create(student=request.user.profile, contest=contest, difficulty_level=new_difficulty,
                                         section_score=0, section_correct_options=0)
        for question in final_questions:
            attended_question = AttendedQuestion.objects.create(student=request.user.profile, question=question)
            section.questions.add(attended_question)
        time = [300, 750, 1000]
        section_time = 2 * time[new_difficulty]
        return render(request, 'contests/view_section.html', {'section': section, 'time': section_time})
