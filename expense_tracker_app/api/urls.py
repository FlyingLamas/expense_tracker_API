from django.urls import path
from expense_tracker_app.api.views import ExpenseListView, ExpenseDetailView, ReportView, CategoryView, MonthlyReportView

urlpatterns = [
    path("expense/", ExpenseListView.as_view(), name = "expense-list"),
    path("expense/<int:pk>/", ExpenseDetailView.as_view(), name = "expense-detail"),
    path("expense/summary/", ReportView.as_view(), name = "summary"),
    path("expense/category/", CategoryView.as_view(), name = "category"),
    path("expense/monthly-report/", MonthlyReportView.as_view(), name = "monthly-report")
    
]


