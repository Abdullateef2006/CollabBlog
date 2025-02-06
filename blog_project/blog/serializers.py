from rest_framework import serializers
from .models import *
from django.contrib.auth.models import User
class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ["name", ]
        
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username']
        
class ContributorSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username', ]
        
# class PostSerializer(serializers.ModelSerializer):
#     category = CategorySerializer(many=True)
#     author = UserSerializer()
#     contributors = ContributorSerializer(many=True)
    
#     class Meta:
#         model = Post
#         fields = ['title', 'slug', 'content', 'author', 'category', 'is_premium', 'published_date', 'contributors',]
  
  


class PostSerializer(serializers.ModelSerializer):
    contributors = UserSerializer(many=True, read_only=True)  # Display contributors, but prevent updates
    author = UserSerializer(read_only=True)  # Author is read-only
    category = CategorySerializer(many=True)

    class Meta:
        model = Post
        fields = ['slug', 'title', 'content', 'author', 'contributors', 'is_premium', 'category', 'published_date']
        read_only_fields = ['slug', 'author', 'contributors', 'is_premium', 'published_date', ]

    def update(self, instance, validated_data):
        """
        Override update to restrict fields that can be modified.
        """
        # Only allow updates to title and content
        instance.title = validated_data.get('title', instance.title)
        instance.content = validated_data.get('content', instance.content)
        instance.save()
        return instance
        
class ProfileSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = UserProfile
        exclude = ['user', 'status', 'uu_id']
        read_only_fields = ['posts', ]

        
        
class ProfileViewSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    
    class Meta:
        model = UserProfile
        fields = "__all__"
        read_only_fields = ['posts', ]

        
        
class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comments
        fields = ['content', 'created_at']


    def create(self, validated_data):
        user = self.context['request'].user  # Fetch the user from the request context
        validated_data['user'] = user  # Ensure that the logged-in user is set
        
        # Save the comment
        return super().create(validated_data)

    
class InvitationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Invitation
        fields = ['id', 'token', 'post', 'email', 'invited_by', 'accepted', 'created']
        read_only_fields = ['token', 'invited_by', 'accepted', 'created']


        
        
        
from rest_framework import serializers
from .models import Invitation

class InvitationEmailSerializer(serializers.Serializer):
    email = serializers.EmailField()

    def validate_email(self, value):
        """
        Custom validation for the email field.
        """
        if not value:
            raise serializers.ValidationError("Email field cannot be empty.")
        return value


class SubscriptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Subscription
        fields = ['email', 'subscription_date']
