from django.shortcuts import render,get_object_or_404
from rest_framework.decorators import api_view,permission_classes
from rest_framework.response import Response
from django.contrib.auth.hashers import make_password
from rest_framework.permissions import IsAuthenticated
from django.utils.crypto import get_random_string
from datetime import datetime, timedelta
from django.core.mail import send_mail
from .serializers import * 
from utils.helpers import get_current_host
from rest_framework.permissions import AllowAny
from rest_framework.views import APIView
from rest_framework import generics, status
from rest_framework.pagination import PageNumberPagination
from .models import *


# Create your views here.
@api_view(['POST'])
def register(request):
    data = request.data
    user = SignUpSerializer(data=data)

    if user.is_valid():
        if not User.objects.filter(username=data['username']).exists():
            user = User.objects.create(
                first_name = data['first_name'],
                last_name = data['last_name'],
                email = data['email'] ,
                username = data['username'] ,
                password = make_password(data['password']) 
            )
            return Response({'message':'User Registered'},status=status.HTTP_201_CREATED)
        else:
            return Response({'message':'User already exists'},status=status.HTTP_400_BAD_REQUEST)    
    else:
        return Response({})
    

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def current_user(request):
    user = UserSerializer(request.user)
    return Response(user.data)


@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def update_user(request):
    user = request.user
    data = request.data

    user.first_name = data['first_name']
    user.last_name = data['last_name']
    user.username = data['email']
    user.email = data['email']

    if data['password'] != "":
        user.password = make_password(data['password'])

    user.save()
    serializer = UserSerializer(user,many= False)

    return Response(serializer.data)    



#froget password 

# import matplotlib.pyplot as plt
# import io

# def generate_chart():
#     # Créez un graphique (par exemple, un graphique simple)
#     plt.figure(figsize=(6, 4))
#     plt.plot([1, 2, 3, 4], [1, 4, 9, 16], label="Courbe d'exemple")
#     plt.xlabel("X")
#     plt.ylabel("Y")
#     plt.title("Graphique Exemple")

#     # Sauvegarder le graphique dans un fichier en mémoire
#     img_buffer = io.BytesIO()
#     plt.savefig(img_buffer, format='png')
#     img_buffer.seek(0)  # Revenir au début du fichier
#     return img_buffer

# from django.core.mail import EmailMessage
# from django.utils.html import strip_tags
# from io import BytesIO
# from django.conf import settings

# @api_view(['POST'])
# @permission_classes([AllowAny])
# def forgot_password(request):
#     data = request.data

#     user = get_object_or_404(User, email=data['email'])

#     token = get_random_string(40)
#     expire_date = datetime.now() + timedelta(minutes=5)

#     user.profile.reset_password_token = token
#     user.profile.reset_password_expire = expire_date
#     user.profile.save()

#     # Use the Angular application's domain here
#     frontend_host = "http://localhost:5173"  # Replace with your Angular app's domain
#     link = f"{frontend_host}/reset-password/{token}"

#     body = f"Le lien de réinitialisation de votre mot de passe est : {link}"

#     # Générer un graphique (exemple avec matplotlib)
#     img_buffer = generate_chart()  # Cette fonction génère et renvoie un graphique en mémoire

#     # Créer un message email avec l'image
#     email = EmailMessage(
#         subject="Réinitialisation de mot de passe pour Tableau de Board",
#         body=body,
#         from_email="aubnet@aub.mr",
#         to=[data['email']]
#     )

#     # Ajouter l'image comme pièce jointe
#     email.attach('chart.png', img_buffer.read(), 'image/png')

#     # Envoyer l'email
#     email.send()

#     return Response({'message': f'Password reset email sent to: {data["email"]}'})

@api_view(['POST'])
@permission_classes([AllowAny])
def forgot_password(request):
    data = request.data

    user = get_object_or_404(User, email=data['email'])

    token = get_random_string(40)
    expire_date = datetime.now() + timedelta(minutes=5)

    user.profile.reset_password_token = token
    user.profile.reset_password_expire = expire_date
    user.profile.save()

    # Use the Angular application's domain here
    frontend_host = "http://localhost:5173"  # Replace with your Angular app's domain
    link = f"{frontend_host}/reset-password/{token}"

    body = f"Le lien de réinitialisation de votre mot de passe est : {link}"

    send_mail(
        "Réinitialisation de mot de passe pour Tableau de Board",
        body,
        "aubnet@aub.mr",
        [data['email']]
    )

    return Response({'message': f'Password reset email sent to: {data["email"]}'})

# reset password


@api_view(['POST'])
@permission_classes([AllowAny])
def reset_password(request, token):
    data = request.data

    try:
        # Trouver l'utilisateur avec le token de réinitialisation
        user = get_object_or_404(User, profile__reset_password_token=token)

        # Vérifier si le token a expiré
        if user.profile.reset_password_expire.replace(tzinfo=None) < datetime.now():
            return Response({'error': 'Token expired'}, status=status.HTTP_400_BAD_REQUEST)

        # Vérifier que les mots de passe correspondent
        if data['password'] != data['confirmPassword']:
            return Response({'error': 'Passwords are not the same'}, status=status.HTTP_400_BAD_REQUEST)

        # Réinitialiser le mot de passe
        user.password = make_password(data['password'])
        user.profile.reset_password_token = ""  # Vider le token après utilisation
        user.profile.reset_password_expire = None  # Vider la date d'expiration

        # Sauvegarder les modifications
        user.profile.save()
        user.save()

        return Response({'details': 'Password reset successfully'}, status=status.HTTP_200_OK)

    except KeyError as e:
        return Response({'error': f'Missing key: {str(e)}'}, status=status.HTTP_400_BAD_REQUEST)
    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)






