from rest_framework.views import APIView, Response
from myapp.models import User, File, UserBrowseFile, UserKeptFile, Team, Comment
from myapp.serializers import CommentSer
from myapp.views import chk_token
from .userfile import chk_file_id
from django.conf import settings
import os


class CommentFile(APIView):
    def post(self, request):
        token = request.META.get('HTTP_TOKEN')
        file_id = request.POST.get('file_id')
        comment = request.POST.get('comment')
        print(token)
        print(comment)
        user_id = chk_token(token)
        if isinstance(user_id, Response):
            return user_id
        u = User.objects.get(pk=user_id)

        f = chk_file_id(file_id)
        if isinstance(f, Response):
            return f
        c = Comment.objects.create(person=u, file=f, content=comment)
        # c = Comment.objects.filter(person=u, file=f, content=comment).get(0)

        print(c)
        return Response({
            'info': 'success',
            'code': 200,
            'data': CommentSer(c).data
        }, status=200)


# class GetImg(APIView):
#     def post(self, request):
#         token = request.META.get('HTTP_TOKEN')
#         img = request.FILES.get('img')
#         user_id = chk_token(token)
#         print(img)
#         if isinstance(user_id, Response):
#             return user_id
#         u = User.objects.get(pk=user_id)
#         ext = os.path.splitext(img.name)[1]
#         img_name = '%s/%s' % (settings.MEDIA_ROOT, img.name)
#         picname = img_name.split(".")[0] + "." + ext
#         print(ext)
#         print(img_name)
#         print(picname)
#         with open(picname, 'wb') as pic:
#             for c in img.chunks():
#                 pic.write(c)
#         print("picture OK", picname)
#         post_pic = str(picname.split("/")[1])


