from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from .models import User, Barbershop, Customer, Service, Appointment, Review ,ShopImage
from BarberEase import models
from django.db.models import Count, Avg
from datetime import date
from django.db.models import Count
from django.db.models import Q
from datetime import datetime, timedelta


# -------------------- Home --------------------
def Home(request):
    reviews = Review.objects.select_related('customer').order_by('-created_at')[:3]
    return render(request, 'index.html', {'reviews': reviews})


# -------------------- Authentication --------------------
def user_login(request):
    if request.method == "POST":
        username_or_email = request.POST.get("username")  # avoid naming conflict
        password = request.POST.get("password")

        # Authenticate
        user = authenticate(request, username=username_or_email, password=password)

        if user is not None:
            login(request, user)
            # Redirect by role
            if user.usertype == "Admin":
                return redirect("Admin_home")
            elif user.usertype == "Owner":
                return redirect("shopowner_home")
            else:
                return redirect("customer_home")
        else:
            messages.error(request, "Invalid credentials. Please try again.")
            return redirect("login")

    return render(request, 'login.html')



def user_logout(request):
    logout(request)
    return redirect("home")


# def signup_customer(request):
#     if request.method == "POST":
#         name = request.POST.get("name")
#         email = request.POST.get("email")
#         password1 = request.POST.get("password1")
#         password2 = request.POST.get("password2")
#         gender = request.POST.get("gender", "")

#         if not all([name, email, password1, password2]):
#             messages.error(request, "Please complete all required fields.")
#             return redirect("signup_customer")

#         if password1 != password2:
#             messages.error(request, "Passwords do not match.")
#             return redirect("signup_customer")

#         username = email  # use email as username

#         # Create user (password hashed internally)
#         user = User.objects.create_user(username=username , email=email, password=password1, usertype="Customer")

#         # Create customer profile and optionally store raw password (only for demo)
#         Customer.objects.create(usrname=user, name=name, gender=gender, email=email, password_raw=password1)

#         messages.success(request, "Customer account created. Please log in.")
#         return redirect("login")

#     return render(request, 'signup_customer.html')



def signup_customer(request):
    if request.method == "POST":
        name = request.POST.get("name")
        username = request.POST.get("username")   # new username field from form
        email = request.POST.get("email")
        password1 = request.POST.get("password1")
        password2 = request.POST.get("password2")
        gender = request.POST.get("gender", "")

        if not all([name, username, email, password1, password2]):
            messages.error(request, "Please complete all required fields.")
            return redirect("signup_customer")

        if password1 != password2:
            messages.error(request, "Passwords do not match.")
            return redirect("signup_customer")

        # Create user with both username and email
        user = User.objects.create_user(
            username=username,
            email=email,
            password=password1,
            usertype="Customer"
        )

        # Create customer profile
        Customer.objects.create(
            usrname=user,
            name=name,
            gender=gender,
            email=email,
            password_raw=password1
        )

        messages.success(request, "Customer account created. Please log in.")
        return redirect("login")

    return render(request, 'signup_customer.html')


# def signup_owner(request):
#     if request.method == "POST":
#         shop_name = request.POST.get("shop_name")
#         email = request.POST.get("email")
#         password1 = request.POST.get("password1")
#         password2 = request.POST.get("password2")
#         location = request.POST.get("location", "")
#         phone = request.POST.get("phone", "")
#         owner_name = request.POST.get("owner_name", "")

#         if not all([shop_name, email, password1, password2]):
#             messages.error(request, "Please fill required fields.")
#             return redirect("signup_owner")

#         if password1 != password2:
#             messages.error(request, "Passwords do not match.")
#             return redirect("signup_owner")

#         username = email
#         user = User.objects.create_user(username=username, email=email, password=password1, usertype="Owner")

#         # Create a Barbershop (owner will be pending approval)
#         Barbershop.objects.create(
#             usrname=user,
#             password_raw=password1,
#             name=owner_name,    
#             phone=phone,
#             email=email,
#             shop_name=shop_name,
#             shop_address=location,
#             is_approved=False,  # admin must approve
#         )

#         messages.success(request, "Barbershop created successfully. Please wait for admin approval.")
#         return redirect("login")

#     return render(request, 'signup_owner.html')

