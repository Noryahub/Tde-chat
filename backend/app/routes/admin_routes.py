from flask import Blueprint, jsonify

from backend.app.services.analytics_service import AnalyticsService

admin_bp = Blueprint(
    "admin",
    __name__,
    url_prefix="/api/admin"
)
@admin_bp.get("/dashboard")
def dashboard_analytics():

    data = (
        AnalyticsService
        .get_dashboard_analytics()
    )

    return jsonify({
        "status": "success",
        "data": data
    })
@admin_bp.get("/signalements")
def latest_signalements():

    data = (
        AnalyticsService
        .get_latest_signalements()
    )

    return jsonify({
        "status": "success",
        "data": data
    })