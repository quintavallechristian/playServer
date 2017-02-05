from django.db.models import Q
from rest_framework import serializers
from .models import *
from django.db.models import Count, Max

# Json representation of the dictionary
class DictionarySerializers(serializers.ModelSerializer):
    class Meta:
        model = Dictionary
        fields = ('pk', 'word', 'description')

class SimpleBoardgamesSerializers(serializers.ModelSerializer):
    class Meta:
        model = Boardgames
        fields = ('pk', 'title', 'thumbnail', 'img',)


# Json representation of users and statistics
class UsersSerializers(serializers.ModelSerializer):
    # Serializer initialization: read the url params
    def __init__(self, *args, **kwargs):
        super(UsersSerializers, self).__init__(*args, **kwargs)

        # Allowed params: "include"
        includes = self.context['request'].query_params.get('include')
        if includes:
            fields = includes.split(',')
            allowed = set(fields)

            # Allowed values: "user_stats"
            if "user_stats" not in allowed:
                self.fields.pop("match_played")
                self.fields.pop("most_played_game")
                self.fields.pop('match_won')
        else:
            self.fields.pop("match_played")
            self.fields.pop("most_played_game")
            self.fields.pop('match_won')

    match_played = serializers.SerializerMethodField()
    most_played_game = serializers.SerializerMethodField()
    match_won = serializers.SerializerMethodField()

    # Get the amount of match played by the user, given a boardgame (total if not given)
    def get_match_played(self, user):
        if ("boardgame" in self.context):
            boardgame = self.context["boardgame"]
            plays_amount = Users.objects.filter(plays__match__boardgame=boardgame, plays__user=user).count()
        else:
            plays_amount = Plays.objects.filter(user=user).count()
        return plays_amount

    # Get the most played game
    def get_most_played_game(self, user):
        games = Boardgames.objects.filter(matches__plays__user=user).annotate(amount=Count('matches')).order_by(
            '-amount')
        if(len(games) !=0):
            return games[0].title
        else:
            return "No game played"

    # Get the amount of match won by the user, given a boardgame (total if not given)
    def get_match_won(self, user):
        if ("boardgame" in self.context):
            boardgame = self.context["boardgame"]
            # Extract the match-points pair from the plays table, stating the highest result for each match.
            #.values() returns a dictionary (json)
            max_points_per_match = Plays.objects.filter(match__boardgame=boardgame).values('match').annotate(max_points=Max('points'))

            #Q() function is used, here, to recreate the query using the match-points pair obtained above.
            #It is necessary because .values() returned unusable results for the database.
            q_statement = Q()
            for pair in max_points_per_match:
                q_statement |= (Q(match=pair['match']) & Q(points=pair['max_points']))

            #Count the amount of won matches by filtering the Plays table looking at q_statment and keeping
            #only the plays in which the given user is the one with the most points.
            # Finally it counts the number of obtained rows.
            win_count = Plays.objects.filter(q_statement, user=user).count()
        else:
            # Extract the match-points pair from the plays table, stating the highest result for each match.
            #.values() returns a dictionary (json) and, aggregate with the "Max" function, performs a group by operation
            #The dictionary cannot be further analyzed because we have not visibility of the other fields of the record.
            max_points_per_match = Plays.objects.all().values('match').annotate(max_points=Max('points'))

            #Q() function is used, here, to recreate the query using the match-max_points pair obtained above.
            # "|=" operator concatenate all the possible combination of match-points in an OR sequence in order to
            #catch all the corresponding records. In this way we can re-obtain the full records, containing also the
            #information regarding the "winning" user. In this way we can catch if the analyzed user is the one that
            #obtained the highest points for each match.
            q_statement = Q()
            for pair in max_points_per_match:
                q_statement |= (Q(match=pair['match']) & Q(points=pair['max_points']))

            #Count the amount of won matches by filtering the Plays table looking at q_statment and keeping
            #only the plays in which the given user is the one with the most points.
            # Finally it counts the number of obtained rows.
            win_count = Plays.objects.filter(q_statement, user=user).count()

        return win_count

    class Meta:
        model = Users
        fields = ('pk', 'email', 'username', 'match_played', 'most_played_game', 'match_won', 'img', )

# Json representation of the template of a boardgames
class TemplatesSerializers(serializers.ModelSerializer):
    word_details = serializers.SerializerMethodField()

    def get_word_details(self, template):
        word = Dictionary.objects.get(templates=template)
        serializer = DictionarySerializers(word)
        return serializer.data

    class Meta:
        model = Templates
        fields = ('boardgame', 'word', 'word_details')

class DetailedPointsSerializers(serializers.ModelSerializer):
    template_details = serializers.SerializerMethodField()
    
    def get_template_details(self, dtPoints):
        template = Templates.objects.get(detailedpoints=dtPoints)
        serializer = TemplatesSerializers(template)
        return serializer.data

    class Meta:
        model = DetailedPoints
        fields = ('template', 'play', 'detailed_points', 'template_details', 'notes')

