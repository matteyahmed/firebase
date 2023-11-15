from django.contrib.auth import login

from rest_framework import permissions, status

from rest_framework.views import APIView, Response
from knox.views import LoginView as KnoxLoginView
from rest_framework.authtoken.serializers import AuthTokenSerializer


from .serializers import AuthSerializer

from firebase_admin import db, storage
from firebase_admin import auth, exceptions





class LoginView(KnoxLoginView):
    serializer = AuthSerializer
    permission_classes = (permissions.AllowAny,)

    def post(self, request, format=None):
        serializer = AuthTokenSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        user.email = request.data.get('email')
        login(request, user)
        return super(LoginView, self).post(request, format=None)

         # if authentication is successful
        # if response.status_code == 200:
        #     if user.username:
        #         # Assuming you have a 'firebase_uid' field in your user model
        #         firebase_uid = user.firebase_uid if user.firebase_uid else user.id

        #         # Check if the Firebase user with the given UID already exists
        #         try:
        #             firebase_user = auth.get_user(firebase_uid)
        #         except exceptions.AuthError as e:
        #             # User does not exist, proceed with creating the Firebase user
        #             if 'USER_NOT_FOUND' in str(e):
        #                 # Set a dummy email if the user doesn't have a valid email
        #                 if not user.email:
        #                     email = f"{user.username}@samaidha.com"
        #                 else:
        #                     email = user.email

        #                 # Create a Firebase user with a dummy email and emailVerified set to True
        #                 firebase_user = auth.create_user(
        #                     uid=firebase_uid,
        #                     email=email,
        #                     email_verified=True,
        #                 )

        #                 custom_token = auth.create_custom_token(firebase_uid)

        #                 # Add Firebase custom token to the response data
        #                 response.data['firebase_custom_token'] = custom_token
        #             else:
        #                 # Handle other AuthError exceptions if needed
        #                 response.data['error'] = 'Error creating Firebase user'
        #     else:
        #         # Handle the case where the user does not have a valid username
        #         response.data['error'] = 'Invalid username'

        # return response
 
    
class PostBlog(APIView):
    def post(self, request, format=None):
        user = request.user
        form_data = request.data

        blog_name = form_data.get('blog_name')
        blog_body = form_data.get('blog_body')
        image = request.FILES.get('image')  # Assuming 'image' is the key for the image in the request data

        # Upload the image to Firebase Storage
        image_url = self.upload_image(blog_name, image)

        # Save blog data to Firebase Realtime Database
        user_id = user.id
        ref = db.reference(f"users/{user_id}/blogs")

        new_blog_ref = ref.push({
            "author": user_id,
            'blog_name': blog_name,
            'blog_body': blog_body,
            'image_url': image_url  # Add the image URL to the blog data
            # Other blog data can be added here
        })

        return Response({'message': 'Blog posted successfully'}, status=status.HTTP_201_CREATED)

    def upload_image(self, blog_name, image):
        # Get a reference to the Firebase Storage bucket
        bucket = storage.bucket()

        # Define the path to store the image in Firebase Storage
        storage_path = f"images/{blog_name}/{image.name}"

        # Upload the image to Firebase Storage
        blob = bucket.blob(storage_path)
        blob.upload_from_file(image.file)

        # Return the public URL of the uploaded image
        return blob.public_url
# class PostBlog(APIView):
#     def post(self, request, format=None):
#         user = request.user
#         form_data = request.data

#         blog_name = form_data.get('blog_name')
#         blog_body = form_data.get('blog_body')

#         user_id = user.id

#         ref = db.reference(f"users/{user_id}/blogs")

#         new_blog_ref = ref.push({
#             "author": user_id,
#             'blog_name': blog_name,
#             'blog_body': blog_body
#             # Other blog data can be added here
#         })
        
#         return Response({'message': 'Blog posted successfully'}, status=status.HTTP_201_CREATED)
    

    
class getData(APIView):
    def get(self, request, format=None):
        user_id = request.user.id

        try:
            # ref = db.reference(f"users/{user_id}/blogs")
            ref = db.reference(f"users/")

            data = ref.get()

            if data:
                return Response(data, status=200)
            else:
                return Response("No data found", status=404)
            
        except Exception as e:
            # Handle exceptions, such as database access errors
            return Response(str(e), status=500)
        
                # Retrieve blogs for the current user
# class GetAllBlogs(APIView):
#     def get(self, request, format=None):
#         try:
#             # Get a reference to the 'users' node in the database
#             users_ref = db.reference('users')

#             all_blogs = {}
#             # Loop through all user IDs
#             for user_id in users_ref.get():
#                 # Get a reference to the blogs for each user
#                 user_blogs_ref = users_ref.child(user_id).child('blogs')
#                 # Retrieve blogs for the current user
#                 user_blogs = user_blogs_ref.get()

#                 # Store the user's blogs in the all_blogs dictionary
#                 all_blogs[user_id] = user_blogs

#             if all_blogs:
#                 return Response(all_blogs, status=200)
#             else:
#                 return Response("No blogs found for any user", status=404)

#         except Exception as e:
#             return Response(str(e), status=500)