class DemChqDtlListAPIView(APIView):
    def get(self, request):
        # Récupérez tous les documents
        demChqDtl = DemChqDtl.objects.all()
        serializer = DemChqDtlSerializer(demChqDtl, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)   




# 
# Assurez-vous que votre serializer est bien défini

class ExportTableQueryView(APIView):
    def get(self, request, *args, **kwargs):
        try:
            # Votre requête SQL brute
            query = """
            SELECT A.OPER,
                   A."COMPTEC" AS COMPTE_BENEF, 
                   TRIM(A.NOMBE) AS BENEFICIAIRE, 
                   A.DATOPER AS DATE_TRANSACTION, 
                   TRIM(A.DEVISE) AS DEVISE, 
                   'CD' AS MODE_REGLEMENT, 
                   ROUND(A.MNTDEVC, 2) AS MONTANT_TRANSACTION, 
                   NVL(NVL((SELECT I.NUMID 
                            FROM AUB.TITU T, AUB.IDP I 
                            WHERE T.CLIENT = C.CLIENT AND T.IDP = I.IDP),
                           (SELECT IDM.TIN1 
                            FROM AUB.TITU T, AUB.CLI M1, AUB.IDM 
                            WHERE T.CLIENT = M1.CLIENT AND T.CLIENT = C.CLIENT 
                            AND T.IDM = IDM.IDM 
                            AND NVL(T.VALIDE, 'N') = 'V')),' ') AS NIF_NNI,
                   A.COMPTED AS COMPTE_DON,
                   A.DORDRED AS NOM_DONNEUR_ORDRE,
                   (SELECT NOM FROM AUB.PAYS WHERE PAYS = A.PAYS) AS PAYS, 
                   'PRODUIT' AS PRODUIT, 
                   A.NOOPER AS REFERENCE_TRANSACTION, 
                   A.COURS12 AS TAUX_CHANGE, 
                   A.DEVISED AS DEVISE_DEBIT, 
                   A.DEVISEC AS DEVISE_CREDIT, 
                   A.MNTDEVD AS MONTANT_DEBIT, 
                   A.MNTDEVC AS MONTANT_CREDIT
            FROM AUB.VIREST A
            JOIN AUB.CPT C ON A.COMPTED = C.COMPTE
            WHERE A.VALIDE = 'V'
            AND C."COMPTEC" NOT LIKE '011000%'
            ORDER BY A.DATOPER
            """

            # Exécutez la requête en utilisant un curseur
            with connection.cursor() as cursor:
                cursor.execute(query)
                rows = cursor.fetchall()

            # Préparez les résultats pour l'API en format JSON
            result = []
            for row in rows:
                result.append({
                    'oper': row[0],
                    'compte_benef': row[1],
                    'beneficiaire': row[2],
                    'date_transaction': row[3],
                    'devise': row[4],
                    'mode_reglement': row[5],
                    'montant_transaction': row[6],
                    'nif_nni': row[7],
                    'compte_don': row[8],
                    'nom_donneur_ordre': row[9],
                    'pays': row[10],
                    'produit': row[11],
                    'reference_transaction': row[12],
                    'taux_change': row[13],
                    'devisd_debit': row[14],
                    'devise_credit': row[15],
                    'montant_debit': row[16],
                    'montant_credit': row[17]
                })

            # Retournez les résultats sous forme de réponse JSON
            return Response(result, status=status.HTTP_200_OK)

        except Exception as e:
            # En cas d'erreur, retournez l'exception
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class CompteAPIView1(APIView):
    serializer_class = CptSerializer

    def get(self, request, *args, **kwargs):
        # Récupérer tous les comptes (ou selon un filtre que vous souhaitez)
        comptes = Cpt.objects.all()

        # Pagination des résultats
        paginator = PageNumberPagination()
        paginator.page_size = 9  # Limiter les résultats par page à 16
        paginated_results = paginator.paginate_queryset(comptes, request)

        # Sérialisation des résultats paginés
        serializer = self.serializer_class(paginated_results, many=True)

        # Retourner les résultats paginés avec la réponse JSON
        return paginator.get_paginated_response(serializer.data)





class CompteAPIView(APIView):
    serializer_class = CptSerializer

    def get(self, request, *args, **kwargs):
        # Récupérer les critères de recherche depuis les paramètres de la requête
        client_filter = request.GET.get('CLIENT', None)
        compte_filter = request.GET.get('COMPTE', None)
        datouv_filter = request.GET.get('DATOUV', None)
        datfrm_filter = request.GET.get('DATFRM', None)
        agence_filter = request.GET.get('AGENCE', None)
        ncg_filter = request.GET.get('NCG','210')  # Ajouter un paramètre pour NCG

        # Requête initiale avec condition de base NCG LIKE '210%' AND POSDEV > 0
        comptes = Cpt.objects.filter(NCG__startswith='210')

        if client_filter:
            comptes = comptes.filter(CLIENT=client_filter)  # Filtre sur CLIENT
        if compte_filter:
            comptes = comptes.filter(COMPTE=compte_filter)  # Filtre sur COMPTE
        if datouv_filter:
            comptes = comptes.filter(DATOUV=datouv_filter)  # Filtre sur DATOUV
        if datfrm_filter:
            comptes = comptes.filter(DATFRM=datfrm_filter)  # Filtre sur DATFRM
        if agence_filter:
            comptes = comptes.filter(AGENCE=agence_filter)  # Filtre sur AGENCE
        if ncg_filter:
            comptes = comptes.filter(NCG__startswith=ncg_filter)  # Filtre sur NCG (commence par '210%')

        # Pagination des résultats
        paginator = PageNumberPagination()
        paginator.page_size = 9  # Limiter les résultats par page
        paginated_results = paginator.paginate_queryset(comptes, request)

        # Sérialisation des résultats paginés
        serializer = self.serializer_class(paginated_results, many=True)

        # Retourner les résultats paginés avec la réponse JSON
        return paginator.get_paginated_response(serializer.data)



