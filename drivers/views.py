import json

from django.shortcuts import redirect, render, get_object_or_404
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse, HttpResponse
from .forms import RegistrationForm, DriverForm
from AutoparkProject.utils import calculate_age
from AutoparkProject.settings import LOGIN_REDIRECT_URL

from employees.models import Car
from drivers.models import CarDriver, Driver



def index(request):
    title = "Главная страница"
    context = {"title": title}
    return render(request, "drivers/index.html", context=context)


def register(request):
    if request.method == "POST":
        reg_form = RegistrationForm(request.POST)
        driver_form = DriverForm(request.POST)

        if reg_form.is_valid() and driver_form.is_valid():
            user = reg_form.save()
            driver = driver_form.save(commit=False)
            driver.user = user
            driver.age = calculate_age(driver.birthday)
            driver.save()
            # return redirect("driver_profile")
            return register_done(request, new_user=driver)

    # для метода GET
    reg_form = RegistrationForm()
    driver_form = DriverForm()
    context = {"reg_form": reg_form, "driver_form": driver_form}

    return render(request, "drivers/register.html", context=context)


def register_done(request, new_user):
    context = {"driver": new_user, "title": "Успешная регистрация"}
    return render(request, "drivers/register_done.html", context=context)


def log_in(request):
    form = AuthenticationForm(request, data=request.POST or None)
    if request.method == "POST":
        if form.is_valid():
            username = form.cleaned_data["username"]
            password = form.cleaned_data["password"]

            user = authenticate(username=username, password=password)

            if user is not None:
                login(request, user)
                url = request.GET.get("next", LOGIN_REDIRECT_URL)
                return redirect(url)

    return render(request, "drivers/login.html", {"form": form, "title": "Вход"})


def log_out(request):
    logout(request)
    url = LOGIN_REDIRECT_URL
    return redirect(url)

@login_required
def select_car(request):
    """
    Если водитель меняет машину, то:
    текущая машина:
    - статус=True
    Новая машина:
    - статус=False
    Меняем машину в таблице связи
    !!!!
    переопределить __str__  у cardriver
    drivercardriver.objects.get_or_create(driver=driver)
    if true:
        ? driver, created = drivercardriver.objects.get_or_create(driver=driver)
        cardriver.car = new_car
    """
    if request.method == "GET":
        title = "Выберите машину"
        cars = Car.objects.filter(status=True)
        car_count = Car.objects.filter(status=True).count()
        context = {"title": title, "cars": cars, "count": car_count}
        return render(request, "drivers/select_car.html", context=context)

    if request.method == "POST":
        car_id = request.POST.get('car_id')
        new_car = Car.objects.get(pk=car_id)

        driver = Driver.objects.get(user=request.user)
        if driver.cardriver_set.first() is not None:
            if driver.cardriver_set.first().car is not None:
                pass



    # if pk is not None:
    #     car = Car.objects.get(pk=pk)
    #     car.status = False
    #     car.save()
    #
    #     driver = Driver.objects.get(user=request.user)
    #     CarDriver.objects.create(car=car, driver=driver)
    #     return redirect("drivers:index")



@csrf_exempt
def test_fetch(request):
    if request.method == "POST":
        json_data = json.loads(request.body)
        car_id = json_data.get('id')

        return JsonResponse({'car_id': car_id})

@login_required
def profile(request, pk):
    driver = get_object_or_404(Driver, pk=pk)
    car_driver = CarDriver.objects.filter(driver=driver).first()

    if car_driver is not None:
        car = car_driver.car
    else:
        car = None


    context = {'driver': driver, 'car': car}
    return render(request, 'drivers/profile.html', context=context)


def refuse_car(request):
    if request.method == "GET":
        return render(request, 'drivers/refuse_car.html')

    if request.method == "POST":
        if 'refuse' in request.POST:
            """
            получаем водителя
            получаем машину водителя
            статус машины -> car.status=True
            cardriver(driver=driver).car=null
            """
            driver = Driver.objects.get(user=request.user)
            driver.cardriver_set.first().car.status = False
            driver.cardriver_set.first().delete()
            return redirect("drivers:profile")
        else:
            return redirect("drivers:profile")