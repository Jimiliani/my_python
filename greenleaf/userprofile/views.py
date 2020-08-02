from django.shortcuts import render


def profileViewWithId(request, userId):
    return render(request, 'userprofile/userNotFound.html')
