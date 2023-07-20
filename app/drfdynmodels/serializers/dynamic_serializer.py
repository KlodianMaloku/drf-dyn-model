from rest_framework import serializers

def create_dynamic_serializer(model):
    """
    Create a serializer class for a dynamic model.

    Args:
        model: The dynamic model class.

    Returns:
        A ModelSerializer subclass for the dynamic model.
    """

    # Get a list of field names from the model
    field_names = [f.name for f in model._meta.get_fields()]

    # Create Meta class
    meta = type('Meta', (), {'model': model, 'fields': field_names})

    # Create serializer class
    dynamic_model_serializer = type(
        'DynamicModelSerializer',
        (serializers.ModelSerializer,),
        {'Meta': meta}
    )

    return dynamic_model_serializer
