import os
from django.http import JsonResponse
from django.db import connection

def version(request):
    """Return deployed version from VERSION file"""
    version_file = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))), '..', 'VERSION')
    try:
        with open(version_file) as f:
            ver = f.read().strip()
    except FileNotFoundError:
        ver = 'unknown'
    return JsonResponse({"version": ver})

def healthz(request):
    """Basic liveness check - process is running"""
    return JsonResponse({"status": "ok"}, status=200)

def readyz(request):
    """Readiness check - DB connection + critical services"""
    try:
        # Check database connection
        with connection.cursor() as cursor:
            cursor.execute("SELECT 1")

        return JsonResponse({
            "status": "ready",
            "database": "connected"
        }, status=200)
    except Exception as e:
        return JsonResponse({
            "status": "not ready",
            "error": str(e)
        }, status=503)
