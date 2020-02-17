from django.shortcuts import render, redirect

def redirect_to_login(request):
        return redirect("/welcome")