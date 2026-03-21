import json
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import get_object_or_404, render
from django.contrib.auth.decorators import login_required

from dashboard.models import Menu, MenuItem, Page, Category
from dashboard.decorators import staff_member_required


@staff_member_required
def menu_items_manage(request, pk):
    """Dynamic menu item management with drag-and-drop functionality"""
    menu = get_object_or_404(Menu, pk=pk)
    
    # Get all top-level items with their children
    menu_items = MenuItem.objects.filter(menu=menu, parent=None).prefetch_related('children')
    pages = Page.objects.filter(status='active')
    categories = Category.objects.filter(status='active')
    
    context = {
        'menu': menu,
        'menu_items': menu_items,
        'pages': pages,
        'categories': categories,
    }
    return render(request, 'dashboard/menu_items_manage.html', context)


@staff_member_required
@require_POST
def menu_item_create_ajax(request):
    """Create a new menu item via AJAX"""
    try:
        data = json.loads(request.body)
        menu_id = data.get('menu_id')
        title = data.get('title', '').strip()
        icon = data.get('icon', '').strip()
        item_type = data.get('type', 'custom_link')
        url = data.get('url', '').strip()
        page_id = data.get('page_id')
        category_id = data.get('category_id')
        parent_id = data.get('parent_id') or None

        if not title:
            return JsonResponse({'success': False, 'error': 'Title is required'})

        menu = get_object_or_404(Menu, pk=menu_id)

        # Determine URL based on type
        if item_type == 'page' and page_id:
            page = get_object_or_404(Page, pk=page_id)
            url = page.get_absolute_url()
        elif item_type == 'category' and category_id:
            category = get_object_or_404(Category, pk=category_id)
            url = category.get_absolute_url()

        # Get max order for this level
        queryset = MenuItem.objects.filter(menu=menu, parent_id=parent_id)
        max_order = queryset.count()

        item = MenuItem.objects.create(
            menu=menu,
            title=title,
            icon=icon,
            type=item_type,
            url=url,
            page_id=page_id if item_type == 'page' else None,
            parent_id=parent_id,
            order=max_order,
            is_active=True
        )

        return JsonResponse({
            'success': True,
            'item': {
                'id': item.id,
                'title': item.title,
                'icon': item.icon,
                'type': item.type,
                'url': item.url,
                'order': item.order,
            }
        })
    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)})


@staff_member_required
@require_POST
def menu_item_update_ajax(request, pk):
    """Update a menu item via AJAX"""
    try:
        data = json.loads(request.body)
        item = get_object_or_404(MenuItem, pk=pk)

        item.title = data.get('title', item.title)
        item.icon = data.get('icon', item.icon)
        item.url = data.get('url', item.url)
        item.css_class = data.get('css_class', item.css_class)
        item.target = data.get('target', item.target)
        item.is_active = data.get('is_active', item.is_active)

        if 'page_id' in data and item.type == 'page':
            item.page_id = data['page_id']
            if item.page:
                item.url = item.page.get_absolute_url()

        item.save()

        return JsonResponse({'success': True})
    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)})


@staff_member_required
@require_POST
def menu_item_delete_ajax(request, pk):
    """Delete a menu item via AJAX"""
    try:
        item = get_object_or_404(MenuItem, pk=pk)
        item.delete()
        return JsonResponse({'success': True})
    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)})


@staff_member_required
@require_POST
def menu_item_reorder_ajax(request):
    """Reorder menu items via AJAX (drag and drop)"""
    try:
        data = json.loads(request.body)
        items = data.get('items', [])
        
        for item_data in items:
            item_id = item_data.get('id')
            parent_id = item_data.get('parent_id') or None
            order = item_data.get('order', 0)
            
            MenuItem.objects.filter(pk=item_id).update(
                parent_id=parent_id,
                order=order
            )
        
        return JsonResponse({'success': True})
    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)})


@staff_member_required
def menu_item_get_ajax(request, pk):
    """Get menu item details via AJAX"""
    try:
        item = get_object_or_404(MenuItem, pk=pk)
        return JsonResponse({
            'success': True,
            'item': {
                'id': item.id,
                'title': item.title,
                'type': item.type,
                'url': item.url,
                'icon': item.icon,
                'page_id': item.page_id,
                'css_class': item.css_class,
                'target': item.target,
                'is_active': item.is_active,
            }
        })
    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)})
