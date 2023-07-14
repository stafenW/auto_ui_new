from django.shortcuts import render


def index(request):
    return render(request, 'index.html')


# async def async_view(request):
#     response = JsonResponse({'code': 0})
#     asyncio.create_task(run_all_cases())
#     return response
