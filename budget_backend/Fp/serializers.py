from rest_framework import serializers
from .models import *
from budget_backend.models import User

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = "__all__"

class FollowSerializer(serializers.ModelSerializer):
    class Meta:
        model = Follow
        fields = "__all__"
    def to_representation(self, instance):
        self.fields['followed_user'] = UserSerializer(read_only = True);
        self.fields['following_user'] = UserSerializer(read_only = True);
        return super(FollowSerializer, self).to_representation(instance)
    

class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = "__all__"
    def to_representation(self, instance):
        self.fields['commenter'] = UserSerializer(read_only = True);
        return super(CommentSerializer, self).to_representation(instance)

class PlanSerializer(serializers.ModelSerializer):
    class Meta:
        model = Plan
        fields = "__all__"
    def to_representation(self, instance):
        self.fields['owner'] = UserSerializer(read_only = True);
        return super(PlanSerializer, self).to_representation(instance)

class ParentChildCommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = ParentChildComment
        fields = "__all__"

class PlanCommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = PlanComment
        fields = "__all__"
    def to_representation(self, instance):
        self.fields['parent_plan'] = PlanSerializer(read_only = True);
        self.fields['child_comment'] = CommentSerializer(read_only = True);
        return super(PlanCommentSerializer, self).to_representation(instance)
    

