

# Create your views here.
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect , get_object_or_404
from django.template.defaultfilters import slugify
from django.views.generic import (
    ListView, DetailView, CreateView, UpdateView, DeleteView, TemplateView
)

from accounts.models import User
from comments.forms import CommentForm
from comments.models import Comment
from django.conf import settings
from . models import Post, Topic, PostSeries, PostSection, Images, PostSection
from . import forms
from tags.models import Tag
import datetime


def post_list(request):
    # return conver image for post list
    def findCoverImg(post_list):
        img_array = []
        for post in post_list:
            cover_img=None
            for section in PostSection.objects.filter(post=post):
                if section.image:
                    cover_img =  section.image
                    break
            img_array.append( cover_img)
        return img_array

    # check if user want to brawser justperticula topic
    # it will prowide 'topic' value in url
    context = {}

    # check if perticular topic needs to be filtered
    if 'topic' in request.GET :
        topic = request.GET.get('topic')
        if Topic.objects.filter(slug=topic).exists():
            topic = Topic.objects.get(slug=topic)
            context['topic'] = topic
            post_list = Post.objects.filter(is_published=True, topic=topic)
            images = findCoverImg(post_list) # cover images
            context['post_list'] = zip(post_list, images)
            return render(request, "post/post_list.html", context,)
    # return all published posts
    post_list = Post.objects.filter(is_published=True,)
    images = findCoverImg(post_list) # cover images
    context['post_list'] = zip(post_list, images)
    # print(context)
    return render(request, "post/post_list.html", context,)

@login_required
def post_create(request):
    if request.user.is_staff:
        if request.method == 'POST': #POST
            #get data form request
            post_form = forms.PostForm(data=request.POST)
            # img_form = forms.ImgForm(request.POST, request.FILES)
            title = request.POST.get('title')
            if post_form.is_valid():
                    #post save
                post = post_form.save()
                # if img_form.is_valid():
                #     #save img
                #     img = img_form.save(commit=False)
                #     img.post = get_object_or_404(Post, pk=post.id)
                #     if 'image' in request.FILES:
                #         img.image = request.FILES['image']
                #         img.save()
                #     else:
                #         print(img_form.errors, post_form.errors)
                # return to home page
                return redirect('post:post_update', post_id=post.id)
                #return redirect('/')
            else:
                messages = post_form.errors
                request.session['messages'] = messages
                return render(request, 'post/post_create.html',  {
                'post_form':post_form,
                # 'img_form':img_form,
            })
        else: #GET
            post_form = forms.PostForm()
            # img_form = forms.ImgForm()
            return render(request, 'post/post_create.html', {
                'post_form':post_form,
                # 'img_form':img_form,
            })
    else:
        request.session['messages'] = 'You need to be a admin to add a project.'
        return HttpResponseRedirect('/')

@login_required
def post_list_all(request):
    context = {}
    post_list = Post.objects.all()
    return render(request, 'post/post_list.html', {'post_list':post_list,})