#ouvert
class CompteDatouvNotNullAPIView(APIView):
    serializer_class = CptSerializer

    def get(self, request, *args, **kwargs):
        # Filtrer les comptes où DATOUV n'est pas null
        comptes = Cpt.objects.exclude(DATOUV__isnull=True)

        # Pagination des résultats
        paginator = PageNumberPagination()
        paginator.page_size = 14  # Limiter les résultats par page
        paginated_results = paginator.paginate_queryset(comptes, request)

        # Sérialisation des résultats paginés
        serializer = self.serializer_class(paginated_results, many=True)

        # Retourner les résultats paginés avec la réponse JSON
        return paginator.get_paginated_response(serializer.data)


# ## virement intern
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.pagination import PageNumberPagination
from django.db import connection
from rest_framework import status

class Virement(APIView):
    def get(self, request, *args, **kwargs):
        try:
            # Récupérer les critères de recherche depuis les paramètres de la requête
            start_date = request.GET.get('start_date', None)
            end_date = request.GET.get('end_date', None)
            beneficiaire_filter = request.GET.get('beneficiaire', None)
            compte_benef_filter = request.GET.get('compte_benef', None)
            reference_transaction_filter = request.GET.get('reference_transaction', None)

            # Construction de la requête SQL de base
            query = """
                SELECT A.OPER,
                       A.comptec AS Compte_Benef,
                       TRIM(NOMBE) AS BENEFICIAIRE,
                       A.DATOPER AS DATE_TRANSACTION,
                       c.agence,
                       TRIM(A.DEV1) AS devise,
                       'CD' AS MODE_REGLEMENT,
                       ROUND(A.MNTDEVC, 2) AS MONTANT_TRANSACTION,
                       NVL(NVL((SELECT i.numid FROM aub.titu t, aub.idp i WHERE t.client = c.client AND t.idp = i.idp),
                               (SELECT idm.tin1 FROM aub.titu t, aub.cli m1, aub.idm WHERE t.client = m1.client AND t.client = c.client AND t.idm = idm.idm AND NVL(t.valide, 'N') = 'V')), ' ') AS NIF_NNI,
                       A.COMPTED AS Compte_Don,
                       A.DORDRED AS NOM_DONNEUR_ORDRE,
                       (SELECT nom FROM aub.pays WHERE pays = A.pays) AS PAYS,
                       'PRODUIT' AS produit,
                       A.NOOPER AS REFERENCE_TRANSACTION,
                       A.COURS12 AS TAUX_CHANGE,
                       A.devised AS devisd_debit,
                       A.devisec AS devise_credit,
                       mntdevd AS montant_debit,
                       mntdevc AS montant_credit
                FROM VIREST A
                JOIN cpt c ON A.COMPTED = c.compte
                WHERE A.VALIDE = 'V'
                  AND A.compted = c.compte
                  AND comptec NOT LIKE '011000%'
            """
            
            # Liste des conditions de filtre et des paramètres de requête
            filters = []
            query_params = []

            # Ajouter le filtre de date si nécessaire
            if start_date and end_date:
                filters.append("A.DATOPER BETWEEN %s AND %s")
                query_params.extend([start_date, end_date])

            # Ajouter un filtre pour le bénéficiaire si nécessaire
            if beneficiaire_filter:
                filters.append("TRIM(NOMBE) LIKE %s")
                query_params.append(f"%{beneficiaire_filter}%")

            # Ajouter un filtre pour le compte bénéficiaire si nécessaire
            if compte_benef_filter:
                filters.append("A.comptec LIKE %s")
                query_params.append(f"%{compte_benef_filter}%")

            # Ajouter un filtre pour la référence de transaction si nécessaire
            if reference_transaction_filter:
                filters.append("A.NOOPER LIKE %s")
                query_params.append(f"%{reference_transaction_filter}%")

            # Ajouter les filtres à la requête SQL si nécessaires
            if filters:
                query += " AND " + " AND ".join(filters)

            # Ajouter l'ordre de tri
            query += " ORDER BY A.DATOPER"

            # Exécuter la requête SQL avec les paramètres
            with connection.cursor() as cursor:
                cursor.execute(query, query_params)
                rows = cursor.fetchall()

            # Format des résultats dans une liste de dictionnaires
            result = []
            for row in rows:
                result.append({
                    'oper': row[0],
                    'compte_benef': row[1],
                    'beneficiaire': row[2],
                    'date_transaction': row[3],
                    'agence': row[4],
                    'devise': row[5],
                    'mode_reglement': row[6],
                    'montant_transaction': row[7],
                    'nif_nni': row[8],
                    'compte_don': row[9],
                    'nom_donneur_ordre': row[10],
                    'pays': row[11],
                    'produit': row[12],
                    'reference_transaction': row[13],
                    'taux_change': row[14],
                    'devisd_debit': row[15],
                    'devise_credit': row[16],
                    'montant_debit': row[17],
                    'montant_credit': row[18],
                })

            # Pagination des résultats
            paginator = PageNumberPagination()
            paginator.page_size = 9  # Limiter les résultats par page
            paginated_results = paginator.paginate_queryset(result, request)

            # Retourner les résultats paginés avec la réponse JSON
            return paginator.get_paginated_response(paginated_results)

        except Exception as e:
            # Gestion des erreurs
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

