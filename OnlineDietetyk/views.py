from datetime import datetime
from django.shortcuts import render, redirect
from django.db import connection
from django.views import View
from django.http import HttpResponse, HttpResponseRedirect
from django.db.models import Q
from django.contrib import messages
#authentication
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_protect
from django import forms
from django.contrib.auth import (
    authenticate,
    get_user_model,
    login,
    logout
)
from .forms import UserLoginForm, UserRegisterForm
#db models
from OnlineDietetyk.models import Pacjenci, SkladnikiZyw, ProduktyZywn, ProduktSkladnik, KategoriaProduktow, KategorieDan,Danie
from OnlineDietetyk.models import DanieProdukt, TypDiety, Diety, DietaDanie, PoryPosilkow, Wizyty, WynikiBadan, PacjentDieta
#For API requests
import json
import requests

#MIGRATION FROM MS SQL TO MySQL notes
"""To retrieve data from MySQL cursor returns needs to be mapped directly, so any assigning to the variable 'q'
was commented for only MS SQL usage"""

#login process
"""class DashboardView(LoginRequiredMixin, TemplateView):
    template_name = "OnlineDietetyk/index.html"
"""

@csrf_protect
def login_view(request):
    next = request.GET.get('next')
    form = UserLoginForm(request.POST or None)
    if form.is_valid():
        username = form.cleaned_data.get('username')
        password = form.cleaned_data.get('password')
        user = authenticate(username = username, password = password)
        login(request, user)
        if next:
            return redirect(next)
        if user.is_superuser:
            return redirect('index')
        else:
            return redirect('patient_index')
    elif not(form.is_valid()) and request.POST.get('demo'):
        username = 'DemoUser'
        password = 'Demo@123'
        user = authenticate(username=username, password=password)
        login(request, user)
        if next:
            return redirect(next)
        if user.is_superuser:
            return redirect('index')
        else:
            return redirect('patient_index')
    context = {
        'form': form,
    }
    return render(request, "OnlineDietetyk/login.html", context)
"""

def login_view(request):
    form = UserLoginForm(request.POST or None)
    if request.GET.get('logInButton'):
        username = request.GET.get('usernameInput')
        password = request.GET.get('passwordInput')
        user = authenticate(username = username, password = password)
        login(request, user)
        if user.is_superuser:
            return redirect('index')
        else:
            return redirect('patient_index')
    return render(request, "OnlineDietetyk/login.html")
"""
def logout_view(request):
    logout(request)
    return redirect('login')

#sites
#Strona glowna dietetyka/admina
@login_required
def index(request):
    return render(request, 'OnlineDietetyk/index.html')

#Strona glowna pacjentow
@login_required
def patient_index(request):
    return render(request, 'OnlineDietetyk/index_p.html')

@login_required
def patients(request):
    return render(request, 'OnlineDietetyk/patients.html')

@login_required
def products(request):
    return render(request, 'OnlineDietetyk/products.html')

#Pacjenci
@login_required
def add_patient(request):
    if request.method == 'POST' and request.user.is_superuser:
        if request.POST.get('surname') and request.POST.get('name') and request.POST.get('mail') and request.POST.get('DOB'):
            post = Pacjenci()
            post.nazwisko = request.POST.get('surname')
            post.imie = request.POST.get('name')
            post.email = request.POST.get('mail')
            post.telefon = request.POST.get('phone')
            post.data_ur = request.POST.get('DOB')
            post.save()
            return render(request, 'OnlineDietetyk/add_patient.html')
    elif  request.method == 'POST' and not(request.user.is_superuser):
        messages.error(request, "Demo version, changes has not been submitted.")
    else:
        return render(request, 'OnlineDietetyk/add_patient.html')


@login_required
def search_patient(request):

    if request.GET.get('surname') or request.GET.get('name') or request.GET.get('mail') or request.GET.get('DOB') or request.GET.get('phone'):
        result = Pacjenci.objects.filter(nazwisko__icontains = request.GET.get('surname')).filter(imie__icontains = request.GET.get('name'))\
            .filter(email__icontains = request.GET.get('mail')).filter(telefon__icontains = request.GET.get('phone')).filter(data_ur__icontains = request.GET.get('DOB'))
        context = {'result': result}
        return render(request, 'OnlineDietetyk/search_patient.html', context)
    elif request.GET.get('search'):
        result = Pacjenci.objects.order_by('nazwisko')[:10]
        context = {'result': result}
        return render(request, 'OnlineDietetyk/search_patient.html', context)
    else:
        return render(request, 'OnlineDietetyk/search_patient.html')