@login_required
def post_update(request, post_id):
    post = get_object_or_404(Post, pk=post_id)
    context = {'post':post}
    if request.method == 'POST':
        #check if title already exists
        new_title = request.POST.get('title')
        if post.title != new_title: # check if titile is new
            if Post.objects.filter(title=new_title).exists() and Post.objects.get(title=new_title).id != post.id:
                request.session['messages'] += '<li>Post with the same title already exists. Try Another</li>'
                return redirect('post:post_update',  post_id=post_id)
            # check if slug already exists
            try_slug = slugify(new_title)
            post_already_exists = True if Post.objects.filter(slug=try_slug).count() > 0 else False
            test_nr = 0
            while post_already_exists:
                test_nr+=1
                test_slug = '{}-{}'.format(try_slug, test_nr)
                if Post.objects.filter(slug=test_slug).count() == 0:
                    try_slug=test_slug
                    break
            #save title and slug if they were updated
            post.slug = try_slug
            post.title = new_title
        #save rest of data
        post.subtitle = request.POST.get('subtitle')
        post.description = request.POST.get('description')
        post.topic =  Topic.objects.get(id=request.POST.get('topic'))
        post.save()

        '''
        structure of data in reuqest.POST:
        [
            # first reuqest gives: topic, susbtitle, desctiption ... and so on
            ..
            ('<int>-id=input',<int>),
            ('<int>-tag-input','<tag type>'),
            ('<int>-order=input',<int>),
            ('<int>-textarea-input','html of the post'),
            ... and so on
        ]
        '''
        print( PostSection.objects.filter(post=post) )
        # iterate through request.POST.items()
        sections_dict = {}
        temp_list, sections_text_list, sections_img_list = [], [], []
        for item in request.POST.items():

            try:
                current_id = int(item[0].split('-')[0])
            except:
                item = None
            if item != None:
                if current_id not in sections_dict.keys():
                    sections_dict[current_id] = {}
                record = sections_dict[current_id]
                key = item[0][(item[0].find('-') + 1):]
                value = item[1]
                record[key]=value

        # filter and remove sectinos that are not included in request.POST items
        for section in PostSection.objects.filter(post=post):
            if section.id not in sections_dict.keys():
                section.image.delete(save=True) if section.image != None else None
                section.delete()

        # save and update sections
        for section_id in sections_dict:
            new_section = sections_dict[section_id] # data to be saved
            try:
                post_section = PostSection.objects.get(id=section_id)
            except:
                post_section = PostSection(post=post)
            # save data common to img and paragraph type of sectino
            post_section.tag = new_section['tag-input']
            post_section.order = new_section['order-input']
            # check for images and save image
            if '{}-image-input'.format(section_id) in request.FILES:
                post_section.image = request.FILES['{}-image-input'.format(section_id)]
            else: # save text only if there is no image
                post_section.text = new_section['textarea-input']
            post_section.save()


        #confirm that model was saved and generate context for forms again
        post_form = forms.PostUpdateForm(initial={
            'title':post.title,
            'subtitle':post.subtitle,
            'description':post.description,
            'topic':post.topic,
        })
        context.update({"post_form":post_form})
        return redirect('post:post_update', post_id=post_id)
    else:
        tags_included = Tag.objects.filter(post=post)
        tags_excluded = Tag.objects.exclude(post=post)

        post_form = forms.PostUpdateForm(initial={
            'title':post.title,
            'subtitle':post.subtitle,
            'description':post.description,
            'topic':post.topic,

        })
        context.update({
            "post_form":post_form,
            'tags_included':tags_included,
            'tags_excluded':tags_excluded,
            'post':post,
            })

        return render(request, 'post/post_update.html', context)


@login_required
def post_publish(request, post_id=None):
    post = get_object_or_404(Post, pk=post_id)
    if post.publication_date == None:
        print('this post is not published')
        post.publication_date = datetime.datetime.now()
        post.is_published = True
        post.save()
        request.session['messages'] = 'Post Was Published: {}'.format(post.publication_date)
    else:
        request.session['messages'] = 'This post is already published'
    return redirect('post:post_update', post_id=post_id)

@login_required
def post_take_down(request, post_id=None):
    post = get_object_or_404(Post, pk=post_id)
    post.is_published = False
    post.save()
    request.session['messages'] = 'Post was taken down.'
    return redirect('post:post_update', post_id=post_id)

@login_required
def post_republish(request, post_id=None):
    post = get_object_or_404(Post, pk=post_id)
    post.is_published = True
    post.save()
    request.session['messages'] = 'Post was republished'
    return redirect('post:post_update', post_id=post_id)

@login_required
def post_delete(request, post_id=None):
    instance = get_object_or_404(Post, pk=post_id)
    instance.delete()
    print('post was deleted.')
    return redirect('index')

def post_detail(request, slug=None):
    post = get_object_or_404(Post, slug=slug)
    comments = Comment.objects.filter(post=post)
    context = {'post':post,'comments':comments}
    if request.method == 'POST' and request.user.is_authenticated:
        user = User.objects.get(pk=request.user.id)
        comment_form = CommentForm(request.POST)
        if comment_form.is_valid():
            comment = comment_form.save(commit=False)
            comment.post = post
            comment.author = user
            comment.save()
            request.session['messages'] = 'Your comment was saved successfully'
            return redirect('post:post_detail', slug=slug)
        else:
            request.session['messages'] = 'Error occured. Your comment was not saved.'
            return redirect('post:post_detail', slug=slug)
    else:
        comment_form = CommentForm()
        context.update({'comment_form':comment_form})
        return render(request, 'post/post_detail.html', context)