from django.db import connection

class Virement(APIView):
    def get(self, request, *args, **kwargs):
       # agence_filter = request.GET.get('agence', None)
        try:
            # Requête SQL brute
            query = """
                SELECT A.OPER,
                       A.comptec AS Compte_Benef,
                       TRIM(NOMBE) AS BENEFICIAIRE,
                       A.DATOPER AS DATE_TRANSACTION,
                       c.agence,
                       TRIM(A.DEV1) AS devise,
                       'CD' AS MODE_REGLEMENT,
                       ROUND(A.MNTDEVC, 2) AS MONTANT_TRANSACTION,
                       NVL(NVL((SELECT i.numid FROM aub.titu t, aub.idp i WHERE t.client = c.client AND t.idp = i.idp),
                               (SELECT idm.tin1 FROM aub.titu t, aub.cli m1, aub.idm WHERE t.client = m1.client AND t.client = c.client AND t.idm = idm.idm AND NVL(t.valide, 'N') = 'V')), ' ') AS NIF_NNI,
                       A.COMPTED AS Compte_Don,
                       A.DORDRED AS NOM_DONNEUR_ORDRE,
                       (SELECT nom FROM aub.pays WHERE pays = A.pays) AS PAYS,
                       'PRODUIT' AS produit,
                       A.NOOPER AS REFERENCE_TRANSACTION,
                       A.COURS12 AS TAUX_CHANGE,
                       A.devised AS devisd_debit,
                       A.devisec AS devise_credit,
                       mntdevd AS montant_debit,
                       mntdevc AS montant_credit
                FROM VIREST A
                JOIN cpt c ON A.COMPTED = c.compte
                WHERE A.VALIDE = 'V'
                  AND A.compted = c.compte
                  AND comptec NOT LIKE '011000%'
                ORDER BY A.DATOPER
            """

            # Exécuter la requête SQL
            with connection.cursor() as cursor:
                cursor.execute(query)
                rows = cursor.fetchall()

            # Format des résultats dans une liste de dictionnaires
            result = []
            for row in rows:
                result.append({
                    'oper': row[0],
                    'compte_benef': row[1],
                    'beneficiaire': row[2],
                    'date_transaction': row[3],
                    'agence': row[4],
                    'devise': row[5],
                    'mode_reglement': row[6],
                    'montant_transaction': row[7],
                    'nif_nni': row[8],
                    'compte_don': row[9],
                    'nom_donneur_ordre': row[10],
                    'pays': row[11],
                    'produit': row[12],
                    'reference_transaction': row[13],
                    'taux_change': row[14],
                    'devisd_debit': row[15],
                    'devise_credit': row[16],
                    'montant_debit': row[17],
                    'montant_credit': row[18],
                })

            # Pagination des résultats
            paginator = PageNumberPagination()
            paginator.page_size = 9  # Limiter les résultats par page
            paginated_results = paginator.paginate_queryset(result, request)

            # Retourner les résultats paginés avec la réponse JSON
            return paginator.get_paginated_response(paginated_results)

        except Exception as e:
            # Gestion des erreurs
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

##### GUICHET ##########
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.pagination import PageNumberPagination
from rest_framework import status
from django.db import connection