@login_required
def patient(request, id):
    #uzycie kursora połączenia z bazą danych
    c = connection.cursor()
    c.callproc('p_pacjent_dane', [id, ])
    c.execute("select * from tmpTable;")
    data = c.fetchone()
    c.execute("drop table tmpTable;")
    c.callproc("p_pacjent_wizyty", [id])
    c.execute("select * from tmpTable;")
    visits = c.fetchall()
    c.execute("drop table tmpTable;")
    #użycie składni ORM
    tests = WynikiBadan.objects.filter(id_pacjenta = id)
    diets = PacjentDieta.objects.filter(id_pacjenta = id)
    context = {'data': data, 'visits': visits, 'tests': tests, 'diets': diets}
    if request.method == 'POST' and request.user.is_superuser:
        # editing patient details
        if (request.POST.get('saveData')):
            newSurname = request.POST.get('surname')
            newName = request.POST.get('name')
            if request.POST.get('dob'):
                newDOB = request.POST.get('dob')
            else:
                newDOB = data[2]
            newEmail = request.POST.get('email')
            newPhone = request.POST.get('phone')
            args = [id, newName, newSurname, newPhone, newEmail, newDOB]
            c.callproc('p_edytuj_pacjent', args)
            return redirect('patient', id=id)
        # adding new visit
        if (request.POST.get('addVisit')):
            tmpDay = str(request.POST.get('day'))
            day = datetime.strptime(tmpDay, '%Y-%m-%d')
            tmpHour = str(request.POST.get('hour'))
            hour = datetime.strptime(tmpHour, '%H:%M').time()
            date = datetime.combine(day, hour)
            if request.POST.get('confirmed'):
                conf = 1
            else:
                conf = 0
            if request.POST.get('finished'):
                finished = 1
            else:
                finished = 0
            args = [id,date,conf,finished]
            c.callproc('p_dodaj_wizyte', args)
            return redirect('patient', id=id)
        #updating visit
        if (request.POST.get('updateSelectedVisit')):
            idVisit = request.POST.get('visitToUpdate')
            if request.POST.get('day'):
                tmpDay = str(request.POST.get('day'))
                day = datetime.strptime(tmpDay, '%Y-%m-%d')
            else:
                tmpDay = str(request.POST.get('latestDay'))
                day = datetime.strptime(tmpDay, "%B %d, %Y")
            if request.POST.get('hour'):
                tmpHour = str(request.POST.get('hour'))
            else:
                tmpHour = str(request.POST.get('latestHour'))
            hour = datetime.strptime(tmpHour, '%H:%M').time()
            date = datetime.combine(day, hour)
            if request.POST.get('confirmed'):
                conf = 1
            else:
                conf = 0
            if request.POST.get('finished'):
                finished = 1
            else:
                finished = 0
            args =  [idVisit, date, conf, finished]
            c.callproc('p_edytuj_wizyte', args)
            return redirect('patient', id=id)
        #removing vist
        if (request.POST.get('removeVisit')):
            c.close()
            tmpID = request.POST.get('visitToRemove')
            Wizyty.objects.filter(id=tmpID).delete()
            return redirect('patient', id=id)
        #adding test
        if (request.POST.get('addTest')):
            day = request.POST.get('date')
            t1 = request.POST.get('test1')
            t2 = request.POST.get('test2')
            t3 = request.POST.get('test3')
            args = [id,day,t1,t2,t3]
            c.callproc('p_dodaj_badanie', args)
            return redirect('patient', id=id)
        #removing test
        if (request.POST.get('removeTest')):
            c.close()
            tmpID = request.POST.get('testToRemove')
            WynikiBadan.objects.filter(id=tmpID).delete()
            return redirect('patient', id=id)
        #updating test
        if (request.POST.get('updateSelectedTest')):
            idTest = request.POST.get('testToUpdate')
            if request.POST.get('date'):
                day = request.POST.get('date')
            else:
                day = request.POST.get('latestDate')
            t1 = float(request.POST.get('test1'))
            t2 = float(request.POST.get('test2'))
            t3 = float(request.POST.get('test3'))
            args = [idTest, day, t1, t2, t3]
            c.callproc('p_edytuj_wynik_badania', args)
            return redirect('patient', id=id)
        #adding diet
        if (request.POST.get('addDiet')):
            idDiet = request.POST.get('tmpDiet')
            date1 = request.POST.get('date1')
            date2 = request.POST.get('date2')
            if request.POST.get('status'):
                status = 1
            else:
                status = 0
            args = [id, idDiet, date1, date2, status]
            c.callproc('p_dodaj_diete_pacjent', args)
            return redirect('patient', id=id)
        #removing diet
        if (request.POST.get('removeDiet')):
            c.close()
            tmpID = request.POST.get('DietToRemove')
            PacjentDieta.objects.filter(id=tmpID).delete()
            return redirect('patient', id=id)

        #update diet
        if (request.POST.get('updateSelectedDiet')):
            idDiet = request.POST.get('dietToUpdate')
            if request.POST.get('date1'):
                day1 = request.POST.get('date1')
            else:
                day1 = request.POST.get('latestDate1')
            if request.POST.get('date2'):
                day2 = request.POST.get('date2')
            else:
                day2 = request.POST.get('latestDate2')
            if request.POST.get('status'):
                status = 1
            else:
                status = 0
            args = [idDiet, day1, day2, status]
            c.callproc('call p_edytuj_diete_pacjenta', args)
            return redirect('patient', id=id)
    elif request.method == 'POST' and not(request.user.is_superuser):
        messages.error(request, "Demo version, changes has not been submitted.")
        return redirect('patient', id=id)
    return render(request, 'OnlineDietetyk/patient.html', context)