# Json representation of single plays
class PlaysSerializers(serializers.ModelSerializer):
    user_details = serializers.SerializerMethodField()
    detailedPoints = serializers.SerializerMethodField()

    def get_user_details(self, play):
        user = Users.objects.get(plays=play)
        serializer = UsersSerializers(user, context={'request': self.context['request']})
        return serializer.data

    def get_detailedPoints(self, play):
        dtPoints = DetailedPoints.objects.filter(play=play)
        serializer = DetailedPointsSerializers(dtPoints, many=True, context={'request': self.context['request']})
        return serializer.data

    class Meta:
        model = Plays
        fields = ('pk', 'match', 'user', 'user_details', 'points', 'detailedPoints')

# Json representation of single matches
class MatchesSerializers(serializers.ModelSerializer):
    plays_set = PlaysSerializers(many=True, read_only=True)
    boardgame_details = serializers.SerializerMethodField()

    def __init__(self, *args, **kwargs):
        super(MatchesSerializers, self).__init__(*args, **kwargs)
        # Allowed params: "include"
        includes = self.context['request'].query_params.get('include')
        if includes:
            fields = includes.split(',')
            allowed = set(fields)

            # Allowed values: "matches", "users", "friends", "favourite"
            if "boardgame" not in allowed:
                self.fields.pop("boardgame")

    def get_boardgame_details(self, match):
        boardgame = Boardgames.objects.get(matches=match)
        serializer = SimpleBoardgamesSerializers(boardgame)
        return serializer.data

    class Meta:
        model = Matches
        fields = ('pk', 'boardgame', 'name', 'time', 'location', 'boardgame_details', 'duration', 'plays_set',)

# Json representation of boardgames and statistics
class BoardgamesSerializers(serializers.ModelSerializer):
    # Serializer initialization: read the url params
    def __init__(self, *args, **kwargs):
        super(BoardgamesSerializers, self).__init__(*args, **kwargs)

        # Allowed params: "include"
        includes = self.context['request'].query_params.get('include')
        if includes:
            fields = includes.split(',')
            allowed = set(fields)

            # Allowed values: "matches", "users", "friends", "favourite"
            if "matches" not in allowed:
                self.fields.pop("matches")
            if "users" not in allowed:
                self.fields.pop("users")
            if "friends" not in allowed:
                self.fields.pop("friends")
        else:
            self.fields.pop("matches")
            self.fields.pop("friends")
            self.fields.pop("users")

    matches = serializers.SerializerMethodField()
    users = serializers.SerializerMethodField()
    friends = serializers.SerializerMethodField()
    favourite = serializers.SerializerMethodField()

    # Get matches played given a boardgame and a user (all matches if user is not provided)
    def get_matches(self, boardgame):
        user_id = self.context['request'].query_params.get('user_id')
        if user_id:
            matches = Matches.objects.filter(boardgame=boardgame, plays__user=user_id)
        else:
            matches = Matches.objects.filter(boardgame=boardgame)

        serializer = MatchesSerializers(matches, many=True, context={'request': self.context['request']})
        return serializer.data

    # Get list of users playing a boardgame
    def get_users(self, boardgame):
        users = Users.objects.filter(plays__match__boardgame=boardgame).distinct()
        serializer = UsersSerializers(users, many=True,
                                      context={'request': self.context['request'], 'boardgame': boardgame})
        return serializer.data

    # Get list of all friend playing a boardgame, given a user
    def get_friends(self, boardgame):
        user_id = self.context['request'].query_params.get('user_id')
        if user_id:
            friends = Users.objects.filter(plays__match__boardgame=boardgame,
                                           user2__user1=user_id).distinct() | Users.objects.filter(
                                            plays__match__boardgame=boardgame,
                                            user1__user2=user_id).distinct()
            serializer = UsersSerializers(friends, many=True,
                                          context={'request': self.context['request'], 'boardgame': boardgame})
            return serializer.data

    def get_favourite(self, boardgame):
        user_id = self.context['request'].query_params.get('user_id')
        if user_id:
            favourite = Users.objects.filter(favourites__boardgame=boardgame, pk=user_id).count()
            return favourite
        else: return -1

    class Meta:
        model = Boardgames
        fields = ('pk', 'title','description', 'img', 'thumbnail', 'average', 'minage', 'playingtime', 'minplayers', 'maxplayers', 'yearpublished', 'maxplaytime', 'minplaytime', 'usersrated', 'matches', 'users', 'friends', 'favourite')

# Json representation of friends
class FriendsSerializers(serializers.ModelSerializer):
    class Meta:
        model = Friends
        fields = ('pk', 'user1','user2')

# Json representation of favourites boardgames by an user
class FavouritesSerializers(serializers.ModelSerializer):
    class Meta:
        model = Favourites
        fields = ('pk', 'user','boardgame')