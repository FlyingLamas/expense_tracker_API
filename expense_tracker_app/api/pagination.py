from rest_framework.pagination import PageNumberPagination

class ExpenseListPagination(PageNumberPagination):
    page_size = 10   
    # page_query_param = "p"  # This shows in url
    page_size_query_param = "size"  # Gives client power to choose how many records should be displayed on a page
    max_page_size = 10
    # last_page_strings = "last"
    