class Guichet(APIView):
    def get(self, request, *args, **kwargs):
        try:
            # Récupérer les critères de recherche depuis les paramètres de la requête
            date_transaction_filter = request.GET.get('date_transaction', None)
            compte_benef_filter = request.GET.get('Compte_benef', None)
            nomlib_filter = request.GET.get('nomlib', None)
            oper_filter = request.GET.get('oper', None)
            agence_filter = request.GET.get('agence', None)

            # Récupérer les dates de début et de fin pour la recherche entre deux dates
            start_date = request.GET.get('start_date', None)
            end_date = request.GET.get('end_date', None)

            # Construction de la requête SQL de base
            query = """
                select 
                       a.oper,
                       f.y1 type_operation,
                       a.datoper date_transaction,
                       a.COMPTED Compte_Don,
                       a.COMPTEC Compte_benef,
                       a.devised devise_debit,
                       a.devisec devise_credit, 
                       a.nomlib,
                       a.mntnetd montant_debeit,
                       a.mntnetc montant_credit,
                       c.agence
                FROM GUICHET a, fx5y8 f,cpt c
                WHERE tname='GUICHET' and trim(a.oper) = trim(f.x1) and a.compted=c.compte and a.VALIDE = 'V'
            """

            # Ajout des filtres dynamiques selon les paramètres
            filters = []

            if date_transaction_filter:
                filters.append(f"a.datoper = '{date_transaction_filter}'")
            if compte_benef_filter:
                filters.append(f"a.COMPTEC = '{compte_benef_filter}'")
            if oper_filter:
                filters.append(f"a.oper = '{oper_filter}'")
            if agence_filter:
                filters.append(f"c.agence = '{agence_filter}'")
            if nomlib_filter:
                filters.append(f"a.nomlib LIKE '%{nomlib_filter}%'")

            # Filtrage par plage de dates (start_date et end_date)
            if start_date and end_date:
                filters.append(f"a.datoper BETWEEN '{start_date}' AND '{end_date}'")
            elif start_date:
                filters.append(f"a.datoper >= '{start_date}'")
            elif end_date:
                filters.append(f"a.datoper <= '{end_date}'")

            # Ajouter les filtres à la requête SQL
            if filters:
                query += " AND " + " AND ".join(filters)

            # Exécuter la requête SQL
            with connection.cursor() as cursor:
                cursor.execute(query)
                rows = cursor.fetchall()

            # Format des résultats dans une liste de dictionnaires
            result = []
            for row in rows:
                result.append({
                    'oper': row[0],
                    'type_operation': row[1],
                    'date_transaction': row[2],
                    'Compte_Don': row[3],
                    'Compte_benef': row[4],
                    'devise_debit': row[5],
                    'devise_credit': row[6],
                    'nomlib': row[7],
                    'montant_debit': row[8],
                    'montant_credit': row[9],
                    'agence': row[10]
                })

            # Pagination des résultats
            paginator = PageNumberPagination()
            paginator.page_size = 14  # Limiter les résultats par page
            paginated_results = paginator.paginate_queryset(result, request)

            # Retourner les résultats paginés avec la réponse JSON
            return paginator.get_paginated_response(paginated_results)

        except Exception as e:
            # Gestion des erreurs
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class Guichet1(APIView):
    def get(self, request, *args, **kwargs):
        try:
            # Récupérer les critères de recherche depuis les paramètres de la requête
            date_transaction_filter = request.GET.get('date_transaction', None)
            compte_benef_filter = request.GET.get('Compte_benef', None)
            nomlib_filter = request.GET.get('nomlib', None)
            oper_filter = request.GET.get('oper', None)
            
            # Récupérer les dates de début et de fin pour la recherche entre deux dates
            start_date = request.GET.get('start_date', None)
            agence_filter = request.GET.get('agence', None)

            # Construction de la requête SQL de base
            query = """
                select 
                       a.oper,
                       f.y1 type_operation,
                       a.datoper date_transaction,
                       a.COMPTED Compte_Don,
                       a.COMPTEC Compte_benef,
                       a.devised devise_debit,
                       a.devisec devise_credit, 
                       a.nomlib,
                       a.mntnetd montant_debeit,
                       a.mntnetc montant_credit,
                       c.agence
                FROM GUICHET a, fx5y8 f,cpt c
                WHERE tname='GUICHET' and trim(a.oper) = trim(f.x1) and a.compted=c.compte and a.VALIDE = 'V'
            """
            # Ajout des filtres dynamiques selon les paramètres
            filters = []
            if date_transaction_filter:
                filters.append(f"a.datoper = '{date_transaction_filter}'")
            if compte_benef_filter:
                filters.append(f"a.COMPTEC = '{compte_benef_filter}'")
            if oper_filter:
                filters.append(f"a.oper = '{oper_filter}'")
            if agence_filter:
                filters.append(f"c.agence= '{agence_filter}'")
            if nomlib_filter:
                filters.append(f"a.nomlib LIKE '%{nomlib_filter}%'")
            
            # Filtrage par plage de dates (start_date et end_date)
            if start_date and end_date:
                filters.append(f"a.datoper BETWEEN '{start_date}' AND '{end_date}'")

            # Ajouter les filtres à la requête SQL
            if filters:
                query += " AND " + " AND ".join(filters)

            # Exécuter la requête SQL
            with connection.cursor() as cursor:
                cursor.execute(query)
                rows = cursor.fetchall()

            # Format des résultats dans une liste de dictionnaires
            result = []
            for row in rows:
                result.append({
                    'oper': row[0],
                    'type_operation': row[1],
                    'date_transaction': row[2],
                    'Compte_Don': row[3],
                    'Compte_benef': row[4],
                    'devise_debit': row[5],
                    'devise_credit': row[6],
                    'nomlib': row[7],
                    'montant_debeit': row[8],
                    'montant_credit': row[9],
                    'agence': row[10]
                })

            # Pagination des résultats
            paginator = PageNumberPagination()
            paginator.page_size = 14  # Limiter les résultats par page
            paginated_results = paginator.paginate_queryset(result, request)

            # Retourner les résultats paginés avec la réponse JSON
            return paginator.get_paginated_response(paginated_results)

        except Exception as e:
            # Gestion des erreurs
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

### parc guichet ####
class OperatioGuichetView(APIView):
    def get(self, request, *args, **kwargs):
        try:
            # Définir la requête SQL
            query = """
                SELECT 
                    f.y1 type_operation,
                    COUNT(*) AS Nombre
                FROM GUICHET a, fx5y8 f
                WHERE tname='GUICHET' and MODEL='OPERLIB' and trim(a.oper) = trim(f.x1) and a.VALIDE = 'V'
                GROUP BY 
                    f.y1
                ORDER BY 
                    f.y1
            """
            
            # Exécuter la requête SQL
            with connection.cursor() as cursor:
                cursor.execute(query)
                rows = cursor.fetchall()

            # Format des résultats dans une liste de dictionnaires
            results = [
                {'type_operation': row[0], 'Nombre': row[1]} for row in rows
            ]

            # Retourner les résultats en JSON
            return Response(results, status=status.HTTP_200_OK)

        except Exception as e:
            # Gérer les erreurs
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

