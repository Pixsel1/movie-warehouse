import re

from rest_framework import serializers

from moviewarehouse.movies.models import Comment, Movie

NUMBER_PATTERN = re.compile(r"\d+")
FLOAT_NUMBER_PATTERN = re.compile(r"\d+\.\d+")


class TopMovieSearchSerializer(serializers.Serializer):
    date_to = serializers.DateField()
    date_from = serializers.DateField()


class TopMovieSerializer(serializers.Serializer):
    movie_id = serializers.IntegerField(source="id")
    total_comments = serializers.IntegerField()
    rank = serializers.IntegerField()


class MovieSearchSerializer(serializers.Serializer):
    title = serializers.CharField()


class MovieSerializer(serializers.ModelSerializer):
    released = serializers.DateField(input_formats=["%d %b %Y"], allow_null=True)
    dvd = serializers.DateField(input_formats=["%d %b %Y"], allow_null=True)

    def to_internal_value(self, data):
        if data.get("runtime") and data["runtime"]:
            result = re.search(NUMBER_PATTERN, data["runtime"])
            if result:
                data["runtime"] = int(result.group())
            else:
                data["runtime"] = None

        if data.get("rating") and data["rating"]:
            result = re.search(FLOAT_NUMBER_PATTERN, data["rating"])
            if result:
                data["rating"] = float(result.group())
            else:
                data["rating"] = None

        return super().to_internal_value(data)

    def get_or_create(self):
        defaults = self.validated_data.copy()
        title = defaults.pop("title")

        return Movie.objects.get_or_create(title=title, defaults=defaults)

    class Meta:
        model = Movie
        fields = (
            "id",
            "imdb_id",
            "title",
            "plot",
            "year",
            "runtime",
            "released",
            "dvd",
            "pg_rating",
            "rating",
            "genre",
            "language",
            "country",
            "director",
            "writer",
            "actors",
            "awards",
            "poster",
            "production",
            "website",
            "created_at",
        )
        extra_kwargs = {"title": {"validators": []}}


class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ("id", "movie", "body", "created_at")
