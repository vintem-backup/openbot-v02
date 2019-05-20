from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Pair
from .forms import PairForm

@login_required
def pairs_list(request):
    pairs = Pair.objects.all()
    return render(request, 'getdata/pairs_overview.html', {'var_pairs':pairs})


@login_required
def pair_new(request):
    form = PairForm(request.POST or None, request.FILES or None)
    if form.is_valid():
        form.save()
        return redirect('listofpairs')
    return render(request, 'getdata/pair_form.html',{'var_form':form})

@login_required
def pair_update(request,id):
    pair = get_object_or_404(Pair, pk=id)
    form = PairForm(request.POST or None, instance=pair)
    if form.is_valid():
        form.save()
        return redirect('listofpairs')
    return render(request, 'getdata/pair_form.html',{'var_form':form})
'''
@login_required
def person_delete(request,id):
    pessoa = get_object_or_404(Person, pk=id)

    if request.method == 'POST':
        pessoa.delete()
        return redirect('person_list')

    return render(request, 'person_delete_confirm.html',{'var_pessoa':pessoa})
'''