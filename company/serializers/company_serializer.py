from rest_framework import serializers
from company.models.company_model import Company
from company.constants import CompanyType
from drf_writable_nested import WritableNestedModelSerializer
from drf_extra_fields.relations import PresentablePrimaryKeyRelatedField
from .shift_time_serializer import ShiftTimeSerializer


class ParentCompanyInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Company
        fields = [
            "id",
            "name",
        ]


class BranchSerializer(serializers.ModelSerializer):  # As company branch
    parent = PresentablePrimaryKeyRelatedField(
        queryset=Company.objects.all(),
        presentation_serializer=ParentCompanyInfoSerializer,
        required=False,
        allow_null=True,
    )

    class Meta:
        model = Company
        fields = "__all__"

    def validate_type(self, value):
        if not value:
            raise serializers.ValidationError("The branch type field is required.")
        elif value == CompanyType.COMPANY:
            raise serializers.ValidationError(
                "The branch type should be something other than company."
            )

        return value

    def to_internal_value(self, data):
        validated_data = super().to_internal_value(data)
        validated_data["type"] = CompanyType.BRANCH

        return validated_data


class CompanySerializer(WritableNestedModelSerializer):
    shifttimemodel_related = ShiftTimeSerializer(many=True, required=True)

    class Meta:
        model = Company
        fields = "__all__"
        
        extra_kwargs = {
            "established_at": {
                "required": True,
                "allow_null": False,
            },
        }

    def validate(self, attrs):
        validated_data = super().validate(attrs)

        # Ensure that a branch has a parent company
        if (
            "parent" not in validated_data
            or validated_data["parent"] is None
            and validated_data["type"] == CompanyType.BRANCH
        ):
            raise serializers.ValidationError(
                {"type": "The Branch must have a parent company."}
            )

        # Check is parent type is "branch" raise
        elif validated_data["type"] == CompanyType.BRANCH:
            company_type = (
                Company.objects.filter(pk=validated_data["parent"].id)
                .values_list("type", flat=True)
                .first()
            )
            if CompanyType.BRANCH == company_type:
                raise serializers.ValidationError(
                    {"type": "The Branch cannot have child branch."}
                )

        return super().validate(attrs)


class CompanyListSerializer(WritableNestedModelSerializer):
    shift_times = ShiftTimeSerializer(many=True, read_only=True)
    parent = PresentablePrimaryKeyRelatedField(
        queryset=Company.objects.all(),
        presentation_serializer=ParentCompanyInfoSerializer,
        required=False,
        allow_null=True,
    )

    class Meta:
        model = Company
        fields = "__all__"
        