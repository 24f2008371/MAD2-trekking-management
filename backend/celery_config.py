from celery import Celery

celery_app = Celery(
    'app',
    broker='redis://127.0.0.1:6379/0',
    backend='redis://127.0.0.1:6379/0'
)
celery_app.conf.update(
    broker_url='redis://127.0.0.1:6379/0',
    result_backend='redis://127.0.0.1:6379/0',
    timezone='UTC'
)

def make_celery(app):
    celery_app.conf.update(
        broker_url=app.config['broker_url'],
        result_backend=app.config['result_backend'],
    )

    class ContextTask(celery_app.Task):
        def __call__(self, *args, **kwargs):
            with app.app_context():
                return self.run(*args, **kwargs)

    celery_app.Task = ContextTask
    return celery_app
