from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

from users.models import User, Librarian, Member, LibrarianLoginHistory


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            "id",
            "username",
            "email",
            "password",
            "first_name",
            "last_name",
            "is_staff",
        ]

    def create(self, validated_data):
        password = validated_data.get("password")
        print(validated_data)
        user = User.objects.create(**validated_data)
        user.set_password(password)
        user.save()

        return user

    def update(self, instance, validated_data):
        partial = validated_data.get("is_partial", False)
        return serializers.ModelSerializer.update(self, instance, validated_data)


class LoginHistorySerializer(serializers.ModelSerializer):
    class Meta:
        model = LibrarianLoginHistory
        fields = "__all__"


class LibrarianSerializer(serializers.ModelSerializer):
    user = UserSerializer()

    class Meta:
        model = Librarian
        fields = ["id", "user", "picture", "created_at", "updated_at"]

    def create(self, validated_data):
        user_data = validated_data.pop("user")
        user_data["is_staff"] = True
        username = user_data.get("username")
        email = user_data.get("email")

        is_username = User.objects.filter(username=username)
        is_email = User.objects.filter(email=email)

        if is_username.exists() and is_email.exists():
            raise serializers.ValidationError("Username or Email is already exists")

        user = User.objects.create_user(**user_data)
        user.set_password(user_data.get("password"))
        user.save()

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
    user = UserSerializer()

    class Meta:
        model = Member
        fields = ["id", "user", "picture", "created_at", "updated_at"]

    def create(self, validated_data):
        user_data = validated_data.pop("user")
        user_data["is_staff"] = False
        username = user_data.get("username")
        email = user_data.get("email")

        is_username = User.objects.filter(username=username)
        is_email = User.objects.filter(email=email)

        if is_username.exists() and is_email.exists():
            raise serializers.ValidationError("Username or Email is already exists")

        user = User.objects.create_user(**user_data)
        user.set_password(user_data.get("password"))
        user.save()

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


class TokenSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        token["user_id"] = user.id
        return token
