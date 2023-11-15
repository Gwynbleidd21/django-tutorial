from django.core.management.base import BaseCommand
from polls.models import Poll, Question, Choice, Answer
import random
from django.utils import timezone


class Command(BaseCommand):
    help = 'Generates a large dataset of polls, questions, choices, and answers'

    def handle(self, *args, **kwargs):
        # Delete existing records
        Answer.objects.all().delete()
        Choice.objects.all().delete()
        Question.objects.all().delete()
        Poll.objects.all().delete()

        # Generate 500 polls
        for i in range(500):
            print(f"Generating poll {i}")
            poll = Poll.objects.create(title=f"Sample Poll {i}")
            # Generate questions for each poll
            for j in range(5):  # Each poll has 5 questions
                question = Question.objects.create(
                    poll=poll,
                    question_text=f"Sample Question {i}_{j}?",
                    pub_date=timezone.now()  # Set the publication date to now
                )
                # Generate choices for each question
                for k in range(4):  # Each question has 4 choices
                    choice = Choice.objects.create(question=question, choice_text=f"Sample Choice {i}_{j}_{k}")
                    # Generate answers for each choice
                    for _ in range(random.randint(1, 10)):  # Each choice has 1 to 10 answers
                        Answer.objects.create(choice=choice)

        self.stdout.write(self.style.SUCCESS('Successfully generated the dataset'))