@login_required
def patient_diets(request):
    type = TypDiety.objects.all()
    cat = {'types': type}
    if request.GET.get('nazwa') or request.GET.get('typ'):
        c = connection.cursor()
        args = [request.GET.get('nazwa'), request.GET.get('typ')]
        c.callproc("p_szukaj_diety", args)
        c.execute("select * from tmpTable;")
        r1 = c.fetchall()
        c.execute("drop table tmpTable;")
        tmpList = []
        for i in r1:
            tmpL2 = []
            tmpL2.append(i[0])
            tmpL2.append(i[1])
            tmpL2.append(i[2])
            args=[i[0]]
            c.callproc("p_dieta_dane", args)
            ds = c.fetchall()
            if (ds):
                for j in ds[0]:
                    tmpL2.append(j)
            tmpList.append(tmpL2)
        context = {'ds': tmpList, 'types': type}
        return render(request, 'OnlineDietetyk/patient_diets.html', context)
    else:
        return render(request, 'OnlineDietetyk/patient_diets.html', cat)

#wizyty
@login_required
def visits(request):
    if request.method == 'POST':
        if (request.POST.get('decline')):
            idVisit = int(request.POST.get('idVisit'))
            Wizyty.objects.filter(id=idVisit).delete()
        return redirect('visits')
    if request.GET.get('search'):
        if (request.GET.get('surname') or request.GET.get('name') or request.GET.get('date')) and not (request.GET.get(
                'confirmed') or request.GET.get('finished')):
            result = Wizyty.objects.filter(id_pacjenta__nazwisko__icontains=request.GET.get('surname')).filter(
                id_pacjenta__nazwisko__icontains=request.GET.get('name')).filter(
                data__date__icontains=request.GET.get('date'))
        elif request.GET.get('confirmed'):
            result = Wizyty.objects.filter(id_pacjenta__nazwisko__icontains=request.GET.get('surname')).filter(
                id_pacjenta__nazwisko__icontains=request.GET.get('name')) \
                .filter(data__date__icontains=request.GET.get('date')).filter(potwierdzona=request.GET.get('confirmed'))
        elif request.GET.get('finished'):
            result = Wizyty.objects.filter(id_pacjenta__nazwisko__icontains=request.GET.get('surname')).filter(
                id_pacjenta__nazwisko__icontains=request.GET.get('name')) \
                .filter(data__date__icontains=request.GET.get('date')).filter(potwierdzona=request.GET.get('finished'))
        context = {'result': result}
        return render(request, 'OnlineDietetyk/visits.html', context)
    else:
        return render(request, 'OnlineDietetyk/visits.html')

