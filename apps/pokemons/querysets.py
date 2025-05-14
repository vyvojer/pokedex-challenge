from django.db.models import QuerySet


class PokemonQuerySet(QuerySet):
    def prefetched(self):
        return self.prefetch_related("types")
