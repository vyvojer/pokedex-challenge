from django.db.models import QuerySet


class PokemonQuerySet(QuerySet):
    """
    Custom QuerySet for the Pokemon model.
    """

    def prefetched(self):
        """
        Returns a queryset with prefetched related objects.

        Returns:
            QuerySet: A queryset with prefetched related objects.
        """
        return self.prefetch_related("types", "abilities")
