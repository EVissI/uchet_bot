import click
from werkzeug.security import generate_password_hash
from app.db.database import sync_session
from app.db.models import AdminUser

@click.group()
def cli():
    """Management commands for uchet_bot"""
    pass

@cli.command('create-admin')
@click.argument('username')
@click.password_option()
def create_admin(username, password):
    """Create a new admin user."""
    with sync_session() as session:
        user = AdminUser(
            username=username,
            password=generate_password_hash(password)
        )
        session.add(user)
        session.commit()
    click.echo(f'Created admin user: {username}')

if __name__ == '__main__':
    cli()