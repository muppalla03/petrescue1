import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'petrescue.settings')
django.setup()

from django.contrib.auth import get_user_model

User = get_user_model()

print("\n" + "="*70)
print("ALL USERS IN DATABASE")
print("="*70)

users = User.objects.all().values('email', 'first_name', 'last_name', 'is_trusted', 'email_verified')

for user in users:
    print(f"\nEmail: {user['email']}")
    print(f"  First Name: {user['first_name']}")
    print(f"  Last Name: {user['last_name']}")
    print(f"  Is Trusted: {user['is_trusted']}")
    print(f"  Email Verified: {user['email_verified']}")

print("\n" + "="*70)
print(f"TOTAL USERS: {len(list(users))}")
print("="*70 + "\n")
