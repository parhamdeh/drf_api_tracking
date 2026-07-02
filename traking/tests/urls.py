from django.urls import path, include
from . import views as test_view


urlpatterns = [
    path(route="no-logging/", view=test_view.MockWithoutMixinAPIView.as_view()),
    path(route="logging/", view=test_view.MockWithMixinAPIView.as_view()),
    path(route="explicit-logging/", view=test_view.MockExplicitLoggingView.as_view()),
    path(route="custom-check-logging/", view=test_view.MockCustomCheckLoggingView.as_view()),
    path(route="session-auth-logging/", view=test_view.MockSessionAuthLoggingView.as_view()),
    path(route="token-auth-logging/", view=test_view.MockTokenAuthLoggingView.as_view()),
    path(route="sensitive-fields-logging/", view=test_view.MockSensitiveFieldsLoggingView.as_view()),
    path(route="invalid-cleaned-subsstitute-logging/", view=test_view.MockInvalidCleanedSubstituteLoggingView.as_view()),
]   