### COMPTE DETAILS ######
class DtailsCompte(APIView):
    def get(self, request, *args, **kwargs):
        try:
            agent_economique_filter = request.GET.get('agent_economique', None)
            # Récupérer les dates de début et de fin pour la recherche entre deux dates
            start_date = request.GET.get('start_date', None)
            end_date = request.GET.get('end_date', None)

            # Construction de la requête SQL de base
            query = """
                select 
                       c.client,
                       c.nom,
                       p.agec,
                       p.ageclib,
                       ng.libelle,
                       t.compte,
                       t.devise 
                from cli c,agec p,cpt t,ncglib ng  
                where c.agec = p.agec and c.client = t.client and ng.ncg = t.ncg and t.ncg like '210%' 
                order by ng.libelle
            """
            # Ajout des filtres dynamiques selon les paramètres
            filters = []
            if agent_economique_filter:
                filters.append(f"ng.libelle = '{agent_economique_filter}'")

            # Exécuter la requête SQL
            with connection.cursor() as cursor:
                cursor.execute(query)
                rows = cursor.fetchall()

            # Format des résultats dans une liste de dictionnaires
            result = []
            for row in rows:
                result.append({
                    'client': row[0],
                    'nom': row[1],
                    'type_agent': row[2],
                    'agent_economique': row[3],
                    'produit': row[4],
                    'compte': row[5],
                    'devise': row[6],
                })

            # Pagination des résultats
            paginator = PageNumberPagination()
            paginator.page_size = 14  # Limiter les résultats par page
            paginated_results = paginator.paginate_queryset(result, request)

            # Retourner les résultats paginés avec la réponse JSON
            return paginator.get_paginated_response(paginated_results)

        except Exception as e:
            # Gestion des erreurs
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)



### COMPTE DEPOSITE ######
from django.db.models import Sum
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.pagination import PageNumberPagination

class CompteDeposite(APIView):
    serializer_class = CptSerializer

    def get(self, request, *args, **kwargs):
        # Récupérer les critères de recherche depuis les paramètres de la requête
        client_filter = request.GET.get('CLIENT', None)
        compte_filter = request.GET.get('COMPTE', None)
        datouv_filter = request.GET.get('DATOUV', None)
        datfrm_filter = request.GET.get('DATFRM', None)
        agence_filter = request.GET.get('AGENCE', None)

        # Requête initiale avec condition de base NCG LIKE '210%' AND POSDEV > 0
        comptes = Cpt.objects.filter(NCG__startswith='210', POSDEV__gt=0)

        # Appliquer les autres filtres dynamiquement
        if client_filter:
            comptes = comptes.filter(CLIENT=client_filter)
        if compte_filter:
            comptes = comptes.filter(COMPTE=compte_filter)
        if datouv_filter:
            comptes = comptes.filter(DATOUV=datouv_filter)
        if datfrm_filter:
            comptes = comptes.filter(DATFRM=datfrm_filter)
        if agence_filter:
            comptes = comptes.filter(AGENCE=agence_filter)

        # Calculer la somme totale de POSDEV pour les comptes filtrés
        total_posdev = comptes.aggregate(total=Sum('POSDEV'))['total'] or 0

        # Pagination des résultats
        paginator = PageNumberPagination()
        paginator.page_size = 14
        paginated_results = paginator.paginate_queryset(comptes, request)

        # Sérialisation des résultats paginés
        serializer = self.serializer_class(paginated_results, many=True)

        # Ajouter la somme totale de POSDEV à la réponse
        return Response({
            'count': paginator.page.paginator.count,
            'next': paginator.get_next_link(),
            'previous': paginator.get_previous_link(),
            'total_posdev': total_posdev,  # Ajout de la somme totale
            'results': serializer.data
        })


from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.pagination import PageNumberPagination
from django.db import connection
from rest_framework import status

class Client(APIView):
    def get(self, request, *args, **kwargs):
        try:
            # Récupérer les critères de recherche depuis les paramètres de la requête
            date_transaction_filter = request.GET.get('date_transaction', None)
            client_filter = request.GET.get('client', None)
            agence_filter = request.GET.get('agence', None)
            nom_filter = request.GET.get('nom', None)
            type_filter = request.GET.get('type', None)

            # Récupérer les dates de début et de fin pour la recherche entre deux dates
            start_date = request.GET.get('start_date', None)
            end_date = request.GET.get('end_date', None)

            # Construction de la requête SQL de base
            query = """
                SELECT 
                   DISTINCT l.CLIENT,
                    l.NOM,
                    l.DATOUV,
                    l.DATFRM,
                    l.AGENCE,
                    ag.ageclib
                FROM cli l, cpt p, ncglib ng, agec ag
                WHERE l.CLIENT = p.CLIENT 
                AND ng.ncg = p.ncg 
                AND l.agec = ag.agec
                AND l.datfrm IS NULL 
                AND p.ncg LIKE %s
            """

            # Ajout des filtres dynamiques selon les paramètres
            filters = []
            if date_transaction_filter:
                filters.append(f"l.DATOUV = %s")
            if client_filter:
                filters.append(f"l.CLIENT = %s")
            if agence_filter:
                filters.append(f"l.AGENCE = %s")
            if nom_filter:
                filters.append(f"l.NOM LIKE %s")
            if type_filter:
                filters.append(f"ag.ageclib = %s")
            # Filtrage par plage de dates (start_date et end_date)
            if start_date and end_date:
                filters.append(f"l.DATOUV BETWEEN %s AND %s")

            # Ajouter les filtres à la requête SQL
            if filters:
                query += " AND " + " AND ".join(filters)

            # Préparer les paramètres pour exécuter la requête
            query_params = ['210%']
            if date_transaction_filter:
                query_params.append(date_transaction_filter)
            if client_filter:
                query_params.append(client_filter)
            if agence_filter:
                query_params.append(agence_filter)
            if nom_filter:
                query_params.append(f"%{nom_filter}%")  # On met le nom dans un format LIKE
            if type_filter:
                query_params.append(type_filter)
            if start_date and end_date:
                query_params.extend([start_date, end_date])

            # Exécuter la requête SQL avec les paramètres
            with connection.cursor() as cursor:
                cursor.execute(query, query_params)
                rows = cursor.fetchall()

            # Format des résultats dans une liste de dictionnaires
            result = []
            for row in rows:
                result.append({
                    'CLIENT': row[0],
                    'NOM': row[1],
                    'DATOUV': row[2],
                    'DATFRM': row[3],
                    'AGENCE': row[4],
                    'TYPE': row[5],
                })

            # Pagination des résultats
            paginator = PageNumberPagination()
            paginator.page_size = 14  # Limiter les résultats par page
            paginated_results = paginator.paginate_queryset(result, request)

            # Retourner les résultats paginés avec la réponse JSON
            return paginator.get_paginated_response(paginated_results)

        except Exception as e:
            # Gestion des erreurs
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


