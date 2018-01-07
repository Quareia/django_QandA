from django.http import HttpResponse


def get_img(request, name):
    file = open('media/' + name, 'rb')
    response = HttpResponse(content=file)
    response['Content-Type'] = 'img'
    return response

