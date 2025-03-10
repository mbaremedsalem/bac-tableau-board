import re
from django.db import connections
from django.http import HttpRequest

class SwitchDatabaseMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request: HttpRequest):
        # Récupérer le chemin de l'URL de la demande
        path = request.path

        # Déterminer quelle base de données utiliser en fonction de l'endpoint demandé
        if path in ['/api/token/', '/api/register/', '/api/me/','/api/forget_password/', '/api/reset_password/<str:token>'] or \
           path.startswith('/api/reset_password/') or \
           path.startswith('/admin/') or \
           re.match(r'^/api/forget_password/[^/]+/$', path) or \
           re.match(r'^/api/reset_password/[^/]+/$', path):
            # Utiliser la base de données SQLite par défaut pour ces endpoints
            using_db = 'sqlite'
        else:
            # Utiliser la base de données Oracle par défaut pour les autres endpoints
            using_db = 'oracle'

        # Modifier la base de données par défaut en fonction de la configuration
        connections['default'].close()  # Fermer la connexion existante
        connections['default'] = connections[using_db]  # Modifier la base de données par défaut
        connections['default'].ensure_connection()  # Réouvrir la connexion

        return self.get_response(request)