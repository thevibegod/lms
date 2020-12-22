from rest_framework.serializers import ModelSerializer

from contests.models import Question, Option

class QuestionSerializer(ModelSerializer):
    # options = OptionSerializer(read_only=True, many=True)

    class Meta:
        model = Question
        fields = '__all__'
        depth = 2

class OptionSerializer(ModelSerializer):
    # question = QuestionSerializer(read_only=True, many=True)
    class Meta:
        model = Option
        fields = '__all__'
        depth=2