@login_required
def new_visit(request):
    return render(request, 'OnlineDietetyk/new_visit.html')

#Produkty
@login_required
def search_product(request):
    categories = KategoriaProduktow.objects.all()
    cat = {'categories' : categories}
    if request.GET.get('nazwa') or request.GET.get('kat') or request.GET.get('kcal') or request.GET.get(
            'skladnik') or request.GET.get('ile'):

        c = connection.cursor()
       # q = c.execute("call p_szukaj_produkt %s,%s,%s,%s", [request.GET.get('nazwa'), request.GET.get('kat'), request.GET.get('kcal'), request.GET.get('skladnik')])
        args = [request.GET.get('nazwa'), request.GET.get('kat')]
        c.callproc("p_szukaj_produkt",args)
        result = c.fetchall()

        context = {'result': result, 'categories' : categories}
        return render(request, 'OnlineDietetyk/search_product.html', context)
    elif request.GET.get('search'):
        c = connection.cursor()
        #q = c.execute("select * from v_produkty_top10_alf")
        c.execute("select * from v_produkty_top10_alf")
        result = c.fetchall()
        context = {'result': result, 'categories': categories}
        return render(request, 'OnlineDietetyk/search_product.html', context)
    else:
        return render(request, 'OnlineDietetyk/search_product.html', cat)

@login_required
def product_details(request, id):
    categories = KategoriaProduktow.objects.all()
    kategorie = {'categories': categories}
    c = connection.cursor()
    c.callproc("p_produkt_dane", [id])
    c.execute("select * from tmpTable;")
    r2 = c.fetchall()
    c.execute("drop table tmpTable;")
    context = {'result': r2}
    if request.method == 'POST' and request.user.is_superuser:
        if (request.POST.get('name') or request.POST.get('cat') or request.POST.get('kcal') or request.POST.get('var1')
                or request.POST.get('var2') or request.POST.get('var3')) and request.POST.get('submit'):
            name = request.POST.get('name')
            cat = request.POST.get('cat')
            kcal = request.POST.get('kcal')
            if not kcal:
                kcal = 0
            var1 = request.POST.get('var1')
            if not var1:
                var1=0
            var2 = request.POST.get('var2')
            if not var2:
                var2=0
            var3 = request.POST.get('var3')
            if not var3:
                var3=0
            args =  [id, name, cat, kcal, var1, var2, var3]
            q3 = c.callproc("p_edytuj_prod", args)
            return redirect('product_details', id=id)
        if (request.POST.get('deleteProduct')):
            c.execute("select * from Danie_produkt where Id_produktu = %s", [id])
            r = c.fetchall()
            if len(r) > 0:
                messages.error(request, "Produkt użyty w daniu!")
            else:
                ProduktSkladnik.objects.filter(id_prod=id).delete()
                ProduktyZywn.objects.filter(id=id).delete()
                return redirect('search_product')
    elif  request.method == 'POST' and not(request.user.is_superuser):
        messages.error(request, "Demo version, changes has not been submitted.")
    return render(request, 'OnlineDietetyk/product.html', context)

@login_required
def new_product(request):
    type = KategoriaProduktow.objects.all()
    context = {'cat': type}
    if request.method == 'POST' and request.user.is_superuser:
        if (request.POST.get('name')):
            name = request.POST.get('name')
            category = request.POST.get('cat')
            kcal = request.POST.get('kcal')
            NewProduct = ProduktyZywn()
            NewProduct.nazwa = name
            type = KategoriaProduktow.objects.get(id=category)
            NewProduct.kategoria_prod = type
            NewProduct.kcal = kcal
            NewProduct.save()
            c = connection.cursor()
            c.execute("select id from Produkty_zywn order by id desc limit 1")
            new_id = c.fetchone()[0]
            return redirect('product_details', id=new_id)
    elif  request.method == 'POST' and not(request.user.is_superuser):
        messages.error(request, "Demo version, changes has not been submitted.")
        return render (request, 'OnlineDietetyk/new_product.html', context)
    else:
        return render (request, 'OnlineDietetyk/new_product.html', context)
#DIETY
@login_required
def diets(request):
    return render(request, 'OnlineDietetyk/diets.html')

