from rest_framework.decorators import api_view
from rest_framework import status
from expense_tracker_app.models import Expense
from expense_tracker_app.api.serializers import ExpenseSerializer
from rest_framework.response import Response
from rest_framework.views import APIView

# For permissions
from rest_framework.permissions import IsAuthenticated

# Generics
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView, RetrieveAPIView, ListAPIView

# Filter Backend
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters

# For Pagination
from expense_tracker_app.api.pagination import ExpenseListPagination


# @api_view(["GET", "POST"])
# def expense_list(request):
    
#     if not request.user.is_authenticated:
#         return Response({"error": "Not Allowed to visit."}, status = status.HTTP_403_FORBIDDEN)
    
#     else:
#         if request.method == "GET":
#             expense = Expense.objects.filter(owner = request.user)
#             serializer = ExpenseSerializer(expense, many = True)
#             return Response(serializer.data, status = status.HTTP_200_OK)
        
#         elif request.method == "POST":
#             serializer = ExpenseSerializer(data = request.data)
#             if serializer.is_valid():
#                 serializer.save(owner = request.user)   # We are passing onwer in brackets because our model has a field owner and request.data does not have that information. so for saving we will have to pass that information, in brackets.
#                 return Response(serializer.data, status = status.HTTP_201_CREATED)
#             else:
#                 return Response(serializer.errors, status = status.HTTP_400_BAD_REQUEST)
            
# @api_view(["GET", "PUT", "DELETE"])
# def expense_detail(request, pk):
    
#     if not request.user.is_authenticated:
#             return Response({"error": "Not Allowed to visit."}, status = status.HTTP_403_FORBIDDEN)
    
#     else:   
#         try:
#             expense = Expense.objects.get(pk = pk)
#         except Expense.DoesNotExist:
#             return Response({"errors": "Expense not found"}, status = status.HTTP_404_NOT_FOUND, )    
        
#         if expense.owner != request.user:
#             return Response({"error": "Unauthorized"}, status = status.HTTP_403_FORBIDDEN)
        
#         else:    
#             if request.method == "GET":
#                 serializer = ExpenseSerializer(expense)
#                 return Response(serializer.data, status = status.HTTP_200_OK)
            
#             elif request.method == "PUT":
#                 serializer = ExpenseSerializer(expense, data = request.data)
#                 if serializer.is_valid():
#                     serializer.save()
#                     return Response(serializer.data, status = status.HTTP_200_OK)
#                 else:
#                     return Response(serializer.errors, status = status.HTTP_400_BAD_REQUEST)
            
#             elif request.method == "DELETE":      
#                 expense.delete()
#                 return Response(status = status.HTTP_204_NO_CONTENT)


        
# Switched to CBV because we wanted to implement filtering, which works naturally for CBVs   
# from rest_framework.views import APIView

# class ExpenseListAV(APIView):
    
#     permission_classes = [IsAuthenticated]
    
#     def get(self, request):
#         expense = Expense.objects.filter(owner = request.user)
#         serializer = ExpenseSerializer(expense, many = True)
#         return Response(serializer.data, status = status.HTTP_200_OK)
    
#     def post(self, request):
#         serializer = ExpenseSerializer(data = request.data)
#         if serializer.is_valid():
#             serializer.save(owner = request.user)
#             return Response(serializer.data, status = status.HTTP_201_CREATED)
#         else:
#             return Response(serializer.errors, status = status.HTTP_400_BAD_REQUEST)     
        
# class ExpenseDetailAV(APIView):
#     permission_classes = [IsAuthenticated]
    
#     def get(self, request, pk):
#         try:
#             expense = Expense.objects.get(pk = pk)
#         except Expense.DoesNotExist:
#             return Response({"error": "Does not exist"})
        
#         if expense.owner != request.user:
#             return Response({"error": "Unauthorized"}, status = status.HTTP_403_FORBIDDEN)
#         else:
#             serializer = ExpenseSerializer(expense)
#             return Response(serializer.data, status = status.HTTP_200_OK)
    
