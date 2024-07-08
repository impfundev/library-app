from django.shortcuts import get_object_or_404, render
from django.http import HttpResponseRedirect
from django.db.models import Q
from datetime import datetime

from members.models import Members
from members.forms import MemberForm
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage


def index(request):
    members = Members.objects.order_by("created_at")
    context = {"members": members, "form": MemberForm()}

    default_page = 1
    page = request.GET.get("page", default_page)
    items_per_page = 5
    paginator = Paginator(members, items_per_page)

    try:
        page_obj = paginator.page(page)
        context["page_obj"] = page_obj
        context["members"] = page_obj

    except PageNotAnInteger:
        page_obj = paginator.page(default_page)
        context["page_obj"] = page_obj
        context["members"] = page_obj

    except EmptyPage:
        page_obj = paginator.page(paginator.num_pages)
        context["page_obj"] = page_obj
        context["members"] = page_obj

    if request.method == "POST":
        form = MemberForm(request.POST)
        if form.is_valid:
            name = form.data["name"]
            email = form.data["email"]
            password = form.data["password"]

            Members.objects.create(name=name, email=email, password=password)

    if request.method == "GET":
        keyword = request.GET.get("q")
        order = request.GET.get("o")

        if keyword is not None:

            filtered_book_list = Members.objects.filter(
                Q(name__icontains=keyword) | Q(email__icontains=keyword)
            ).order_by("-created_at")
            context["members"] = filtered_book_list

        if order == "new":

            context["members"] = Members.objects.all().order_by("-updated_at")
        elif order == "old":

            context["members"] = Members.objects.all().order_by("updated_at")

    return render(request, "members.html", context)


def update(request, id):
    latest_member_list = Members.objects.order_by("created_at")
    context = {"members": latest_member_list}
    member = Members.objects.get(id=id)
    initial = {
        "name": member.name,
        "email": member.email,
        "password": member.password,
    }
    form = MemberForm(request.POST or None, initial=initial)

    if request.method == "POST":
        if form.is_valid:
            name = form.data["name"]
            email = form.data["email"]
            password = form.data["password"]
            member = Members.objects.filter(id=id)

            member.update(
                name=name, email=email, password=password, updated_at=datetime.now()
            )

            return HttpResponseRedirect("/dashboard/members")

    context["form"] = form
    context["member_id"] = id
    return render(request, "members_update_form.html", context)


def delete(request, id):
    context = {}
    member = get_object_or_404(Members, id=id)

    if request.method == "POST":
        member.delete()

        return HttpResponseRedirect("/dashboard/members")

    return render(request, "members.html", context)
