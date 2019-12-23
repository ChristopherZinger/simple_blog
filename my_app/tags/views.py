from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect , get_object_or_404
from django.template.defaultfilters import slugify
from . forms import TagForm
from . models import Tag
from post.models import Post, Images


@login_required
def tag_create(request):
    context = {}
    request.session['messages'] = 'Add tag'
    if request.method == 'POST':
        tag_form = TagForm(data=request.POST)
        try_slug = slugify(request.POST.get('title'))
        try_title = request.POST.get('title')
        #check if tag with this title or slug already exists
        exists = False if Tag.objects.filter(slug=try_slug).count() > 0 or Tag.objects.filter(title=try_title).count() > 0 else True
        if exists:
            # validate
            if tag_form.is_valid():
                tag = tag_form.save(commit=False)
                tag.slug = try_slug
                tag.save()
                return redirect('tags:tag_list')
            else:
                request.session['messages'] = 'Error occured. Tag was not saved because of invalid form.'
                return redirect('tags:tag_list')
        else:
            request.session['messages'] = 'Tag with this title or this slug already exists. Try different Title.'
            return render(request, 'tags/tag_create.html', {'tag_form':TagForm()})
    else:
        tag_form = TagForm()
        context.update({'tag_form':tag_form})
        return render(request, 'tags/tag_create.html', context)


def tag_detail(request, slug=None):
    tag = get_object_or_404(Tag, slug=slug)
    context = {'tag':tag}
    return render(request, 'tags/tag_detail.html', context)


@login_required
def tag_update(request,tag_id=None):
    context = {}
    tag = get_object_or_404(Tag, pk=tag_id)
    if request.method == 'POST':
        tag_form = TagForm(data=request.POST)
        try_slug = slugify(request.POST.get('title'))
        try_title = request.POST.get('title')
        exists = False if Tag.objects.filter(slug=try_slug).count() > 0 or Tag.objects.filter(title=try_title).count() > 0 else True
        if exists:
            if tag_form.is_valid():
                tag.title = try_title
                tag.slug = try_slug
                tag.save()
                return redirect('tags:tag_list')
            else:
                request.session['messages'] = 'Error occured. Tag was not saved because of invalid form.'
                return redirect('tags:tag_list')
        else:
            request.session['messages'] = 'Tag with this title or this slug already exists. Try different Title.'
            return render(request, 'tags/tag_create.html', {'tag_form':TagForm(initial={
            'title':tag.title,
            })})
    else:
        tag_form = TagForm(initial={
        'title':tag.title
        })
        context.update({'tag_form':tag_form})
        return render(request, 'tags/tag_create.html', context)
def tag_delete(request, tag_id=None):
    tag = get_object_or_404(Tag, pk=tag_id)
    tag.delete()
    return redirect('tags:tag_list')

def tag_list(request):

    tags = Tag.objects.all()
    context = {'tags':tags }
    return render(request, 'tags/tag_list.html', context)


@login_required
def add_tag_to_post(request, post_id=None, tag_id=None):
    post = get_object_or_404(Post, pk=post_id)
    tag = get_object_or_404(Tag, pk=tag_id)
    post.tags.add(tag)
    return redirect('post:post_update', post_id=post_id)

@login_required
def remove_tag_from_post(request, post_id=None, tag_id=None):
    post = get_object_or_404(Post, pk=post_id)
    tag = get_object_or_404(Tag, pk=tag_id)
    post.tags.remove(tag)
    return redirect('post:post_update', post_id=post_id)
