import gamestore.settings as settings
from django.core.management.base import BaseCommand, CommandError
from board.models import Game, Tweet
from board.logic.tweet import TweetAPI
from board.api import twitterapi


twitter_wrapper = twitterapi.TwitterWrapper(settings.API_TWITTER_TOKEN)


class Command(BaseCommand):
    help = 'Add the specified filtered games to database'

    def add_arguments(self, parser):
        parser.add_argument('-i', '--id', action='store', nargs='?', default=None, type=int)

    def handle(self, *args, **options):
        game_id = options['id']
        game = Game.objects.filter(id=game_id).first()

        tweet_ids_log = []
        tweet_ids = twitter_wrapper.get_tweets_by_string(game.slug)
        if tweet_ids:
            for tweet_id in tweet_ids:
                tweet = TweetAPI(tweet_id)
                new_values = {
                    'text': tweet.text,
                    'created_at': tweet.created_at,
                    'author_id': tweet.author_id,
                    'author_name': tweet.author_name,
                    'author_url': tweet.author_url,
                    'game': game,
                }
                Tweet.objects.update_or_create(id=tweet.id, defaults=new_values)
                tweet_ids_log.append(tweet.id)
        else:
            raise CommandError('There are no tweets with such parameters')

        self.stdout.write(self.style.SUCCESS(f'Successfully added tweets with id: {tweet_ids_log}'))
