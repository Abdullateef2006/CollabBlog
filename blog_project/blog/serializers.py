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
        fields = ['id','slug', 'title', 'content', 'author', 'contributors', 'is_premium', 'category', 'published_date', 'views']
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


from rest_framework import serializers
from django.contrib.auth.models import User
from .models import UserProfile

class UserRegisterSerializer(serializers.ModelSerializer):
    """
    Serializer for registering a new user.
    """
    password = serializers.CharField(write_only=True, required=True, style={'input_type': 'password'})
    confirm_password = serializers.CharField(write_only=True, required=True, style={'input_type': 'password'})

    class Meta:
        model = User
        fields = ['username', 'email', 'password', 'confirm_password']

    def validate(self, data):
        """
        Ensure the passwords match.
        """
        if data['password'] != data['confirm_password']:
            raise serializers.ValidationError({"password": "Passwords do not match."})
        return data

    def create(self, validated_data):
        """
        Create a new user instance.
        """
        validated_data.pop('confirm_password')  # Exclude `confirm_password` as it's not part of the model
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            password=validated_data['password']
        )
        return user


# class UserProfileSerializer(serializers.ModelSerializer):
#     """
#     Serializer for the UserProfile model.
#     """
#     user = serializers.StringRelatedField(read_only=True)  # Display username instead of User ID

#     class Meta:
#         model = UserProfile
#         fields = ['user', 'status']

class TrendingPostSerializer(serializers.ModelSerializer):
    comment_count = serializers.IntegerField(read_only=True)

    class Meta:
        model = Post
        fields = ['id', 'title', 'slug', 'content', 'author', 'views', 'comment_count', 'published_date']
