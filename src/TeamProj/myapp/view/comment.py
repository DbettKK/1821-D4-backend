from rest_framework.views import APIView, Response
from myapp.models import User, File, UserBrowseFile, UserKeptFile, Team, Comment, Message, Agree, Disagree
from myapp.serializers import CommentSer
from myapp.views import chk_token
from .userfile import chk_file_id


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
        # 创建评论的同时，创建类型为comment的消息,发送给文件的创建人
        Message.objects.create(
            user=f.creator,
            msg_type='comment',
            msg_title='评论消息',
            msg_content='用户 ' + u.username + ' 评论了您的文档 ' + f.file_title + '!',
            msg_typr_from=f.id,
            msg_person_from=user_id
        )
        print(c)
        return Response({
            'info': 'success',
            'code': 200,
            'data': CommentSer(c).data
        }, status=200)


class GetComments(APIView):
    def get(self, request):
        token = request.META.get('HTTP_TOKEN')
        file_id = request.GET.get('file_id')
        user_id = chk_token(token)
        if isinstance(user_id, Response):
            return user_id
        u = User.objects.get(pk=user_id)
        f = chk_file_id(file_id)
        if isinstance(f, Response):
            return f
        c = Comment.objects.filter(file=f)
        return Response({
            'info': 'success',
            'code': 200,
            'data': CommentSer(c, many=True).data
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


class UserAgree(APIView):
    def get(self, request):
        token = request.META.get('HTTP_TOKEN')
        comment_id = request.GET.get('comment_id')
        user_id = chk_token(token)
        if isinstance(user_id, Response):
            return user_id
        u = User.objects.get(pk=user_id)
        c = Comment.objects.get(pk=comment_id)
        if Agree.objects.filter(person=u, comment=c):
            return Response({
                'info': '你已经点过赞了',
                'code': 403
            }, status=403)
        Agree.objects.create(
            person=u,
            comment=c
        )
        return Response({
            'info': 'success',
            'code': 200
        }, status=200)


class UserDisagree(APIView):
    def get(self, request):
        token = request.META.get('HTTP_TOKEN')
        comment_id = request.GET.get('comment_id')
        user_id = chk_token(token)
        if isinstance(user_id, Response):
            return user_id
        u = User.objects.get(pk=user_id)
        c = Comment.objects.get(pk=comment_id)
        if Disagree.objects.filter(person=u, comment=c):
            return Response({
                'info': '你已经踩过了',
                'code': 403
            }, status=403)
        Disagree.objects.create(
            person=u,
            comment=c
        )
        return Response({
            'info': 'success',
            'code': 200
        }, status=200)


class GetNum(APIView):
    def get(self, request):
        token = request.META.get('HTTP_TOKEN')
        comment_id = request.GET.get('comment_id')
        user_id = chk_token(token)
        if isinstance(user_id, Response):
            return user_id
        c = Comment.objects.get(pk=comment_id)
        a_num = Agree.objects.filter(comment=c).count()
        d_num = Disagree.objects.filter(comment=c).count()
        return Response({
            'info': 'success',
            'code': 200,
            'data': {
                'agree': a_num,
                'disagree': d_num
            }
        }, status=200)