# def signup_owner(request):
#     if request.method == "POST":
#         username = request.POST.get("username")  # <-- NEW username
#         shop_name = request.POST.get("shop_name")
#         email = request.POST.get("email")
#         password1 = request.POST.get("password1")
#         password2 = request.POST.get("password2")
#         location = request.POST.get("location", "")
#         phone = request.POST.get("phone", "")

#         if not all([username, shop_name, email, password1, password2]):
#             messages.error(request, "Please fill required fields.")
#             return redirect("signup_owner")

#         if password1 != password2:
#             messages.error(request, "Passwords do not match.")
#             return redirect("signup_owner")

#         # Create user with username + email
#         user = User.objects.create_user(
#             username=username,
#             email=email,
#             password=password1,
#             usertype="Owner"
#         )

#         # Create a Barbershop (owner will be pending approval)
#         Barbershop.objects.create(
#             usrname=user,
#             password_raw=password1,
#             phone=phone,
#             email=email,
#             shop_name=shop_name,
#             shop_address=location,
#             is_approved=False,  # admin must approve
#         )

#         messages.success(request, "Barbershop created successfully. Please wait for admin approval.")
#         return redirect("login")

#     return render(request, 'signup_owner.html')

def signup_owner(request):
    if request.method == "POST":
        username = request.POST.get("username")
        shop_name = request.POST.get("shop_name")
        email = request.POST.get("email")
        password1 = request.POST.get("password1")
        password2 = request.POST.get("password2")
        location = request.POST.get("shop_address", "")  # use "shop_address" to match form
        phone = request.POST.get("phone", "")
        opening_time = request.POST.get("opening_time", "")
        closing_time = request.POST.get("closing_time", "")
        license_image = request.FILES.get("license_image")
        shop_images = request.FILES.getlist("shop_images")

        # Required field checks
        if not all([username, shop_name, email, password1, password2, license_image]):
            messages.error(request, "Please fill all required fields, including license image.")
            return redirect("signup_owner")

        if password1 != password2:
            messages.error(request, "Passwords do not match.")
            return redirect("signup_owner")

        if not shop_images:
            messages.error(request, "Please upload at least one shop image.")
            return redirect("signup_owner")

        # Create user
        user = User.objects.create_user(
            username=username,
            email=email,
            password=password1,
        )
        user.usertype = "Owner"
        user.save()

        # Create barbershop
        barbershop = Barbershop.objects.create(
            usrname=user,
            password_raw=password1,
            phone=phone,
            email=email,
            shop_name=shop_name,
            shop_address=location,
            opening_time=opening_time or None,
            closing_time=closing_time or None,
            license_image=license_image,
            is_approved=False,
        )

        # Save shop images
        for img in shop_images:
            ShopImage.objects.create(shop=barbershop, image=img)

        messages.success(request, "Barbershop created successfully. Please wait for admin approval.")
        return redirect("login")

    return render(request, 'signup_owner.html')

# -------------------- Admin views --------------------
# @login_required
# def Admin_home(request):
#     if request.user.usertype != "Admin":
#         messages.error(request, "Unauthorized access.")
#         return redirect("Home")

#     shops = Barbershop.objects.all().order_by('-created_at')
#     customers = Customer.objects.all()
#     appointments = Appointment.objects.all().order_by('-created_at')

#     context = {
#         "shops_count": shops.count(),
#         "customers_count": customers.count(),
#         "appointments_count": appointments.count(),
#         "shops": shops,
#         "customers": customers,
#         "appointments": appointments[:20],
#     }
#     return render(request, 'admin_home.html', context)

@login_required
def Admin_home(request):
    if request.user.usertype != "Admin":
        messages.error(request, "Unauthorized access.")
        return redirect("home")
    
    shops_count = Barbershop.objects.count()
    customers_count = Customer.objects.count()
    appointments_count = Appointment.objects.count()
    review_count = Review.objects.count()

    # Separate approved and pending shops
    pending_shops = Barbershop.objects.filter(is_approved=False).order_by('-created_at')
    approved_shops = Barbershop.objects.filter(is_approved=True).order_by('-created_at')

    customers = Customer.objects.all()
    appointments = Appointment.objects.all().order_by('-created_at')
    pending_shops_count = Barbershop.objects.filter(is_approved=False).count()


    context = {
        "shops_count": shops_count,
        "review_count": review_count,
        "customers_count": customers_count,
        "appointments_count": appointments_count,
        "pending_shops": pending_shops,
        "pending_shops_count": pending_shops_count,
        "approved_shops": approved_shops,
        "customers_count": customers.count(),
        "appointments_count": appointments.count(),
        "appointments": appointments[:20],
    }
    return render(request, 'admin_home.html', context)



