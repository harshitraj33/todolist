from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import View, DeleteView
from django.forms import modelform_factory, ModelForm
from django.forms.widgets import DateTimeInput
from django.urls import reverse_lazy
from .models import List, Item

ListForm = modelform_factory(List, fields=['name', 'due_date'], widgets={'due_date': DateTimeInput(attrs={'type': 'datetime-local'})})

class ItemForm(ModelForm):
    class Meta:
        model = Item
        fields = ['text', 'due_date']
        widgets = {
            'due_date': DateTimeInput(attrs={'type': 'datetime-local'}),
        }

class ListListView(View):
    def get(self, request):
        lists = List.objects.prefetch_related('item_set').all()
        form = ListForm()
        lists_with_forms = [(list_obj, ItemForm()) for list_obj in lists]
        return render(request, 'app/list_list.html', {'object_list': lists, 'form': form, 'lists_with_forms': lists_with_forms})

    def post(self, request):
        form = ListForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('list_list')
        lists = List.objects.prefetch_related('item_set').all()
        lists_with_forms = [(list_obj, ItemForm()) for list_obj in lists]
        return render(request, 'app/list_list.html', {'object_list': lists, 'form': form, 'lists_with_forms': lists_with_forms})

class ListDetailView(View):
    def get(self, request, pk):
        list_obj = get_object_or_404(List, pk=pk)
        items = list_obj.item_set.all()
        form = ItemForm()
        return render(request, 'app/list_detail.html', {'list': list_obj, 'object_list': items, 'form': form})

    def post(self, request, pk):
        list_obj = get_object_or_404(List, pk=pk)
        form = ItemForm(request.POST)
        if form.is_valid():
            item = form.save(commit=False)
            item.list = list_obj
            item.save()
            return redirect('list_detail', pk=pk)
        items = list_obj.item_set.all()
        return render(request, 'app/list_detail.html', {'list': list_obj, 'object_list': items, 'form': form})

class ListDeleteView(DeleteView):
    model = List
    success_url = reverse_lazy('list_list')

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        self.object.delete()
        return redirect(self.get_success_url())

class ItemDeleteView(DeleteView):
    model = Item

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        self.object.delete()
        return redirect(self.get_success_url())

    def get_success_url(self):
        return reverse_lazy('list_detail', kwargs={'pk': self.object.list.pk})

class ItemToggleView(View):
    def post(self, request, pk):
        item = get_object_or_404(Item, pk=pk)
        item.completed = not item.completed
        item.save()
        return redirect('list_list')

class AddItemView(View):
    def post(self, request, pk):
        list_obj = get_object_or_404(List, pk=pk)
        form = ItemForm(request.POST)
        if form.is_valid():
            item = form.save(commit=False)
            item.list = list_obj
            item.save()
            return redirect('list_list')
        return redirect('list_list')
