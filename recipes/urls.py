from django.urls import path
from recipes import views
from recipes.views import RecipeCreationView, CommentAddingView, CommentDeleterView, SpecificRecipeView, \
    RecipeDeleterView, PendingRecipesView, PendingRecipeApprovalView, PendingCommentView, CommentApprovalView

urlpatterns = [
    path('add-a-recipe/', RecipeCreationView.as_view(), name='add-recipe'),
    path('recipe/<pk>', SpecificRecipeView.as_view(), name='specific-recipe'),

    path('pdf-view/<pk>', views.get_pdf, name='pdf'),

    path('delete-recipe/<pk>', RecipeDeleterView.as_view(), name='delete-recipe'),
    path('leave-comment/<pk>', CommentAddingView.as_view(), name='leave-comment'),

    path('delete-comment/<pk>', CommentDeleterView.as_view(), name='delete-comment'),


    # admin
    path('pending-recipes/', PendingRecipesView.as_view(), name='pending-recipes'),
    path('pending-comments/', PendingCommentView.as_view(), name='pending-comments'),

    path('approve-recipe/<pk>/', PendingRecipeApprovalView.as_view(), name='approve-recipe'),
    path('approve-comment/<pk>/', CommentApprovalView.as_view(), name='approve-comment')
]