def admin_shop_detail(request, shop_id):
    shop = get_object_or_404(Barbershop, id=shop_id)
    return render(request, "admin_shop_detail.html", {"shop": shop})


@login_required
def approve_shop(request, shop_id):
    if request.user.usertype != "Admin":
        messages.error(request, "Unauthorized access.")
        return redirect("home")

    shop = get_object_or_404(Barbershop, id=shop_id)
    shop.is_approved = True
    shop.save()
    messages.success(request, f"{shop.shop_name} approved.")
    return redirect("Admin_home")


@login_required
def reject_shop(request, shop_id):
    if request.user.usertype != "Admin":
        messages.error(request, "Unauthorized access.")
        return redirect("home")

    shop = get_object_or_404(Barbershop, id=shop_id)
    shop.delete()
    messages.success(request, "Shop rejected and removed.")
    return redirect("Admin_home")


# -------------------- Shop owner views --------------------
@login_required
def ShopOwner_home(request):
    if request.user.usertype != "Owner":
        messages.error(request, "Unauthorized access.")
        return redirect("home")

    # get the shop owned by this user
    shop = get_object_or_404(Barbershop, usrname=request.user)
    services = Service.objects.filter(shop=shop)
    appointments = Appointment.objects.filter(shop=shop).order_by('-created_at')

    context = {
        "shop": shop,
        "services": services,
        "appointments": appointments,
    }
    return render(request, 'shopowner_home.html', context)


@login_required
def add_service(request):
    if request.user.usertype != "Owner":
        messages.error(request, "Unauthorized access.")
        return redirect("home")

    shop = get_object_or_404(Barbershop, usrname=request.user)

    if request.method == "POST":
        name = request.POST.get("service_name")
        price = request.POST.get("price")
        if not name or not price:
            messages.error(request, "Please provide service name and price.")
            return redirect("add_service")
        Service.objects.create(shop=shop, service_name=name, price=price)
        messages.success(request, "Service added successfully.")
        return redirect("shopowner_home")

    return render(request, 'add_service.html', {"shop": shop})


@login_required
def approve_appointment(request, appointment_id):
    appointment = get_object_or_404(Appointment, id=appointment_id)
    # Ensure only the owner of the shop can approve
    if request.user.usertype == "Owner" and appointment.shop.usrname == request.user:
        appointment.status = 1
        appointment.save()
        messages.success(request, "Appointment approved.")
    else:
        messages.error(request, "Unauthorized.")
    return redirect("shopowner_home")


@login_required
def reject_appointment(request, appointment_id):
    appointment = get_object_or_404(Appointment, id=appointment_id)
    if request.user.usertype == "Owner" and appointment.shop.usrname == request.user:
        appointment.status = 2
        appointment.save()
        messages.warning(request, "Appointment rejected.")
    else:
        messages.error(request, "Unauthorized.")
    return redirect("shopowner_home")


@login_required
def manage_shop_images(request):
    shop = get_object_or_404(Barbershop, usrname=request.user)

    if request.method == "POST":
        if "update_shop" in request.POST:
            # Update shop details
            shop.shop_name = request.POST.get("shop_name")
            shop.email = request.POST.get("email")
            shop.phone = request.POST.get("phone")
            shop.shop_address = request.POST.get("shop_address")
            shop.opening_time = request.POST.get("opening_time")
            shop.closing_time = request.POST.get("closing_time")
            shop.save()

        if "upload_images" in request.POST and request.FILES.getlist("images"):
            for img in request.FILES.getlist("images"):
                ShopImage.objects.create(shop=shop, image=img)

        if "delete_images" in request.POST and request.POST.getlist("delete_ids"):
            ShopImage.objects.filter(id__in=request.POST.getlist("delete_ids"), shop=shop).delete()

        return redirect("manage_shop_images")

    return render(request, "manage_shop_images.html", {"shop": shop})


