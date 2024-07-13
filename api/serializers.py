from rest_framework import serializers

from users.models import User, Librarian, Member


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            "username",
            "email",
            "password",
            "first_name",
            "last_name",
            "is_staff",
        ]
        extra_kwargs = {"password": {"write_only": True}}  # Hide password from response

    def update(self, instance, validated_data):
        partial = self.context.get("is_partial", False)
        return serializers.ModelSerializer.update(
            self, instance, validated_data, partial=partial
        )


class LibrarianSerializer(serializers.ModelSerializer):
    user_detail = UserSerializer(source="user")

    class Meta:
        model = Librarian
        fields = ["user_detail", "picture", "created_at", "updated_at"]

    def create(self, validated_data):
        user_data = validated_data.pop("user")
        user_data["is_staff"] = True
        user = User.objects.create_user(**user_data)

        librarian = Librarian.objects.create(user=user, **validated_data)
        return librarian

    def update(self, instance, validated_data):
        instance.user.username = validated_data.get("user", instance.user).get(
            "username", instance.user.username
        )
        instance.user.email = validated_data.get("user", instance.user).get(
            "email", instance.user.email
        )
        instance.user.first_name = validated_data.get("user", instance.user).get(
            "first_name", instance.user.first_name
        )
        instance.user.last_name = validated_data.get("user", instance.user).get(
            "last_name", instance.user.last_name
        )
        instance.user.is_staff = validated_data.get("user", instance.user).get(
            "is_staff", instance.user.is_staff
        )

        instance.picture = validated_data.get("picture", instance.picture)
        instance.created_at = validated_data.get("created_at", instance.created_at)
        instance.updated_at = validated_data.get("updated_at", instance.updated_at)

        user = User.objects.filter(id=instance.user.id)
        user.update(
            username=instance.user.username,
            email=instance.user.email,
            first_name=instance.user.first_name,
            last_name=instance.user.last_name,
            is_staff=instance.user.is_staff,
        )
        Librarian.objects.filter(id=instance.id).update(user=user[0])
        instance.save()
        return instance


class MemberSerializer(serializers.ModelSerializer):
    user_detail = UserSerializer(source="user")

    class Meta:
        model = Member
        fields = ["user_detail", "picture", "created_at", "updated_at"]

    def create(self, validated_data):
        user_data = validated_data.pop("user")
        user_data["is_staff"] = False
        user = User.objects.create_user(**user_data)

        member = Member.objects.create(user=user, **validated_data)
        return member

    def update(self, instance, validated_data):
        instance.user.username = validated_data.get("user", instance.user).get(
            "username", instance.user.username
        )
        instance.user.email = validated_data.get("user", instance.user).get(
            "email", instance.user.email
        )
        instance.user.first_name = validated_data.get("user", instance.user).get(
            "first_name", instance.user.first_name
        )
        instance.user.last_name = validated_data.get("user", instance.user).get(
            "last_name", instance.user.last_name
        )
        instance.user.is_staff = validated_data.get("user", instance.user).get(
            "is_staff", instance.user.is_staff
        )

        instance.picture = validated_data.get("picture", instance.picture)
        instance.created_at = validated_data.get("created_at", instance.created_at)
        instance.updated_at = validated_data.get("updated_at", instance.updated_at)

        user = User.objects.filter(id=instance.user.id)
        user.update(
            username=instance.user.username,
            email=instance.user.email,
            first_name=instance.user.first_name,
            last_name=instance.user.last_name,
            is_staff=instance.user.is_staff,
        )
        Member.objects.filter(id=instance.id).update(user=user[0])
        instance.save()
        return instance
