from django.shortcuts import get_object_or_404, render
from django.http import HttpResponseRedirect
from datetime import datetime

from members.models import Members
from members.forms import MemberForm


def index(request):
    latest_memeber_list = Members.objects.order_by("created_at")[:10]
    context = {"members": latest_memeber_list, "form": MemberForm()}

    if request.method == "POST":
        form = MemberForm(request.POST)
        if form.is_valid:
            name = form.data["name"]
            email = form.data["email"]
            password = form.data["password"]

            Members.objects.create(name=name, email=email, password=password)

    return render(request, "members.html", context)


def update(request, id):
    latest_member_list = Members.objects.order_by("created_at")[:10]
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