# -------------------- Customer views --------------------
@login_required
def Customer_home(request):
    if request.user.usertype != "Customer":
        messages.error(request, "Unauthorized access.")
        return redirect("home")

    shops = Barbershop.objects.filter(is_approved=True).order_by('-created_at')
    # find the customer's profile
    try:
        customer = Customer.objects.get(usrname=request.user)
    except Customer.DoesNotExist:
        customer = None

    my_appointments = Appointment.objects.filter(customer__usrname=request.user).order_by('-created_at')
    next_appointment = my_appointments.filter(date__gte=date.today()).first()

    context = {
        "shops": shops,
        "customer": customer,
        "appointments": my_appointments,
        "next_appointment": next_appointment,

    }
    return render(request, 'customer_home.html', context)

@login_required
def customer_profile(request):
    customer = Customer.objects.get(usrname=request.user)

    if request.method == "POST":
        customer.name = request.POST.get("name", customer.name)
        customer.gender = request.POST.get("gender", customer.gender)
        customer.phone = request.POST.get("phone", customer.phone)
        customer.email = request.POST.get("email", customer.email)

        if "profile_pic" in request.FILES:
            customer.profile_pic = request.FILES["profile_pic"]

        customer.save()
        messages.success(request, "Profile updated successfully!")

    return render(request, "customer_profile.html", {"customer": customer})


# @login_required
# def book_appointment(request, shop_id, service_id):
#     if request.user.usertype != "Customer":
#         messages.error(request, "Unauthorized access.")
#         return redirect("home")

#     shop = get_object_or_404(Barbershop, id=shop_id, is_approved=True)
#     service = get_object_or_404(Service, id=service_id, shop=shop)
#     customer = get_object_or_404(Customer, usrname=request.user)

#     if request.method == "POST":
#         date = request.POST.get("date")
#         time = request.POST.get("time")
#         if not date or not time:
#             messages.error(request, "Please select date and time.")
#             return redirect("book_appointment", shop_id=shop_id, service_id=service_id)

#         Appointment.objects.create(customer=customer, shop=shop, service=service, date=date, time=time)
#         messages.success(request, "Appointment booked. Waiting for approval.")
#         return redirect("customer_home")

#     context = {"shop": shop, "service": service}
#     return render(request, 'book_appointment.html', context)



# @login_required
# def book_appointment(request, shop_id, service_id):
#     if request.user.usertype != "Customer":
#         messages.error(request, "Unauthorized access.")
#         return redirect("home")

#     shop = get_object_or_404(Barbershop, id=shop_id, is_approved=True)
#     service = get_object_or_404(Service, id=service_id, shop=shop)
#     customer = get_object_or_404(Customer, usrname=request.user)

#     date_selected = request.GET.get("date") or request.POST.get("date")
#     available_slots = []

#     if date_selected:
#         # Parse date
#         try:
#             appointment_date = datetime.strptime(date_selected, "%Y-%m-%d").date()
#         except ValueError:
#             appointment_date = None

#         # Get all existing bookings for that day, this shop, this service
#         booked_times = Appointment.objects.filter(
#             shop=shop,
#             service=service,
#             date=appointment_date,
#             status__in=[0, 1]  # Pending or Approved
#         ).values_list("time", flat=True)

#         # Generate possible slots
#         opening = shop.opening_time or datetime.strptime("09:00", "%H:%M").time()
#         closing = shop.closing_time or datetime.strptime("18:00", "%H:%M").time()
#         slot_length = service.duration  # in minutes

#         slots = []
#         t = datetime.combine(appointment_date, opening)
#         closing_dt = datetime.combine(appointment_date, closing)

#         while t + timedelta(minutes=slot_length) <= closing_dt:
#             slot_time = t.time()
#             if slot_time not in booked_times:
#                 slots.append(slot_time.strftime("%H:%M"))
#             t += timedelta(minutes=slot_length)
#         available_slots = slots

#     if request.method == "POST" and date_selected:
#         time = request.POST.get("slot")
#         if not date_selected or not time:
#             messages.error(request, "Please select date and time slot.")
#             return redirect(request.path_info + f"?date={date_selected}")

#         # Double-check slot is still available
#         exists = Appointment.objects.filter(
#             shop=shop,
#             service=service,
#             date=date_selected,
#             time=time,
#             status__in=[0, 1]
#         ).exists()
#         if exists:
#             messages.error(request, "Sorry, slot just booked. Please choose another.")
#             return redirect(request.path_info + f"?date={date_selected}")

