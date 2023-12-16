import sentry_sdk

from trail import libconfig
from trail.trail import Trail  # noqa

if not libconfig.is_development_environment():
    sentry_sdk.init(
        dsn="https://544746f4656c155d47e2745c0a13a28b@o4506219332304896.ingest.sentry.io/4506219404197888",  # noqa
        # Set traces_sample_rate to 1.0 to capture 100% of transactions for performance monitoring.
        traces_sample_rate=1.0,
        # Set profiles_sample_rate to 1.0 to profile 100% of sampled transactions.
        # We recommend adjusting this value in production.
        profiles_sample_rate=1.0,
    )
