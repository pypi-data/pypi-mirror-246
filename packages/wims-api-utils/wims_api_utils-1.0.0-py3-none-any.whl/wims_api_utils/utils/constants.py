"""All constants for project."""
import os

from dotenv import find_dotenv, load_dotenv

# this will load all the envars from a .env file located in the project root (api)
load_dotenv(find_dotenv())

WIMS_API_CORS_ORIGINS = os.getenv("WIMS_API_CORS_ORIGINS", "*")
ALLOW_ALL_ORIGINS = "*"
CORS_ORIGINS = []
if WIMS_API_CORS_ORIGINS != "*":
    CORS_ORIGINS = WIMS_API_CORS_ORIGINS.split(",")
ADMIN_GROUP = "wims-admin"
DESIGNER_GROUP = "wims-designer"
REVIEWER_GROUP = "wims-reviewer"
CLIENT_GROUP = "wims-client"
WIMS_ROLES = [DESIGNER_GROUP, REVIEWER_GROUP, CLIENT_GROUP]
ALLOW_ALL_APPLICATIONS = "/wims/wims-reviewer/access-allow-applications"

NEW_APPLICATION_STATUS = "New"
DRAFT_APPLICATION_STATUS = "Draft"
KEYCLOAK_DASHBOARD_BASE_GROUP = "wims-analytics"
ANONYMOUS_USER = "Anonymous-user"

FILTER_MAPS = {
    "application_id": {"field": "id", "operator": "eq"},
    "application_name": {"field": "form_name", "operator": "ilike"},
    "application_status": {"field": "application_status", "operator": "eq"},
    "created_by": {"field": "created_by", "operator": "eq"},
    "modified_from": {"field": "modified", "operator": "ge"},
    "modified_to": {"field": "modified", "operator": "le"},
    "created_from": {"field": "created", "operator": "ge"},
    "created_to": {"field": "created", "operator": "le"},
    "form_name": {"field": "form_name", "operator": "ilike"},
    "id": {"field": "id", "operator": "eq"},
    "form_type": {"field": "form_type", "operator": "eq"},
    "can_bundle": {"field": "can_bundle", "operator": "eq"},
    "is_bundle": {"field": "is_bundle", "operator": "eq"},
    "title":{"field": "title", "operator": "ilike"},
    "category":{"field": "category", "operator": "ilike"},
}

DEFAULT_PROCESS_KEY = "Defaultflow"
DEFAULT_PROCESS_NAME = "Default Flow"
HTTP_TIMEOUT = 30