#         Appointment.objects.create(
#             customer=customer, shop=shop, service=service, date=date_selected, time=time
#         )
#         messages.success(request, "Appointment booked. Waiting for approval.")
#         return redirect("customer_home")

#     context = {
#         "shop": shop, "service": service,
#         "date_selected": date_selected,
#         "available_slots": available_slots,
#     }
#     return render(request, 'book_appointment.html', context)

@login_required
def book_appointment(request, shop_id, service_id):
    if request.user.usertype != "Customer":
        messages.error(request, "Unauthorized access.")
        return redirect("home")

    shop = get_object_or_404(Barbershop, id=shop_id, is_approved=True)
    service = get_object_or_404(Service, id=service_id, shop=shop)
    customer = get_object_or_404(Customer, usrname=request.user)

    date_selected = request.GET.get("date") or request.POST.get("date")
    available_slots = []

    if date_selected:
        try:
            appointment_date = datetime.strptime(date_selected, "%Y-%m-%d").date()
        except ValueError:
            appointment_date = None

        # Get all existing bookings for that day, this shop, this service (ALL statuses)
        booked_times = Appointment.objects.filter(
            shop=shop,
            service=service,
            date=appointment_date
        ).values_list("time", flat=True)

        opening = shop.opening_time or datetime.strptime("09:00", "%H:%M").time()
        closing = shop.closing_time or datetime.strptime("18:00", "%H:%M").time()
        slot_length = service.duration  # in minutes

        slots = []
        t = datetime.combine(appointment_date, opening)
        closing_dt = datetime.combine(appointment_date, closing)
        now = datetime.now()

        while t + timedelta(minutes=slot_length) <= closing_dt:
            slot_time = t.time()
            slot_datetime = datetime.combine(appointment_date, slot_time)
            # Only allow booking if slot is not booked AND slot datetime is in future
            if slot_time not in booked_times and slot_datetime > now:
                slots.append(slot_time.strftime("%H:%M"))
            t += timedelta(minutes=slot_length)
        available_slots = slots

    if request.method == "POST" and date_selected:
        time = request.POST.get("slot")
        if not date_selected or not time:
            messages.error(request, "Please select date and time slot.")
            return redirect(request.path_info + f"?date={date_selected}")

        # Extra check: slot not in booked_times and not in the past
        appointment_date = datetime.strptime(date_selected, "%Y-%m-%d").date()
        slot_datetime = datetime.combine(appointment_date, datetime.strptime(time, "%H:%M").time())
        if slot_datetime <= datetime.now():
            messages.error(request, "Cannot book a slot in the past.")
            return redirect(request.path_info + f"?date={date_selected}")

        exists = Appointment.objects.filter(
            shop=shop,
            service=service,
            date=date_selected,
            time=time
        ).exists()
        if exists:
            messages.error(request, "Sorry, slot already booked. Please choose another.")
            return redirect(request.path_info + f"?date={date_selected}")

        Appointment.objects.create(
            customer=customer, shop=shop, service=service, date=date_selected, time=time
        )
        messages.success(request, "Appointment booked. Waiting for approval.")
        return redirect("customer_home")

    context = {
        "shop": shop, "service": service,
        "date_selected": date_selected,
        "available_slots": available_slots,
    }
    return render(request, 'book_appointment.html', context)




def shop_detail(request, shop_id):
    shop = get_object_or_404(Barbershop, id=shop_id)
    return render(request, "shop_detail_customer.html", {"shop": shop})


@login_required
def add_review(request, shop_id):
    if request.user.usertype != "Customer":
        messages.error(request, "Unauthorized access.")
        return redirect("home")

    shop = get_object_or_404(Barbershop, id=shop_id, is_approved=True)
    customer = get_object_or_404(Customer, usrname=request.user)

    if request.method == "POST":
        rating = request.POST.get("rating")
        comment = request.POST.get("comment", "")
        try:
            rating_int = int(rating)
            if rating_int < 1 or rating_int > 5:
                raise ValueError()
        except Exception:
            messages.error(request, "Please provide rating between 1 and 5.")
            return redirect("add_review", shop_id=shop_id)

        Review.objects.create(customer=customer, shop=shop, rating=rating_int, comment=comment)
        messages.success(request, "Review submitted.")
        return redirect("customer_home")

    return render(request, 'add_review.html', {"shop": shop})


