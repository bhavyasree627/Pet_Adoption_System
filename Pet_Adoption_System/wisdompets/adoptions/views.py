from django.shortcuts import render,redirect
from django.http import Http404
from django.utils import timezone
from .models import Pet

def home(request):
    return render(request, 'home.html')

def pets(request):
    pets = Pet.objects.all()
    return render(request, 'pets.html', {
        'pets': pets,
    })

def add_pet(request):
    if request.method == "POST":
        data=request.POST
        name=data.get('name')
        submitter=data.get('submitter')
        species=data.get('species')
        breed=data.get('breed')
        description=data.get('description')
        sex=data.get('sex')
        submission_date=timezone.now()
        age=int(data.get('age'))
        pet_image=request.FILES.get("pet_image")
        Pet.objects.create(
            name=name, 
            submitter=submitter,  
            species=species, 
            breed=breed,
            description=description,
            submission_date=submission_date,
            pet_image=pet_image,
            sex=sex,
            age=age,
            )

    return render(request, 'add_pet.html')

def pet_detail(request, pet_id):
    try:
        pet = Pet.objects.get(id=pet_id)
    except Pet.DoesNotExist:
        raise Http404('pet not found')
    return render(request, 'pet_detail.html', {
        'pet': pet,
    })

def delete_pet(request,id):
    queryset = Pet.objects.get(id=id)
    queryset.delete()
    return redirect('/all_pets/')

def update_pet(request,id):
    queryset = Pet.objects.get(id=id)
    if request.method=="POST":
        data=request.POST
        name=data.get('name')
        submitter=data.get('submitter')
        species=data.get('species')
        breed=data.get('breed')
        description=data.get('description')
        sex=data.get('sex')
        age=int(data.get('age'))
        pet_image=request.FILES.get("pet_image")

        queryset.name=name
        queryset.submitter=submitter
        queryset.species=species
        queryset.breed=breed
        queryset.description=description
        queryset.sex=sex
        queryset.age=age
        if pet_image:
            queryset.pet_image=pet_image
        queryset.save()
        return redirect('/all_pets/')
        
    context={'pet':queryset}
    return render(request, 'update_pet.html',context)