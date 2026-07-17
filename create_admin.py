"""One-off CLI to create the first admin account.

Usage:
    python create_admin.py <username> <password>
"""
import sys

from app import create_app
from app.extensions import db
from app.models import Admin


def main():
    if len(sys.argv) != 3:
        print("Usage: python create_admin.py <username> <password>")
        sys.exit(1)

    username, password = sys.argv[1], sys.argv[2]
    if len(password) < 6:
        print("Password must be at least 6 characters.")
        sys.exit(1)

    app = create_app()
    with app.app_context():
        if Admin.query.filter_by(username=username).first():
            print(f'An admin named "{username}" already exists.')
            sys.exit(1)

        admin = Admin(username=username)
        admin.set_password(password)
        db.session.add(admin)
        db.session.commit()
        print(f'Admin account "{username}" created successfully.')


if __name__ == "__main__":
    main()
