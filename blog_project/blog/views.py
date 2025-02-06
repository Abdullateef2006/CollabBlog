from django.shortcuts import render
from django.http import HttpResponse
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.permissions import IsAuthenticated
from django.db.models import Q
from django.core.mail import send_mail
import requests
from django.urls import reverse
from django.shortcuts import render
from .models import *
from rest_framework.views import APIView
from .serializers import *
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404
from django.conf import settings
from rest_framework.decorators import api_view, permission_classes
from rest_framework.status import HTTP_200_OK, HTTP_400_BAD_REQUEST, HTTP_403_FORBIDDEN



class Category_api(APIView):
    def get(self, request):
            
        category = Category.objects.all()
        category_serializer = CategorySerializer(category, many=True)
        
        return Response({
            "data": category_serializer.data
        }, status=status.HTTP_200_OK)


class Review_api(APIView):
    def get(self, request):
            
        comments = Comments.objects.all()
        comments_serializer = CommentSerializer(comments, many=True)
        
        return Response({
            "data": comments_serializer.data
        }, status=status.HTTP_200_OK)

class Post_api(APIView):

    def get(self, request):
        courses = Post.objects.prefetch_related("category").all()
        category = Category.objects.all()

        post_serializer = PostSerializer(courses, many=True)
        category_serializers = CategorySerializer(category, many=True)

        return Response(
            {"post": post_serializer.data,
                "category": category_serializers.data},
            status=status.HTTP_200_OK,
        )




class Course_List_Category(APIView):

    def get(request, self, name):
        category = get_object_or_404(Category, name=name)
        post = Post.objects.prefetch_related("category").filter(category=category)
        categories = Category.objects.all()

        post_serializer = PostSerializer(post, many=True)
        categories_serializer = CategorySerializer(categories, many=True)

        return Response(
            {"course": post_serializer.data,
                "category": categories_serializer.data},
            status=status.HTTP_200_OK,
        )
        
        
