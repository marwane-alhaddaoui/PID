from django.shortcuts import render,redirect,get_object_or_404
from django.http import Http404
from catalogue.models import Artist
from catalogue.forms.ArtistForm import ArtistForm
from django.contrib import messages
from django.conf import settings

# Create your views here.
def index(request):
    artists = Artist.objects.all()
    title = 'Liste des artistes'
    
    return render(request, 'artist/index.html', {
        'artists':artists,
        'title':title
    })

def show(request, artist_id):
    try:
        artist = Artist.objects.get(id=artist_id)
    except Artist.DoesNotExist:
        raise Http404('Artist inexistant');
        
    title = 'Fiche d\'un artiste'
    
    return render(request, 'artist/show.html', {
        'artist':artist,
        'title':title 
    })

def edit(request, artist_id):
    # fetch the object related to passed id
    artist = Artist.objects.get(id=artist_id)

    
    # pass the object as instance in form
    form = ArtistForm(request.POST or None, instance = artist)
    
    if request.method == 'POST':	#TODO http_override doesn't work
        # save the data from the form and
        # redirect to detail_view
        if form.is_valid():
            form.save()
            messages.success(request, "Artiste modifié avec succès.")
            return render(request, "artist/show.html", {
                'artist' : artist,
            })
        else:
            messages.error(request, "Échec de la modification de l'artiste !")



    return render(request, 'artist/edit.html', {
        'form' : form,
        'artist' : artist,
    })
def create(request):
    if not request.user.is_authenticated or not request.user.has_perm('add_artist'):
                        return redirect(f"{settings.LOGIN_URL}?next={request.path}")
    form = ArtistForm(request.POST or None)
    
    if request.method == 'POST':
        if form.is_valid():
            form.save()
            messages.add_message(request, messages.SUCCESS, "Nouvel artiste créé avec succès.")

            return redirect('catalogue:artist-index')
        else:
            messages.add_message(request, messages.ERROR, "Échec de l'ajout d'un nouvel artiste !")

    return render(request, 'artist/create.html', {
        'form' : form,
    })


def delete(request, artist_id):
    artist = get_object_or_404(Artist, id = artist_id)

    if request.method =="POST":
        artist.delete()
        messages.success(request, "Artiste supprimé avec succès.")
        return redirect('catalogue:artist-index')
    else:
        messages.error(request, "Échec de la suppression de l'artiste !")

    return render(request, 'artist/show.html', {
        'artist' : artist,
    })