@login_required
def diets_all(request):
    type = TypDiety.objects.all()
    cat = {'types': type}
    if request.GET.get('nazwa') or request.GET.get('typ'):
        c = connection.cursor()
        args = [request.GET.get('nazwa'), request.GET.get('typ')]
        c.callproc("p_szukaj_diety", args)
        c.execute("select * from tmpTable")
        r1 = c.fetchall()
        c.execute("drop table tmpTable")
        tmpList = []
        for i in r1:
            tmpL2 = []
            tmpL2.append(i[0])
            tmpL2.append(i[1])
            tmpL2.append(i[2])
            tmpL2.append(i[3])
            tmpL2.append(i[4])
            c.callproc("p_dieta_dane", [i[0]])
            c.execute("select * from tmpTable;")
            ds = c.fetchall()
            c.execute("drop table tmpTable;")
            if (ds):
                for j in ds[0]:
                    tmpL2.append(j)
            tmpList.append(tmpL2)
        context = { 'ds': tmpList, 'types': type}
        return render(request, 'OnlineDietetyk/diets_all.html', context)
    elif request.GET.get('search'):
        c = connection.cursor()
        c.execute("select * from v_diety_top100_alf")
        r1 = c.fetchall()
        tmpList = []
        for i in r1:
            tmpL2 = []
            tmpL2.append(i[0])
            tmpL2.append(i[1])
            tmpL2.append(i[2])
            tmpL2.append(i[3])
            tmpL2.append(i[4])
            c.callproc("p_dieta_dane", [i[0]])
            c.execute("select * from tmpTable;")
            ds = c.fetchall()
            c.execute("drop table tmpTable;")
            if (ds):
                for j in ds[0]:
                    tmpL2.append(j)
            tmpList.append(tmpL2)
        context = {'ds': tmpList, 'types': type}
        return render(request, 'OnlineDietetyk/diets_all.html', context)
    else:
        return render(request, 'OnlineDietetyk/diets_all.html', cat)

@login_required
def diet(request, id):
    c = connection.cursor()
    c.callproc("p_dania_wg_diety", [id])
    dm = c.fetchall()
    c.callproc("p_dieta_dane", [id])
    c.execute("select * from tmpTable;")
    ds = c.fetchall()
    c.execute("drop table tmpTable;")
    context = {'dm': dm, 'ds': ds}
    if request.method == 'POST' and request.user.is_superuser:
        if (request.POST.get('add')):
            c.close()
            mealID = request.POST.getlist('tmpMeal')
            mealDay = request.POST.getlist('tmpDay')
            mealTime = request.POST.getlist('tmpTimeOfMeal')
            mealPortions = request.POST.getlist('tmpPortions')
            tmpList = []
            for i in range(0, len(mealID)):
                d = Diety.objects.get(id=id)
                m = Danie.objects.get(id=mealID[i])
                decimalPortion = float(mealPortions[i])
                if (mealTime[i]):
                    t = PoryPosilkow.objects.get(id=mealTime[i])
                    new = DietaDanie(id_diety=d, id_dania=m, dzien=mealDay[i], pora_dnia=t, porcje=decimalPortion)
                else:
                    new = DietaDanie(id_diety=d, id_dania=m, dzien=mealDay[i], porcje=decimalPortion)
                tmpList.append(new)
            DietaDanie.objects.bulk_create(tmpList)
        if (request.POST.get('remove')):
            c.close()
            c = connection.cursor()
            mealID = request.POST.get('idMeal')
            c.callproc("p_usun_danie_dieta", [id, mealID])
        return redirect('diet', id=id)
    elif request.method == 'POST' and not(request.user.is_superuser):
        messages.error(request, "Demo version, changes has not been submitted.")
        return render(request, 'OnlineDietetyk/diet.html', context)
    else:
        return render(request, 'OnlineDietetyk/diet.html', context)