####---- virement intern ######
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.pagination import PageNumberPagination
from django.db import connection
from rest_framework import status

class VirementIntern(APIView):
    def get(self, request, *args, **kwargs):
        try:
            # Récupérer les critères de recherche depuis les paramètres de la requête
            date_operation_filter = request.GET.get('date_operation', None)
            client_filter = request.GET.get('client', None)
            state_filter = request.GET.get('state', None)
            agence_filter = request.GET.get('agence', None)
            
            # Récupérer les dates de début et de fin pour la recherche entre deux dates
            start_date = request.GET.get('start_date', None)
            end_date = request.GET.get('end_date', None)

            # Construction de la requête SQL de base
            query = """
                SELECT v.datoper,
                       v.mntdevd,
                       v.mntdevc,
                       c.client ,
                       c.agence,
                       v.compted,
                       v.comptec, 
                       v.state
                FROM virint v
                JOIN cpt c ON c.compte = v.compted
            """

            # Liste des conditions de filtre
            filters = []
            query_params = []

            if date_operation_filter:
                filters.append("v.datoper = %s")
                query_params.append(date_operation_filter)
            if client_filter:
                filters.append("c.client = %s")
                query_params.append(client_filter)
            if state_filter:
                filters.append("v.state = %s")
                query_params.append(state_filter)
            if agence_filter:
                filters.append("c.agence = %s")  # Use c.agence if the column is in cpt
                query_params.append(agence_filter)
            if start_date and end_date:
                filters.append("v.datoper BETWEEN %s AND %s")
                query_params.extend([start_date, end_date])

            # Ajouter les filtres à la requête SQL si nécessaires
            if filters:
                query += " WHERE " + " AND ".join(filters)

            # Exécuter la requête SQL avec les paramètres
            with connection.cursor() as cursor:
                cursor.execute(query, query_params)
                rows = cursor.fetchall()

            # Format des résultats dans une liste de dictionnaires
            result = []
            for row in rows:
                result.append({
                    'date_operation': row[0],
                    'montant_debit': row[1],
                    'montant_credit': row[2],
                    'client': row[3],
                    'agence': row[4],
                    'compte_debit': row[5],
                    'compte_credit': row[6],
                    'status': row[7]
                })

            # Pagination des résultats
            paginator = PageNumberPagination()
            paginator.page_size = 9  # Limiter les résultats par page
            paginated_results = paginator.paginate_queryset(result, request)

            # Retourner les résultats paginés avec la réponse JSON
            return paginator.get_paginated_response(paginated_results)

        except Exception as e:
            # Gestion des erreurs
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


#####---- parque compte 
from django.db import connection
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status


class LibelleCountView(APIView):
    def get(self, request, *args, **kwargs):
        try:
            # Définir la requête SQL
            query = """
                SELECT 
                    ng.libelle,
                    COUNT(*) AS count
                FROM cli c, agec p, cpt t, ncglib ng
                WHERE 
                    c.agec = p.agec
                    AND c.client = t.client
                    AND ng.ncg = t.ncg
                    AND t.ncg LIKE '210%'
                    AND t.datfrm IS NULL
                GROUP BY ng.libelle
                ORDER BY ng.libelle
            """
            # Exécuter la requête SQL
            with connection.cursor() as cursor:
                cursor.execute(query)
                rows = cursor.fetchall()

            # Format des résultats dans une liste de dictionnaires
            results = [{'libelle': row[0], 'count': row[1]} for row in rows]

            # Retourner les résultats en JSON
            return Response(results, status=status.HTTP_200_OK)

        except Exception as e:
            # Gérer les erreurs
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

#####detaile compte 
from django.db import connection
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status


