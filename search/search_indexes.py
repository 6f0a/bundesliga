from .models import Teams
from haystack import indexes 


class TeamsIndex(indexes.SearchIndex, indexes.Indexable):
    id = indexes.IntegerField(model_attr='id')
    text = indexes.EdgeNgramField(document=True, use_template=True)
    name = indexes.CharField(model_attr ='name')

    def get_model(self):
        return Teams
 
    def index_queryset(self, using=None):
        return self.get_model().objects.all()