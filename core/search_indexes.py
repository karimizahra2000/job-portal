# core/search_indexes.py
from django_elasticsearch_dsl import Document, Index, fields
from django_elasticsearch_dsl.registries import registry
from core.models import Job

job_index = Index('jobs')
job_index.settings(
    number_of_shards=1,
    number_of_replicas=0
)


@registry.register_document
class JobDocument(Document):
    employer = fields.ObjectField(properties={
        'id': fields.IntegerField(),
        'username': fields.TextField(),
    })

    class Index:
        name = 'jobs'  # اسم ایندکس در Elasticsearch

    class Django:
        model = Job
        fields = [
            'id',
            'title',
            'description',
            'status',
            'is_published',
            'created_at',
        ]
