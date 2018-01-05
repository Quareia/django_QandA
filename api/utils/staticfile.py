from django.http import HttpResponse


def get_ans_img(request, name):
    file = open('media/' + name, 'rb')
    response = HttpResponse(content=file)
    response['Content-Type'] = 'img'
    return response


def get_user_img(request, name):
    file = open('media/' + name, 'rb')
    response = HttpResponse(content=file)
    response['Content-Type'] = 'img'
    return response
