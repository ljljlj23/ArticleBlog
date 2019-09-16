from django.db import models
from ckeditor.fields import RichTextField

GENDER_LIST=(
    (1,'男'),
    (2,'女'),
)

class Author(models.Model):
    name = models.CharField(max_length=32,verbose_name='作者名')
    age = models.IntegerField(verbose_name='年龄')
    # 男1 女2
    gender = models.IntegerField(choices=GENDER_LIST,verbose_name='性别',default=1)
    email = models.CharField(max_length=32,verbose_name='邮箱')

    def __str__(self):
        return self.name

    class Meta:
        db_table='author'
        verbose_name = '作者'
        verbose_name_plural = verbose_name

class Type(models.Model):
    name = models.CharField(max_length=32,verbose_name='类型名')
    description = models.TextField(verbose_name='描述')

    def __str__(self):
        return self.name

    class Meta:
        db_table='type'
        verbose_name = '类型'
        verbose_name_plural = verbose_name

class Article(models.Model):
    title = models.CharField(max_length=32,verbose_name='文章标题')
    date = models.DateField(auto_now=True,verbose_name='发表时间')
    # content = models.TextField(verbose_name='内容')
    content = RichTextField()
    # description = models.TextField(verbose_name='描述')
    description = RichTextField()
    # 图片
    # upload_to 指定文件上传位置，static目录下的images中
    picture = models.ImageField(upload_to='images')
    # 推荐1 非推荐0
    recommend = models.IntegerField(verbose_name='推荐',default=0)
    # 点击率
    click = models.IntegerField(verbose_name='点击率',default=0)
    author = models.ForeignKey(to=Author,on_delete=models.SET_DEFAULT,default=1,verbose_name='作者')
    type = models.ManyToManyField(to=Type,verbose_name='类型')

    def __str__(self):
        return self.title

    class Meta:
        db_table='article'
        verbose_name='文章'
        verbose_name_plural=verbose_name

