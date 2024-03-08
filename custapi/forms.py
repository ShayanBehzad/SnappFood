from django import forms
from .models import Comment



# this class is not connected to anything
class CommentForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance:
            author = self.instance.author
        else:
            author = None
        if author:
            self.fields['order'] = author.order_set.all()
    
    class Meta:
        model = Comment
        fields = '__all__'