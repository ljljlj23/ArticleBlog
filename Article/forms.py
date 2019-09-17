from django import forms

class Register(forms.Form):
    name = forms.CharField(required=True,label='姓名')
    password = forms.CharField(max_length=8,min_length=6,label='密码')

    # 固定写法
    def clean_name(self):
        '''
        自定义验证
        用户名不允许是admin
        '''
        name=self.cleaned_data.get('name')
        if name == 'admin':
            self.add_error('name','用户名不可以是admin')
        else:
            return name