@login_required
def new_diet(request):
    type = TypDiety.objects.all()
    cat = {'types': type}
    if request.method == 'POST' and request.user.is_superuser:
        if (request.POST.get('name')):
            name = request.POST.get('name')
            kat = request.POST.get('kat')
            NowaDieta = Diety()
            NowaDieta.nazwa = name
            c = connection.cursor()
            if (kat):
                q1 = TypDiety.objects.get(id=kat)
                NowaDieta.typ = q1
            if (request.POST.get('adding_date')):
                NowaDieta.data_dodania = request.POST.get('adding_date')
            else:
                NowaDieta.data_dodania = datetime.today().strftime('%Y-%m-%d')
            NowaDieta.wersja = request.POST.get('version')
            NowaDieta.save()
            c.execute("select id from Diety order by id desc limit 1")
            id_nowej_diety = c.fetchone()[0]
            # return HttpResponseRedirect('/OnlineDietetyk/meal/%s/',id_nowego_dania)
            return redirect('diet', id=id_nowej_diety)
    elif  request.method == 'POST' and not(request.user.is_superuser):
        messages.error(request, "Demo version, changes has not been submitted.")
        return render(request, 'OnlineDietetyk/new_diet.html', cat)
    else:
        return render(request, 'OnlineDietetyk/new_diet.html', cat)

@login_required
def diet_meals(request):
    categories = KategorieDan.objects.all()
    cat = {'categories': categories}
    if request.GET.get('nazwa') or request.GET.get('kat'):
        c = connection.cursor()
        args = [request.GET.get('nazwa'), request.GET.get('kat')]
        c.callproc("p_szukaj_danie", args)
        c.execute("select * from tmpTable;")
        r1 = c.fetchall()
        c.execute("drop table tmpTable;")
        result = list()
        for i in r1:
            c.callproc("p_danie_dane", [i.ID])
            c.execute("select * from tmpTable;")
            r2 = c.fetchall()
            c.execute("drop table tmpTable;")
            result.append(list(i) + list(r2))
        context = {'result': result, 'categories': categories}
        return render(request, 'OnlineDietetyk/diet_meals.html', context)
    else:
        return render(request, 'OnlineDietetyk/diet_meals.html', cat)

#DANIA
@login_required
def meals(request):
    categories = KategorieDan.objects.all()
    cat = {'categories': categories}
    if request.GET.get('nazwa') or request.GET.get('kat'):
        c = connection.cursor()
        args = [request.GET.get('nazwa'), request.GET.get('kat')]
        c.callproc("p_szukaj_danie", args )
        c.execute("select * from tmpTable;")
        r1 = c.fetchall()
        c.execute("drop table tmpTable;")
        result = list()
        for i in r1:
            c.callproc("p_danie_dane", [i[0]])
            c.execute("select * from tmpTable;")
            r2 = c.fetchall()
            c.execute("drop table tmpTable;")
            result.append(list(i)+list(r2))
        context = {'result': result, 'categories': categories}
        return render(request, 'OnlineDietetyk/meals.html', context)
    elif request.GET.get('search'):
        c = connection.cursor()
        c.execute("select * from v_dania_top100_alf")
        r1 = c.fetchall()
        result = list()
        for i in r1:
            c.callproc("p_danie_dane", [i[0]])
            c.execute("select * from tmpTable")
            r2 = c.fetchall()
            c.execute("drop table tmpTable")
            result.append(list(i) + list(r2))
        context = {'result': result, 'categories': categories}
        return render(request, 'OnlineDietetyk/meals.html', context)
    else:
        return render(request, 'OnlineDietetyk/meals.html', cat)

@login_required
def meal(request, id):
    c = connection.cursor()
    c.callproc("p_danie_dane", [id])
    c.execute("select * from tmpTable;")
    meal_stats = c.fetchall()
    c.execute("drop table tmpTable;")
    c.callproc("p_danie_produkty", [id])
    c.execute("select * from tmpTable;")
    meal_prod = c.fetchall()
    c.execute("drop table tmpTable;")
    context1 = {'meal_stats': meal_stats, 'meal_prod': meal_prod}
    if request.method == 'POST' and request.user.is_superuser:
        if (request.POST.get('add') and request.POST.get('tmpProd') ):
            c.close()
            productsID = request.POST.getlist('tmpProd')
            prodAmounts = request.POST.getlist('tmpAmount')
            tmpList = []
            for i in range(0, len(productsID)):
                m = Danie.objects.get(id = id)
                p = ProduktyZywn.objects.get(id = productsID[i])
                new = DanieProdukt(id_dania=m, id_produktu=p, prod_na_100g=prodAmounts[i])
                tmpList.append(new)
            DanieProdukt.objects.bulk_create(tmpList)
                #c = connection.cursor()
                #q = c.execute("call p_dodaj_prod_do_dania %s,%s,%s", [id, i, 22])
        #return render(request, 'OnlineDietetyk/meal.html', context1)
        if (request.POST.get('remove')):
            c.close()
            c = connection.cursor()
            productID = request.POST.get('idProd')
            c.callproc("p_usun_prod_danie", [id, productID])
        return redirect('meal', id=id)
    elif  request.method == 'POST' and not(request.user.is_superuser):
        messages.error(request, "Demo version, changes has not been submitted.")
        return render(request, 'OnlineDietetyk/meal.html', context1)
    else:
        return render(request, 'OnlineDietetyk/meal.html', context1)