#     def put(self, request, pk):
#         expense = Expense.objects.get(pk = pk)
        
#         if expense.owner != request.user:
#             return Response({"error": "Unauthorized"}, status = status.HTTP_403_FORBIDDEN)
#         else:
#             serializer = ExpenseSerializer(expense, data = request.data)
#             if serializer.is_valid():
#                 serializer.save()
#                 return Response(serializer.data, status = status.HTTP_200_OK)
#             else:
#                 return Response(serializer.errors, status = status.HTTP_400_BAD_REQUEST)
        
#     def delete(self, request, pk):
#         expense = Expense.objects.get(pk = pk)
#         if expense.owner != request.user:
#             return Response({"error": "Unauthorized"}, status = status.HTTP_403_FORBIDDEN)
#         else:
#             expense.delete()
#             return Response(status = status.HTTP_204_NO_CONTENT)

        
# Using Generics
class ExpenseListView(ListCreateAPIView):
    # queryset = Expense.objects.all()  # We dont like this, because if we do every user will be able to see everyone's expenses
                                        # So we overwrite it with get_queryset Method, where we filter the expenses only for the logged in user.
    serializer_class = ExpenseSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['category', 'expense_date']
    search_fields = ["title", "description"]
    ordering_fields = ["amount", "expense_date"]  
    
    pagination_class = ExpenseListPagination  
    
    def get_queryset(self):
        return Expense.objects.filter(owner = self.request.user)
    
    # We are using this following field to because we have an extra field which DRF does not know about
    # if not we could simply write serializer.save(), but we have an owner field and this data is not in POST data. thus we have to write perform_create.
    def perform_create(self, serializer):
        serializer.save(owner = self.request.user)
    # So if we did not have any extra fields we could have completely skipped this perform create method and DRF would have saved the data
    # And perform_create is ONLY used when new data is created - that happens in POST.
    
class ExpenseDetailView(RetrieveUpdateDestroyAPIView):
    serializer_class = ExpenseSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        return Expense.objects.filter(owner = self.request.user)
    
from django.db.models import Avg, Sum, Max, Min, Count

class ReportView(RetrieveAPIView):
    
    permission_classes = [IsAuthenticated]
    
    def get(self, request, *args, **kwargs):
        queryset = Expense.objects.filter(owner = request.user)
        summary = queryset.aggregate(
            Sum("amount"),
            Avg("amount"),
            Max("amount"),
            Min("amount"),
            Count("id"),
        )
        
        return Response(summary, status = status.HTTP_200_OK)
    
class CategoryView(ListAPIView):
    
    permission_classes = [IsAuthenticated]
    
    def get(self, request, *args, **kwargs):
        queryset = Expense.objects.filter(owner = request.user).values("category")
        summary = queryset.annotate(
            Total_amount = Sum("amount"),
            Average = Avg("amount"),
            Maximum_amount = Max("amount"),
            Minimum_amount = Min("amount"),
            Number_of_items = Count("id"),
        )
        
        return Response(summary, status = status.HTTP_200_OK)

class MonthlyReportView(APIView):
    """
    We are using APIView because it gives us full control over our logic.
    In the monthly report we are performing custom filtering(month, year.
    Generic Views like ListAPIView, RetrieveAPIView, etc are meant for CRUD patterns with predefined logic
    For custom reports, analytics, etc. there are no model instance to retrieve or create, so APIView is preferred.
    """
    # for accessing for particalur month use following url
    # http://127.0.0.1:8000/expense/monthly-report/?month=11&year=2025
    
    permission_classes = [IsAuthenticated]
    
    def get(self, request, *args, **kwargs):
        month = request.query_params.get("month")
        year = request.query_params.get("year")
        
        queryset = Expense.objects.filter(
            owner = request.user,
            expense_date__month = month,
            expense_date__year = year
        )
        
        summary = queryset.aggregate(
            total_amount = Sum("amount"),
            avg_amount = Avg("amount"),
            max_amount = Max("amount"),
            min_amount = Min("amount"),
            count = Count("id"),
        )
        return Response(summary, status = status.HTTP_200_OK)
