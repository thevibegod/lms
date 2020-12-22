from django.db import models
from django.utils import timezone


class Domain(models.Model):
    def __str__(self):
        return self.name

    name = models.CharField(max_length=50)


class Contest(models.Model):

    def __str__(self):
        return self.name

    name = models.CharField(max_length=100)
    contest_code = models.CharField(max_length=20)
    starts_at = models.DateTimeField()
    ends_at = models.DateTimeField(null=True, blank=True)
    created_by = models.ForeignKey('users.Profile', on_delete=models.CASCADE)
    created_at = models.DateTimeField(default=timezone.now)
    domains = models.ManyToManyField(Domain)
    is_private = models.BooleanField(default=False)


class Question(models.Model):
    EASY = 0
    MEDIUM = 1
    HARD = 2
    DIFFICULTY_LEVELS = ((EASY, 'Easy'), (MEDIUM, 'Medium'), (HARD, 'Hard'))
    contest = models.ForeignKey(Contest, on_delete=models.CASCADE)
    statement = models.TextField()
    image = models.ImageField(null=True, upload_to='questions/', blank=True)
    created_at = models.DateTimeField(default=timezone.now)
    difficulty_level = models.IntegerField(choices=DIFFICULTY_LEVELS)
    options = models.ManyToManyField('Option', related_name='question')


class Option(models.Model):
    # question = models.ForeignKey(Question, on_delete=models.CASCADE)
    statement = models.TextField()
    image = models.ImageField(null=True, upload_to='options/', blank=True)
    is_correct = models.BooleanField(default=False)
    created_at = models.DateTimeField(default=timezone.now)
    choice_number = models.IntegerField()


class AttendedQuestion(models.Model):
    student = models.ForeignKey('users.Profile', on_delete=models.CASCADE)
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    option = models.ForeignKey(Option, on_delete=models.CASCADE, null=True)


class Section(models.Model):
    student = models.ForeignKey('users.Profile', on_delete=models.CASCADE)
    contest = models.ForeignKey(Contest, on_delete=models.CASCADE)
    difficulty_level = models.IntegerField(choices=Question.DIFFICULTY_LEVELS)
    questions = models.ManyToManyField(AttendedQuestion)
    section_score = models.IntegerField()
    section_correct_options = models.IntegerField()
    time = models.IntegerField(default=0, null=True, blank=True)


class TotalScore(models.Model):
    student = models.ForeignKey('users.Profile', on_delete=models.CASCADE)
    contest = models.ForeignKey(Contest, on_delete=models.CASCADE)
    score = models.IntegerField()
    finish_time = models.DateTimeField()
    final_section = models.ForeignKey(Section, on_delete=models.CASCADE, null=True)
