from django.shortcuts import render
from django.http import HttpResponse
from .models import Item, Inventory, Character, Landmark, Game
from authentication.models import User
from django.http import JsonResponse
from random import randrange, choice, randint


beginning_inventory = {
    "food": "A day's food for your team.",
    "cd": "A cd",
    "Bible": "A Gideon Bible",

}

place_list = {
    "camp": "a camp",
    "hotel": "a hotel",
    "pack": "a pack"}

landmarks = {"Oregon Border":
                 {"story": "You make camp on ",
                  "key": "Bible",
                  "gain": "cd",
                  "loss": "food",
                  "story_loss": "You lose one day's food.",
                  "story_gain": "After finding the Bible in your packs, the group allows you to rest on their land and offers you a gift of food to help you on your way."
                  },
             "Eugene":
                 {"story": "You have reached Eugene.",
                  "key": "Bible",
                  "gain": "cd",
                  "loss": "food",
                  "story_loss": "You lose one day's food.",
                  "story_gain": "You receive a CD.",
                  },
             "Salem":
                 {"story": "You have reached Salem.",
                  "key": "Bible",
                  "gain": "cd",
                  "loss": "food",
                  "story_loss": "You lose a day's food.",
                  "story_gain": "You receive a book.",
                  },
             }


"""This helper function creates the initial inventory in packing view. """


def create_initial_inventory():
    initial_inv = Inventory.objects.create(name="initial_inv")
    items = []
    for x in beginning_inventory.keys():
        items.append(x)
    for x in range(len(beginning_inventory)):
        if items[x] != "food":
            name = Item.objects.create(name=items[x], description=beginning_inventory[items[x]], inventory=initial_inv)
        if items[x] == "food":
            y = 0
            while y < 5:
                name = Item.objects.create(name=items[x], description=beginning_inventory[items[x]],
                                           inventory=initial_inv)
                y += 1
    return initial_inv

"""This helper function creates all the place inventories and found items in play view."""

def create_place_inventories(place_inventory):
    places = place_list.keys()
    for place in places:
        find = Item.objects.create(name=place, description=place_list[place],
                                       inventory=place_inventory)


def landmark_outcomes(name):
    milestone = landmarks[name]
    ldmk = Landmark.objects.create(name=name)
    find = Item.objects.create(name=milestone["gain"], description=milestone["gain"], landmark=ldmk, inventory=place_inventory)
    player_inventory = player_inv.items.all()
    has_key = None
    for item in player_inventory:
        if item.name == milestone["key"]:
            has_key = True
            break
        else:
            has_key = False
    if has_key == True:
        find.landmark = None
        find.inventory = player_inv
        find.save()
    if has_key == False:
        for item in player_inventory:
            if item.name == milestone["loss"]:
                item.inventory = place_inventory
                item.save()


def gameplay(request):
    return render(request, 'game/gameplay.html', {})


def gameplay_entry(request):
    if request.method == 'POST':
        print(request.user.username)
        user = User.objects.get(username=request.user.username)
        limit = 0
        if request.POST.get("choice", None) == str(1):
            limit = 15
            print("1")
        if request.POST.get("choice", None) == str(2):
            limit = 10
            print("2")
        if request.POST.get("choice", None) == str(3):
            limit = 5
            print("3")
        print(limit)
        inv = Inventory(name="player_inv", limit=limit)
        inv.save()
        user.game = inv
        user.save()
        return JsonResponse({'message': 'success'})
    return JsonResponse({'message': 'fail'})

#This needs a try/except to ensure it's one of these three.

def names(request):
    # create_characters() # add variables for name1 through name4
     return render(request, 'game/names.html', {})


def names_entry(request):

    if request.method == 'POST':
        user = User.objects.get(username=request.user.username)
        inv = user.game
        Character.objects.create(name="You", inventory=inv)
        Character.objects.create(name=request.POST.get('choice2', None), inventory=inv)
        Character.objects.create(name=request.POST.get('choice3', None), inventory=inv)
        Character.objects.create(name=request.POST.get('choice4', None), inventory=inv)
        Character.objects.create(name=request.POST.get('choice5', None), inventory=inv)
        user.save()
        inv.save()
        print(inv.characters.all)
        return JsonResponse({'message': 'success'})
    return JsonResponse({'message': 'fail'})

#This one doesn't print to the console properly.  Not sure why.

def show_game(request):
    user = User.objects.get(username=request.user.username)
    return render(request, 'pages/show_game.html', {'user': user})

#What is this function for?  Testing?



"""
The first version of packing and packing_entry created an initial inventory and changed inv to player inv.
"""

def packing(request):

    """
    This second version of the function needs a dictionary to print out the names of the items.
    """
    # i_inv = create_initial_inventory()
    # return render(request, 'game/packing.html', {"initial_inventory": i_inv})

    return render(request, 'game/packing.html', {})


def packing_entry(request):

    """
    This second version of the view function will need a dictionary to fill out descriptions.
    This or the next two functions need to set limit on player_inventory items.
    """
    if request.method == 'POST':

        user = User.objects.get(username=request.user.username)
        inv = user.game
        Item.objects.create(name=request.POST.get('choice', None), inventory=inv)
        print(inv)

        # user = User.objects.get(username=request.user.username)
        # player_inventory = user.game
        # to_pack = Item.objects.get(name=request.POST.get('choice', None))
        # to_pack.inventory = player_inventory
        # print(player_inventory)


        return JsonResponse({'message': 'success'})
    return JsonResponse({'message': 'fail'})


def depart(request):
    player_inv = Inventory.objects.create()
    player_inventory = player_inv.items.all()
    return render(request, 'game/depart.html', {"player_inventory": player_inventory})

    #The form on this page needs to allow the user to:
        #  remove items from the pack and return them to initial_inv.

def depart_entry(request):
    if request.method == 'POST':
        unpack = request.POST.get("unpack", None)
    return JsonResponse({"unpack": unpack})


def play(request):

    """This one is the heart of the game.
    Template:
        display mile_counter and day_counter (Do they need to be in the database to show in template?
        User needs to be able to:
            Walk
            Random events
            Forage / Scavenge (places)
            Landmarks
        This needs to allow the user to die / lose the game.
        This needs to allow the user to win.
    """

    place_inventory = Inventory.objects.create(name="place_inv")
    create_place_inventories(place_inventory)
    return render(request, 'game/play.html', {})



def play_entry(request):
    user = User.objects.get(username=request.user.username)
    player_inventory = user.game
    if request.method == 'POST':
        if request.POST.get("move", None) == str(1):
            player_inventory.mile_counter += randint(12, 22)
            player_inventory.day_counter += 1
            player_inventory.save()
            print("{} days on the trail.  {} miles covered.".format(player_inventory.day_counter, player_inventory.mile_counter))
            for i in player_inventory.characters.all():
                    i.description -= 5
                    print(i.description)
                    i.save()
            for i in player_inventory.items.all():
                if i.name == "food":
                    i.inventory = None
                    i.save()
                    print(player_inventory)
                    break
#What's up with the indentation on this if/else statement???
            else:
                print("You have run out of food.")
                for i in player_inventory.characters.all():
                    i.description -= 20
                    i.save()
                    print(i.description)

        if request.POST.get("move", None) == str(2):
            pass

        if request.POST.get("move", None) == str(3):
            pass

        return JsonResponse({'message': 'success'})
    return JsonResponse({'message': 'fail'})


def win(request):
    return render(request, 'game/win.html', {})