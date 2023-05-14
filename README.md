### django-rest-framework

django rest framework porject:
create a folder in pc: ```django-rest-framework```

open in vs code in terminal and create a virtual env: ```python3 -m venv drenv(drenv is our venv name)```

Now activate venv in terminal by, 
```source drenv/bin/activate(for mac)```
```drenv/Scripts/activate (for windows)```

Need to install django in venv: ```pip install django```

If pip upgrading needed: ```pip install --upgrade pip```

create a project of django by: ```django-admin startproject apiproject(our root app name)```

```cd apiproject```

```python3 manage.py migrate```

```python3 manage.py startapp myapp(app name)```

create a superuser: ```python3 manage.py createsuperuser(name,email,password) and app will start in 127.0.0.0/admijn```

```python3 manage.py runserver```

#### Creating a model: Now create a model inside myapp:

a. In root app (apiproject) in settings: add in ```INSTALLED_APP= ['myapp','rest_framework']```

b. in models.py of myapp create a model:```from django.db import models```

```
# Create your models here.

class Contact(models.Model):
    name = models.CharField(max_length=100, default='')
    title = models.CharField(max_length=200, default='')
    email = models.CharField(max_length=30, default='')
    
    def __str__(self):
        return self.name
```
c. go to admin.py of myapp and regiter this model:
```
from django.contrib import admin
from .models import Contact
# Register your models here.
admin.site.register(Contact)
```
d. close the terminal and open new. 
```
i) cd appproject 
j) python3 manage.py makemigrations [if error occurs: pip install djangorestframework
k)python3 manage.py migrate 
l) python3 manage.py runserver
```
Now we can add items in Model through admin url.

#### To add some data using serializers: 

(https://www.django-rest-framework.org/tutorial/1-serialization/#writing-regular-django-views-using-our-serializer):
We created model but it is needed to show in JSON data and serializer will do it for us.
Step 1. inside myapp create a file named setializers.py and add these lines of code:
```
from rest_framework import serializers
from myapp.models import Contact



class ContactSerializer(serializers.Serializer):
    name = serializers.CharField(max_length=100)
    title = serializers.CharField(max_length=200)
    email = serializers.EmailField(max_length=30)
    
    
    def create(self, validated_data):
        return Contact.objects.create(**validated_data)
    
    
    def update(self, instance, validated_data):
        instance.name = validated_data.get('name', instance.name)
        instance.title = validated_data.get('title', instance.title)
        instance.email = validated_data.get('email', instance.email)
       
        return instance
```
We add some data through shell.[In terminal]
```
cd apiproject
```
```
python3 manage.py runshell
```
Now copy this code in Notepad and edit according model and run it in terminal:
```
from snippets.models import Snippet [from myapp(app name).models import Contact(model class name)]
from snippets.serializers import SnippetSerializer[from myapp(app name).serializers import ContactSerializer(model class name)]
from rest_framework.renderers import JSONRenderer
from rest_framework.parsers import JSONParser
```
```
a = Contact(name= 'Another User', title="My new title", email="anoterhuser@email.com")
a.save()
```
Refresh the Model in admin Ui and a new user is created through shell.
Now want to get data in Json format:
In terminal shell:
```
serializer = SnippetSerializer(snippet) [serializer = ContactSerializer(a)]
```
```
serializer.data
```
content = JSONRenderer().render(serializer.data)
content
```
Output is in JSON format.
#### Now implement functionbased api view:
(https://www.django-rest-framework.org/tutorial/1-serialization/#writing-regular-django-views-using-our-serializer):
a) Now in myapp-> views.py paste the following code[got from above link]:
```
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.parsers import JSONParser
from myapp.models import Contact
from myapp.serializers import ContactSerializer
```
And:
```
@csrf_exempt
def snippet_list(request):
    if request.method == 'GET':
        apivar = Contact.objects.all()
        serializer = ContactSerializer(apivar, many=True)
        return JsonResponse(serializer.data, safe=False)

    elif request.method == 'POST':
        data = JSONParser().parse(request)
        serializer = ContactSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data, status=201)
        return JsonResponse(serializer.errors, status=400)
```
b) Now in myapp -> urls.py
```
from django.urls import path
from myapp import views

urlpatterns = [
    path('myapi/', views.snippet_list),
]
```
c) Finally add this url in root app(apiproject)
```
from django.urls import path, include 

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('myapp.urls')),
]
```
Done. ```http://127.0.0.1:8000/myapi/```. We get the JSON data
        
To get dynamic api value: 
Paste the following code in views.py of myapp:
```
@csrf_exempt
def api_detail(request, pk):
    try:
        detailVar = Contact.objects.get(pk=pk)
    except Contact.DoesNotExist:
        return HttpResponse(status=404)

    if request.method == 'GET':
        serializer = ContactSerializer(detailVar)
        return JsonResponse(serializer.data)

    elif request.method == 'PUT':
        data = JSONParser().parse(request)
        serializer = ContactSerializer(detailVar, data=data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data)
        return JsonResponse(serializer.errors, status=400)

    elif request.method == 'DELETE':
        detailVar.delete()
        return HttpResponse(status=204)    
  ```
  And add the following url in urls.py in myapp:
  ```
  urlpatterns = [
    path('myapi/', views.api_list),
    path('apidetails/<int:pk>/', views.api_detail),
]
```
Done. search in browser or Thender client of vs code in GET req: http://127.0.0.1:8000/apidetails/1/


