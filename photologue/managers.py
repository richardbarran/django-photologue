from django.db.models.query import QuerySet


class PhotoQuerySet(QuerySet):

    def is_public(self):
        """Trivial filter - will probably become more complex as time goes by!"""
        return self.filter(is_public=True)
