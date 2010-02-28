from django.core.management.base import NoArgsCommand


class Command(NoArgsCommand):
    help = " Prints all models in project and how many objects of each model is present in database "
    requires_model_validation = True

    def handle_noargs(self, **options):
        from django.db.models import get_models
        
        lines = []

        for model in get_models():
            lines.append( "model: %s, objects in database: %s" % (model.__name__, model._default_manager.count()) )

        return "\n".join(lines)
