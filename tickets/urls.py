from django.urls import path
from . import views

urlpatterns = [
    # Support Tickets
    path('tickets/create/', views.SupportTicketCreateView.as_view(), name='ticket-create'),
    path('tickets/', views.SupportTicketListView.as_view(), name='ticket-list'),
    path('tickets/<int:pk>/', views.SupportTicketDetailView.as_view(), name='ticket-detail'),
    
    # Issue Reports
    path('issues/create/', views.IssueReportCreateView.as_view(), name='issue-create'),
]