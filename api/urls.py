from django.urls import path
from .views import *
urlpatterns = [
    path('register/', register,name='register'),
    path('me/', current_user,name='me'),
    path('me/update/', update_user,name='update-user'),
    path('forget_password/', forgot_password,name='forget-password'),
    path('reset_password/<str:token>', reset_password, name="reset_password"),

    path('compte_filter/', CompteAPIView.as_view(), name='DemChqDt-list'),
    path('compte_ouvert/', CompteDatouvNotNullAPIView.as_view(), name='export-table-query'),
    path('compte_depot/', CompteDeposite.as_view(), name='depot-table-query'),
    path('client/', Client.as_view(), name='client_query'),
    

    path('virement/', Virement.as_view(), name='virement_table_query'),
    path('virement_intern/', VirementIntern.as_view(), name='virement_intern_table_query'),
    
    path('guichet/', Guichet.as_view(), name='guichet_table_query'),
    path('parque_guichet/', OperatioGuichetView.as_view(), name='parque_guichet_table_query'),

    



    ###-----parque compte -----------------######
    path('parque_count/', LibelleCountView.as_view(), name='libelle-count'),
    path('compte_details/', CompteDetailsView.as_view(), name='client-details'),
    path('parque_depot/', ProduitDepotView.as_view(), name='produit-depot'),
    path('depot_details/', ClientComptePosdevView.as_view(), name='client-compte-posdev'),
    path('parque_client/', ClientDataAPIView.as_view(), name='client_data_api'),
    path('details_parque_compte/', DtailsCompte.as_view(), name='client_data_api'),
    
    
]