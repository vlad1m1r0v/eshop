import copy

from rest_framework.serializers import ModelSerializer


class NonEmptySerializer(ModelSerializer):
    def to_representation(self, instance):
        representation = super().to_representation(instance)
        non_null_representation = copy.deepcopy(representation)
        for key in representation.keys():
            if not representation[key]:
                non_null_representation.pop(key)
        return non_null_representation