class ProfileCreateEdit(APIView):
    serializer_class = ProfileSerializer
    
    def get(self, request):
        # Retrieve the profile for the logged-in user or 404 if not found
        profile = get_object_or_404(UserProfile, user=request.user)
        # Serialize the profile data
        profile_serializer = ProfileViewSerializer(profile)
        your_posts = Post.objects.filter(author = request.user) 
        post_serializer = PostSerializer(your_posts, many=True)
        
        return Response({"profile":profile_serializer.data, "post" : post_serializer.data}, status=status.HTTP_200_OK)

    def post(self, request):
        try:
            profile = UserProfile.objects.get(user=request.user)
            profile_serializer = ProfileSerializer(profile, data=request.data, partial=True)
        except UserProfile.DoesNotExist:
            profile_serializer = ProfileSerializer(data=request.data)
        
        if profile_serializer.is_valid():
            profile_serializer.save(user=request.user)  # Save with the current logged-in user
            return Response(profile_serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(profile_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request):
        # Retrieve the profile or return 404 if not found
        profile = get_object_or_404(UserProfile, user=request.user)
        # Partially update the profile
        profile_serializer = ProfileSerializer(profile, data=request.data, partial=True)
        
        if profile_serializer.is_valid():
            profile_serializer.save()  # Update the profile
            return Response(profile_serializer.data, status=status.HTTP_200_OK)
        return Response(profile_serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class PostCreateAPIView(APIView):
    serializer_class = PostSerializer

    permission_classes = [IsAuthenticated]  # Ensure only authenticated users can create posts
    
    def post(self, request):
        # The serializer expects the post data to include fields like title, content, author, and category
        serializer = PostSerializer(data=request.data)
        
        if serializer.is_valid():
            # Set the author field from the logged-in user
            serializer.save(author=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class Post_detail_api(APIView):
    serializer_class = CommentSerializer  # Set the serializer for comments
    
    def get(self, request, name, *args, **kwargs):
        """
        Handle retrieving a post's details and its comments.
        """
        try:
            # Get the post by title
            post = Post.objects.get(title=name)
        except Post.DoesNotExist:
            return Response({"error": "Post not found."}, status=status.HTTP_404_NOT_FOUND)

        # Filter comments specific to the post
        comments = Comments.objects.filter(post=post)

        # Serialize the post and comments
        post_serializer = PostSerializer(post)
        comments_serializer = CommentSerializer(comments, many=True)

        try:
            # Fetch the user profile for additional logic
            profile = UserProfile.objects.get(user=request.user)
        except UserProfile.DoesNotExist:
            return Response({"error": "User profile not found."}, status=status.HTTP_404_NOT_FOUND)

        # Example of profile-specific logic (Uncomment and adjust based on your requirement)
        # if profile.status == "Regular":
        #     return Response(
        #         {"data": "You are a regular user. Premium features are limited."},
        #         status=status.HTTP_403_FORBIDDEN
        #     )

        return Response(
            {
                "post": post_serializer.data,
                "comments": comments_serializer.data,
            },
            status=status.HTTP_200_OK
        )

    def post(self, request, name, *args, **kwargs):
        """
        Handle creating a new comment for a post.
        """
        # Get the post or return 404 if not found
        post = get_object_or_404(Post, title=name)

        # Extract comment data from the request
        comment_data = {
            "content": request.data.get("content")  # Assuming content is the comment body
        }

        # Create the comment serializer instance and pass the 'request' object through context
        comment_serializer = CommentSerializer(data=comment_data, context={'request': request})

        # Check if the data is valid
        if comment_serializer.is_valid():
            # Manually add the post and user before saving
            comment_serializer.validated_data['post'] = post
            comment_serializer.validated_data['user'] = request.user
            
            # Save the valid comment data
            comment_serializer.save()

            return Response(
                comment_serializer.data, status=status.HTTP_201_CREATED
            )
        
        # If invalid data, return errors
        return Response(
            comment_serializer.errors, status=status.HTTP_400_BAD_REQUEST
        )



            
         



class CommentListCreateView(APIView):
    """
    API View to list and create comments for a specific post.
    """
    serializer_class  = CommentSerializer

    def get(self, request, name):
        """
        List all comments for a specific post.
        """
        post = get_object_or_404(Post, title=name)  # Ensure post exists
        comments = post.comments.all()  # Fetch all comments for this post (via related_name)
        serializer = CommentSerializer(comments, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request, name):
        """
        Create a new comment for a specific post.
        """
        post = get_object_or_404(Post, title=name)  # Ensure post exists
        data = request.data.copy()  # Make a mutable copy of request data
        data['post'] = post.title  # Assign post ID to the new comment
        serializer = CommentSerializer(data=data)

        if serializer.is_valid():
            serializer.save()  # Save the comment
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)




class SendInvitationView(APIView):
    """
    Send an invitation to an external user to contribute to a post.
    """
    permission_classes = [IsAuthenticated]
    serializer_class  = InvitationEmailSerializer

    def post(self, request, name):
        post = get_object_or_404(Post, title=name)

        # Ensure the user is the author of the post
        if post.author != request.user:
            return Response(
                {"error": "You don't have permission to invite contributors for this post."},
                status=status.HTTP_403_FORBIDDEN,
            )

        # Validate the email using the serializer
        serializer = InvitationEmailSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        email = serializer.validated_data['email']

        # Create the invitation
        invitation = Invitation.objects.create(post=post, email=email, invited_by=request.user)
        invitation_link = f"{request.scheme}://{request.get_host()}/api/accept_invitation/{invitation.token}/"
        
        # Send the email invitation
        # send_mail(
        #     subject="You've been invited to contribute!",
        #     message=f"Click here to accept the invitation: {invitation_link}",
        #     from_email=request.user.email,
        #     recipient_list=[email],
        # )

        return Response(
            {
                "message": "Invitation sent successfully!",
                "link": invitation_link,
            },
            status=status.HTTP_200_OK,
        )
   
    
        


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def send_invitation(request, post_id):
    """
    Send an invitation to an external user to contribute to a post.
    """
    user = request.user
    post = get_object_or_404(Post, id=post_id)

    if post.author != user:
        return Response({"error": "You don't have permission to invite contributors for this post."}, status=HTTP_403_FORBIDDEN)

    email = request.data.get('email')
    if not email:
        return Response({"error": "Email is required."}, status=HTTP_400_BAD_REQUEST)

    invitation = Invitation.objects.create(post=post, email=email, invited_by=user)
    invitation_link = f"{request.scheme}://{request.get_host()}/api/accept_invitation/{invitation.token}/"

    # Send email
    send_mail(
        subject="You've been invited to contribute!",
        message=f"Click here to accept the invitation to contribute: {invitation_link}",
        from_email=request.user.email,
        recipient_list=[email],
    )

    return Response({"message": "Invitation sent successfully!", "link": invitation_link}, status=HTTP_200_OK)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def accept_invitation(request, token):
    """
    Accept an invitation and add the user as a contributor to the post.
    """
    invitation = get_object_or_404(Invitation, token=token)

    if invitation.accepted:
        return Response({"error": "Invitation already accepted."}, status=HTTP_400_BAD_REQUEST)

    invitation.post.contributors.add(request.user)
    invitation.accepted = True
    invitation.save()

    return Response({"message": f"You are now a contributor to the post: {invitation.post.title}"}, status=HTTP_200_OK)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def list_contributors(request, name):
    """
    List all contributors of a post.
    """
    post = get_object_or_404(Post, title=name)

    if request.user != post.author and request.user not in post.contributors.all():
        return Response({"error": "You don't have permission to view this post's contributors."}, status=HTTP_403_FORBIDDEN)

    contributors = post.contributors.all()
    serializer = ContributorSerializer(contributors, many=True)

    return Response(serializer.data, status=HTTP_200_OK)




from .permissions import IsAuthorOrContributor


class EditPostView(APIView):
    """
    Edit a post (only allowed for contributors and the author of the post).
    """
    permission_classes = [IsAuthenticated, IsAuthorOrContributor]
    serializer_class = PostSerializer  # Specify the serializer to validate and save post data

    def patch(self, request, name):
        """
        Edit the post with partial updates (PATCH request).
        """
        # Fetch the post by its title (slug or ID can also be used depending on requirements)
        post = get_object_or_404(Post, title=name)

        # Check custom permission
        self.check_object_permissions(request, post)

        # Use the serializer to validate and update post data
        serializer = self.serializer_class(post, data=request.data, partial=True)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        # Save and return the updated post
        serializer.save()
        return Response(
            {
                "message": "Post updated successfully.",
                "post": serializer.data,
            },
            status=status.HTTP_200_OK,
        )



class SubscriptionView(APIView):
    serializer_class = SubscriptionSerializer
    """
    Handle creating a new subscription to the newsletter.
    """
    def post(self, request, *args, **kwargs):
        # Extract email from the request data
        email = request.data.get("email")

        # Check if an email already exists
        if Subscription.objects.filter(email=email).exists():
            return Response({"error": "This email is already subscribed!"}, status=status.HTTP_400_BAD_REQUEST)

        # Optionally: Link the subscription to the authenticated user (if logged in)
        user = request.user if request.user.is_authenticated else None

        # Create the subscription data without the user field in the serializer
        subscription_data = {
            "email": email,
            "user": user,  # The user is set here even though it's not in the serializer fields
        }
        

        # Create the serializer instance
        serializer = SubscriptionSerializer(data=subscription_data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CreatorProfileAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, id):
        profile = get_object_or_404(UserProfile, id=id)
        posts = Post.objects.filter(author=profile.user)
        
        profile_serializer = ProfileViewSerializer(profile)
        post_serializer = PostSerializer(posts, many=True)
        
        return Response({
            'profile': profile_serializer.data,
            'posts': post_serializer.data
        })
