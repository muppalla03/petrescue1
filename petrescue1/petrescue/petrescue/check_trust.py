from django.contrib.auth import get_user_model
from accounts.utils import check_trusted_user_criteria

User = get_user_model()
user = User.objects.first()

print("\n" + "="*70)
print(f"ALL CRITERIA STATUS FOR: {user.email}")
print("="*70 + "\n")

criteria = check_trusted_user_criteria(user)

for k, v in criteria.items():
    symbol = "✅" if v['met'] else "❌"
    print(f"{symbol} {v['name']}")
    print(f"   ➜ {v['details']}")
    print()

# Trust score
score = user.calculate_trust_score()
print("="*70)
print(f"TRUST SCORE: {score}/100")
print(f"IS TRUSTED: {user.is_trusted}")
print("="*70 + "\n")
