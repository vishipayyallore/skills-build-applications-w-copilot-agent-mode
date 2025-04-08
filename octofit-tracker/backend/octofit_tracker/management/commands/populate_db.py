from django.core.management.base import BaseCommand
from octofit_tracker.models import User, Team, Activity, Leaderboard, Workout
from octofit_tracker.test_data import get_test_data
from django.conf import settings
from pymongo import MongoClient

class Command(BaseCommand):
    help = 'Populate the database with test data for users, teams, activities, leaderboard, and workouts'

    def handle(self, *args, **kwargs):
        # Connect to MongoDB
        client = MongoClient(settings.DATABASES['default']['HOST'], settings.DATABASES['default']['PORT'])
        db = client[settings.DATABASES['default']['NAME']]

        # Drop existing collections
        db.users.drop()
        db.teams.drop()
        db.activities.drop()
        db.leaderboard.drop()
        db.workouts.drop()

        # Clear existing data
        User.objects.all().delete()
        Team.objects.all().delete()
        Activity.objects.all().delete()
        Leaderboard.objects.all().delete()
        Workout.objects.all().delete()

        # Get test data
        test_data = get_test_data()

        # Populate users
        for user_data in test_data['users']:
            User.objects.update_or_create(username=user_data['username'], defaults=user_data)

        # Populate teams
        teams = [Team(**team) for team in test_data['teams']]
        Team.objects.bulk_create(teams)

        # Populate activities
        activities = []
        for activity in test_data['activities']:
            user_instance = User.objects.get(username=activity['user'])
            activity['user'] = user_instance
            activities.append(Activity(**activity))
        Activity.objects.bulk_create(activities)

        # Populate leaderboard
        leaderboard_entries = []
        for entry in test_data['leaderboard']:
            user_instance = User.objects.get(username=entry['user'])
            entry['user'] = user_instance
            leaderboard_entries.append(Leaderboard(**entry))
        Leaderboard.objects.bulk_create(leaderboard_entries)

        # Populate workouts
        workouts = [Workout(**workout) for workout in test_data['workouts']]
        Workout.objects.bulk_create(workouts)

        self.stdout.write(self.style.SUCCESS('Successfully populated the database with test data.'))