### How to fix cors issue in django and vue side:

Django side:
a. ```pip install django-cors-headers```
b. In settings.py of root app:
``` INSTALLED_APPS = [
    'django.contrib.staticfiles',
    'rest_framework',
    'myapp',
    'vueapp',
    'corsheaders',
]
```
c.
```
MIDDLEWARE = [
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    "corsheaders.middleware.CorsMiddleware",
]
```
d. And add the following :
```
CORS_ALLOWED_ORIGINS = [
    "hhttp://localhost:3000",
]

CORS_ORIGIN_ALLOW_ALL = True

CORS_ALLOW_CREDENTIALS = True


CORS_ALLOW_METHODS = [
    "DELETE",
    "GET",
    "OPTIONS",
    "PATCH",
    "POST",
    "PUT",
]
CORS_ALLOW_HEADERS = [
    "accept",
    "accept-encoding",
    "authorization",
    "content-type",
    "dnt",
    "origin",
    "user-agent",
    "x-csrftoken",
    "x-requested-with",
]
```
It will fix the cors issues for connecting django-vue/react/angular.

#### In vue side:

Enable CORS in your Vue app:
Another way to fix CORS issues is to enable CORS in your Vue app. You can do this by adding the axios.defaults.withCredentials = true line to your Vue app's main.js file. This will enable cookies to be sent in CORS requests made by Axios.

```
// main.js

import Vue from 'vue'
import App from './App.vue'
import axios from 'axios'

Vue.config.productionTip = false

axios.defaults.withCredentials = true

new Vue({
  render: h => h(App),
}).$mount('#app')
```
### API View decorator:
We will work only in views.py in myapp deleting previous api code of myapp-> views.py
```
from django.shortcuts import render

# Create your views here.

from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.parsers import JSONParser
from myapp.models import Contact
from myapp.serializers import ContactSerializer

from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
```
And:
```
@api_view(['GET', 'POST'])
def api_list(request):
    """
    List all code snippets, or create a new snippet.
    """
    if request.method == 'GET':
        apivar = Contact.objects.all()
        serializer = ContactSerializer(apivar, many=True)
        return Response(serializer.data)

    elif request.method == 'POST':
        serializer = ContactSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
 ```
 And: 
 ```
 @api_view(['GET', 'PUT', 'DELETE'])
def api_detail(request, pk):
    try:
        detailVar = Contact.objects.get(pk=pk)
    except Contact.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = ContactSerializer(detailVar)
        return Response(serializer.data)

    elif request.method == 'PUT':
        serializer = ContactSerializer(detailVar, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        detailVar.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
 ```
 Now we can check http://127.0.0.1:8000/myapi/ and http://127.0.0.1:8000/apidetails/1
 
 ## Creating view by mixins and genric view(Most convenient) Whole app develop:
 * Need to fix in views.py and urls.py of myapp where root is apiproject:
 1) In views.py
 ```
 from django.shortcuts import render

# Create your views here.

from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.parsers import JSONParser
from myapp.models import Contact
from myapp.serializers import ContactSerializer

from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

from django.http import Http404
from rest_framework.views import APIView

from rest_framework import mixins
from rest_framework import generics
```
And:
```
class ContactList(generics.ListCreateAPIView, mixins.ListModelMixin, mixins.CreateModelMixin, generics.GenericAPIView):
    queryset = Contact.objects.all()
    serializer_class = ContactSerializer

    def get(self, request):
        return self.list(request)
    
    def post(self, request):
        return self.create(request)
 ```
 ```
 class ContactDetail(generics.RetrieveUpdateDestroyAPIView, mixins.RetrieveModelMixin, mixins.UpdateModelMixin, mixins.DestroyModelMixin, generics.GenericAPIView):
    queryset = Contact.objects.all()
    serializer_class = ContactSerializer

    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)
    
    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)
    
    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)
```
2) and In urls.py:
```
from django.urls import path
from myapp import views

urlpatterns = [
     path('huhu/', views.ContactList.as_view()),
     path('myDetail/<int:pk>/', views.ContactDetail.as_view()),
]
```
Done.
3) serializers.py file looks like:
```
from rest_framework import serializers
from myapp.models import Contact



class ContactSerializer(serializers.Serializer):
    name = serializers.CharField(max_length=100)
    title = serializers.CharField(max_length=200)
    email = serializers.EmailField(max_length=30)
    
    
    def create(self, validated_data):
        return Contact.objects.create(**validated_data)
    
    
    def update(self, instance, validated_data):
        instance.name = validated_data.get('name', instance.name)
        instance.title = validated_data.get('title', instance.title)
        instance.email = validated_data.get('email', instance.email)
       
        return instance
        
  OR,

from rest_framework import serializers
from myapp.models import Contact

class ContactSerializer(serializers.ModelSerializer):
    class Meta:
        model = Contact
        fields = ['name','title','email']
 ```
4) In root app urls.py
 ```
from django.contrib import admin
from django.urls import path, include 

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('myapp.urls')),
]
```
5) Add in settings as above in root app.

 