class CompteDetailsView(APIView):
    def get(self, request, *args, **kwargs):
        try:
            agent_economique_filter = request.GET.get('agent_economique', None)
            # Définir la requête SQL
            query = """
                SELECT 
                    c.client,
                    c.nom,
                    p.agec,
                    p.ageclib,
                    ng.libelle,
                    t.compte,
                    t.devise
                FROM 
                    cli c, agec p, cpt t, ncglib ng
                WHERE 
                    c.agec = p.agec 
                    AND c.client = t.client 
                    AND ng.ncg = t.ncg 
                    AND t.ncg LIKE '210%'
                ORDER BY 
                    ng.libelle
            """
                        # Ajout des filtres dynamiques selon les paramètres
            filters = []

            if agent_economique_filter:
                filters.append(f"ng.libelle = %s")

            # Préparer les paramètres pour exécuter la requête
            query_params = []
            if agent_economique_filter:
                query_params.append(agent_economique_filter)

            # Exécuter la requête SQL
            with connection.cursor() as cursor:
                cursor.execute(query)
                rows = cursor.fetchall()

            # Format des résultats dans une liste de dictionnaires
            results = [
                {
                    'client': row[0],
                    'nom': row[1],
                    'agec': row[2],
                    'ageclib': row[3],
                    'libelle': row[4],
                    'compte': row[5],
                    'devise': row[6]
                } for row in rows
            ]

            # Retourner les résultats en JSON
            return Response(results, status=status.HTTP_200_OK)

        except Exception as e:
            # Gérer les erreurs
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


#####-----parque depot ------###
from django.db import connection
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status


class ProduitDepotView(APIView):
    def get(self, request, *args, **kwargs):
        try:
            # Définir la requête SQL
            query = """
                SELECT 
                    ng.libelle AS Produit,
                    COUNT(*) AS Nombre,
                    SUM(t.posdev) AS Depot
                FROM 
                    cli c, agec p, cpt t, ncglib ng
                WHERE 
                    c.agec = p.agec 
                    AND c.client = t.client 
                    AND ng.ncg = t.ncg 
                    AND t.ncg LIKE '210%' 
                    AND t.datfrm IS NULL 
                    AND t.posdev > 0
                GROUP BY 
                    ng.libelle
                ORDER BY 
                    ng.libelle
            """
            
            # Exécuter la requête SQL
            with connection.cursor() as cursor:
                cursor.execute(query)
                rows = cursor.fetchall()

            # Format des résultats dans une liste de dictionnaires
            results = [
                {'Produit': row[0], 'Nombre': row[1], 'Depot': row[2]} for row in rows
            ]

            # Retourner les résultats en JSON
            return Response(results, status=status.HTTP_200_OK)

        except Exception as e:
            # Gérer les erreurs
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


####----depot details -----####
from django.db import connection
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status


class ClientComptePosdevView(APIView):
    def get(self, request, *args, **kwargs):
        try:
            # Requête SQL
            query = """
                SELECT 
                    c.client,
                    c.nom,
                    p.agec,
                    p.ageclib,
                    ng.libelle,
                    t.compte,
                    t.devise,
                    t.posdev
                FROM 
                    cli c, agec p, cpt t, ncglib ng
                WHERE 
                    c.agec = p.agec 
                    AND c.client = t.client 
                    AND ng.ncg = t.ncg 
                    AND t.ncg LIKE '210%' 
                    AND t.posdev > 0
                ORDER BY 
                    ng.libelle
            """
            
            # Exécuter la requête SQL
            with connection.cursor() as cursor:
                cursor.execute(query)
                rows = cursor.fetchall()

            # Convertir les résultats en dictionnaires
            results = [
                {
                    'client': row[0],
                    'nom': row[1],
                    'agec': row[2],
                    'ageclib': row[3],
                    'libelle': row[4],
                    'compte': row[5],
                    'devise': row[6],
                    'posdev': row[7]
                }
                for row in rows
            ]

            # Retourner les résultats au format JSON
            return Response(results, status=status.HTTP_200_OK)

        except Exception as e:
            # Gestion des erreurs
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)




#### parque client 

from rest_framework.views import APIView
from rest_framework.response import Response
from django.db import connection

class ClientDataAPIView1(APIView):
    def get(self, request):
        with connection.cursor() as cursor:
            query = """
                SELECT p.ageclib, c.agence ,COUNT(*)
                FROM cli c
                INNER JOIN agec p ON c.agec = p.agec
                INNER JOIN cpt t ON c.client = t.client
                WHERE t.ncg LIKE '210%' AND c.datfrm IS NULL
                GROUP BY p.ageclib ,c.agence
            """
            cursor.execute(query)
            results = cursor.fetchall()

        # Structurer les données pour la réponse JSON
        data = [{"ageclib": row[0], "agence": row[1], "count": row[2]} for row in results]

        return Response(data)


from rest_framework.views import APIView
from rest_framework.response import Response
from django.db import connection

class ClientDataAPIView(APIView):
    def get(self, request):
        # Récupérer le paramètre de requête 'agence' s'il existe
        agence_filter = request.query_params.get('agence', None)

        with connection.cursor() as cursor:
            query = """
                SELECT p.ageclib, c.agence, COUNT(*)
                FROM cli c
                INNER JOIN agec p ON c.agec = p.agec
                INNER JOIN cpt t ON c.client = t.client
                WHERE t.ncg LIKE '210%' AND c.datfrm IS NULL
            """
            
            # Ajouter le filtre sur l'agence si le paramètre est présent
            if agence_filter:
                query += " AND c.agence = %s"
            
            # Ajouter la clause GROUP BY
            query += " GROUP BY p.ageclib, c.agence"

            # Exécuter la requête
            if agence_filter:
                cursor.execute(query, [agence_filter])
            else:
                cursor.execute(query)

            results = cursor.fetchall()

        # Structurer les données pour la réponse JSON
        data = [{"ageclib": row[0], "agence": row[1], "count": row[2]} for row in results]

        return Response(data)