@login_required
def new_meal(request):
    c1 = KategorieDan.objects.all()
    kat = {'kat1': c1}
    c = connection.cursor()
    if request.method == 'POST' and request.user.is_superuser:
        if (request.POST.get('name') and request.POST.get('kat')):
            name = request.POST.get('name')
            kat = request.POST.get('kat')
            NoweDanie = Danie()
            NoweDanie.nazwa = name
            q1 = KategorieDan.objects.get(id=kat)
            NoweDanie.kategoria_dania = q1
            NoweDanie.save()
            c.execute("select id from Danie order by id desc limit 1")
            id_nowego_dania = c.fetchone()[0]
            #return HttpResponseRedirect('/OnlineDietetyk/meal/%s/',id_nowego_dania)
            return redirect('meal', id=id_nowego_dania)
    elif  request.method == 'POST' and not(request.user.is_superuser):
        messages.error(request, "Demo version, changes has not been submitted.")
        return render(request, 'OnlineDietetyk/new_meal.html', kat)
    else:
        return render(request, 'OnlineDietetyk/new_meal.html', kat)

@login_required
def meal_products(request):
    categories = KategoriaProduktow.objects.all()
    cat = {'categories' : categories}
    if request.GET.get('nazwa') or request.GET.get('kat') or request.GET.get('kcal') or request.GET.get(
            'skladnik') or request.GET.get('ile'):

        c = connection.cursor()
       # q = c.execute("call p_szukaj_produkt %s,%s,%s,%s", [request.GET.get('nazwa'), request.GET.get('kat'), request.GET.get('kcal'), request.GET.get('skladnik')])
        c.callproc("p_szukaj_produkt", [request.GET.get('nazwa'), request.GET.get('kat')])
        result = c.fetchall()

        context = {'result': result, 'categories' : categories}
        return render(request, 'OnlineDietetyk/meal_products.html', context)
    else:
        return render(request, 'OnlineDietetyk/meal_products.html', cat)

#raporty
@login_required
def reports(request):
    c = connection.cursor()
    c.execute('select * from v_wizyty_nadchodzace')
    visits = c.fetchall()
    c.execute('select * from v_pacjenci_statystyki')
    patients = c.fetchall()
    c.execute('select * from v_dania_top10_kcal')
    top1 = c.fetchall()
    c.execute('select * from v_dania_top10_bialko')
    top2 = c.fetchall()
    c.execute('select * from v_dania_top10_tluszcze')
    top3 = c.fetchall()
    c.execute('select * from v_dania_top10_weglowodany')
    top4 = c.fetchall()
    context = {
        'visits': visits,
        'patients': patients,
        'top1': top1,
        'top2': top2,
        'top3': top3,
        'top4': top4,
    }
    return render (request, 'OnlineDietetyk/reports.html', context)

#OpenFoodDatbase API
def openfoodapi(request):
    categories = KategoriaProduktow.objects.all()
    if request.GET.get('keyword'):
        keyword = request.GET.get('keyword')
        param = {"search_terms": keyword, "json": "true"}
        respond = requests.get('https://world.openfoodfacts.org/cgi/search.pl', params = param).json()
        context = {
        'results': respond["products"],
        'categories': categories
        }
        return render(request, 'OnlineDietetyk/openfoodapi.html', context)
    if request.method == 'POST' and request.user.is_superuser:
        if (request.POST.get('addFromAPI') and request.POST.get('kat')):
            #return HttpResponseRedirect('/OnlineDietetyk/meal/%s/',id_nowego_dania)
            return redirect('meal', id=1)
    elif  request.method == 'POST' and not(request.user.is_superuser):
        messages.error(request, "Demo version, changes has not been submitted.")
        return render(request, 'OnlineDietetyk/openfoodapi.html')
    else:
        return render(request, 'OnlineDietetyk/openfoodapi.html')

