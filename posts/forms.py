from django import forms

from posts.models import Post, Comment


class EditPostForm(forms.ModelForm):
    class Meta:
        model=Post
        fields = ('title','content','picture_content','creator','post_tag','section_topic')



class CreatePostForm(forms.ModelForm):
    class Meta:
        model=Post
        fields = ('title','content','picture_content','post_tag','section_topic')




class CheckPostForm(forms.ModelForm):
    class Meta:
        model=Post
        fields = ("is_published",)

class CommentForm(forms.ModelForm):
    class Meta:
        model=Comment
        fields = ("comment",)