@login_required
def manage_shops(request):
    pending_shops = Barbershop.objects.filter(is_approved=False)
    approved_shops = Barbershop.objects.filter(is_approved=True)
    return render(request, "manage_shops.html", {
        "pending_shops": pending_shops,
        "approved_shops": approved_shops,
    })



# @login_required
# def approve_shop(request, shop_id):
#     shop = get_object_or_404(Barbershop, id=shop_id)
#     shop.is_approved = True
#     shop.save()
#     messages.success(request, f"Shop '{shop.shop_name}' approved successfully.")
#     return redirect("manage_shops")

# @login_required
# def reject_shop(request, shop_id):
#     shop = get_object_or_404(Barbershop, id=shop_id)
#     shop.delete()
#     messages.success(request, f"Shop '{shop.shop_name}' rejected and deleted.")
#     return redirect("manage_shops")

@login_required
def shop_detail_admin(request, shop_id):
    shop = get_object_or_404(Barbershop, id=shop_id)
    return render(request, "shop_detail_admin.html", {"shop": shop})


# -------------------
# MANAGE CUSTOMERS
# -------------------
@login_required
def manage_customers(request):
    customers = Customer.objects.all()
    customers = customers.annotate(appointment_count=Count('appointments'))
    max_appointments = customers.aggregate(max=Count('appointments'))['max'] or 0
    return render(request, "manage_customers.html", {
        "customers": customers,
        "max_appointments": max_appointments,
    })

@login_required
def customer_detail(request, customer_id):
    customer = get_object_or_404(Customer, id=customer_id)
    return render(request, "customer_detail.html", {"customer": customer})


# -------------------
# MANAGE APPOINTMENTS
# -------------------
@login_required
def manage_appointments(request):
    appointments = Appointment.objects.select_related("customer", "shop", "service").all()

    # Filtering
    search = request.GET.get('search', '').strip()
    status = request.GET.get('status', '')

    if search:
        appointments = appointments.filter(
            Q(customer__name__icontains=search) |
            Q(customer__usrname__username__icontains=search) |
            Q(shop__shop_name__icontains=search)
        )
    if status != '':
        appointments = appointments.filter(status=status)

    # For stats cards:
    pending_count = appointments.filter(status=0).count()
    approved_count = appointments.filter(status=1).count()
    rejected_count = appointments.filter(status=2).count()

    return render(request, "manage_appointments.html", {
        "appointments": appointments,
        "pending_count": pending_count,
        "approved_count": approved_count,
        "rejected_count": rejected_count,
    })

@login_required
def owner_appointments(request):
    if request.user.usertype != "Owner":
        messages.error(request, "Unauthorized access.")
        return redirect("home")
    shop = get_object_or_404(Barbershop, usrname=request.user)
    appointments = Appointment.objects.filter(shop=shop).order_by('-created_at')
    return render(request, 'owner_appointments.html', {
        "shop": shop,
        "appointments": appointments,
    })


# -------------------
# REPORTS
# -------------------
@login_required
def reports(request):
    shops_count = Barbershop.objects.count()
    customers_count = Customer.objects.count()
    appointments_count = Appointment.objects.count()
    review_count = Review.objects.count()

    # Top shops by appointment count
    top_shops = Barbershop.objects.annotate(
    total_appointments=Count("appointments")
    ).order_by("-total_appointments")[:5]

# Top rated shops
    top_rated = Barbershop.objects.annotate(
    avg_rating=Avg("reviews__rating")
    ).order_by("-avg_rating")[:5]

    return render(request, "reports.html", {
        "shops_count": shops_count,
        "customers_count": customers_count,
        "appointments_count": appointments_count,
        "review_count": review_count,
        "top_shops": top_shops,
        "top_rated": top_rated,
    })

from django.db.models import Count, Avg

@login_required
def owner_reports(request):
    if request.user.usertype != "Owner":
        messages.error(request, "Unauthorized access.")
        return redirect("home")
    shop = get_object_or_404(Barbershop, usrname=request.user)
    # Top services by appointment count
    top_services = shop.services.annotate(app_count=Count('appointment')).order_by('-app_count')[:5]
    # Top customers by appointment count
    top_customers = shop.appointments.values('customer__name').annotate(app_count=Count('id')).order_by('-app_count')[:5]
    # Average rating
    avg_rating = shop.reviews.aggregate(avg=Avg("rating"))["avg"]
    context = {
        "shop": shop,
        "top_services": top_services,
        "top_customers": top_customers,
        "avg_rating": avg_rating,
    }
    return render(request, 'owner_report.html', context)


@login_required
def manage_services(request, shop_id):
    if request.user.usertype != "Owner":
        messages.error(request, "Unauthorized access.")
        return redirect("home")

    shop = get_object_or_404(Barbershop, id=shop_id, usrname=request.user)

    # Add a new service
    if request.method == "POST" and "add_service" in request.POST:
        service_name = request.POST.get("service_name")
        price = request.POST.get("price")
        image = request.FILES.get("image")

        if service_name and price:
            Service.objects.create(
                shop=shop,
                service_name=service_name,
                price=price,
                image=image
            )
            messages.success(request, "Service added successfully!")
            return redirect("manage_services", shop_id=shop.id)
        else:
            messages.error(request, "Please fill all fields.")

    # Delete a service
    if request.method == "POST" and "delete_service" in request.POST:
        service_id = request.POST.get("delete_service")
        service = get_object_or_404(Service, id=service_id, shop=shop)
        service.delete()
        messages.success(request, "Service deleted successfully.")
        return redirect("manage_services", shop_id=shop.id)

    services = Service.objects.filter(shop=shop)

    return render(request, "manage_services.html", {
        "shop": shop,
        "services": services,
    })

# @login_required
# def shop_detail_customer(request, shop_id):
#     shop = get_object_or_404(Barbershop, id=shop_id, is_approved=True)
#     return render(request, "shop_detail_customer.html", {"shop": shop})



@login_required
def shop_detail_customer(request, shop_id):
    shop = get_object_or_404(Barbershop, id=shop_id, is_approved=True)
    customer = None
    can_review = False
    has_appointment = False
    already_reviewed = False

    # Eligibility logic
    if request.user.is_authenticated and request.user.usertype == "Customer":
        try:
            customer = Customer.objects.get(usrname=request.user)
            has_appointment = Appointment.objects.filter(
                customer=customer, shop=shop, status=3
            ).exists()
            already_reviewed = Review.objects.filter(
                customer=customer, shop=shop
            ).exists()
            can_review = has_appointment and not already_reviewed
        except Customer.DoesNotExist:
            pass

    # Handle review form POST
    if request.method == "POST" and can_review:
        rating = int(request.POST.get("rating", 5))
        comment = request.POST.get("comment", "")
        Review.objects.create(
            customer=customer, shop=shop, rating=rating, comment=comment
        )
        messages.success(request, "Thank you for your review!")
        return redirect("shop_detail_customer", shop_id=shop_id)

    context = {
        "shop": shop,
        "can_review": can_review,
        "has_appointment": has_appointment,
        "already_reviewed": already_reviewed,
    }
    return render(request, "shop_detail_customer.html", context)

def shop_list(request):
    # Get all approved shops
    shops = Barbershop.objects.filter(is_approved=True)

    # Get filter/search parameters from GET
    q = request.GET.get('q', '')
    service_id = request.GET.get('service', '')
    location = request.GET.get('location', '')

    # Filter by search text (name, address, or service)
    if q:
        shops = shops.filter(
            Q(shop_name__icontains=q) |
            Q(shop_address__icontains=q) |
            Q(services__service_name__icontains=q)
        ).distinct()

    # Filter by service
    if service_id:
        shops = shops.filter(services__id=service_id)

    # Filter by location (if you want, or skip if not needed)
    if location:
        shops = shops.filter(shop_address__icontains=location)

    # For dropdowns
    services = Service.objects.all()
    locations = Barbershop.objects.values_list('shop_address', flat=True).distinct()

    context = {
        'shops': shops.distinct(),
        'services': services,
        'locations': locations,
    }
    return render(request, 'shop_list.html', context)


@login_required
def complete_appointment(request, appointment_id):
    appointment = get_object_or_404(Appointment, id=appointment_id)
    # Only the shop owner (who owns the shop) can complete it
    if request.user.usertype == "Owner" and appointment.shop.usrname == request.user:
        if appointment.status == 1:  # Only approved appointments can be completed
            appointment.status = 3   # 3 = Completed
            appointment.save()
            messages.success(request, "Appointment marked as completed.")
        else:
            messages.warning(request, "Only approved appointments can be marked as completed.")
    else:
        messages.error(request, "Unauthorized.")
    return redirect("shopowner_home")