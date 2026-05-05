# Trusted User Feature - Implementation Guide

## Step 1: Apply Database Migration

Run these commands in terminal:

```bash
# Navigate to project directory
cd project_path

# Create fresh migrations
python manage.py makemigrations accounts

# Apply migrations to database
python manage.py migrate accounts
```

**Expected Output:**
```
Running migrations:
  Applying accounts.0004_trusted_user_feature... OK
```

---

## Step 2: Start Server

```bash
python manage.py runserver
```

Go to: `http://127.0.0.1:8000/admin/`

---

## Step 3: Implement All 5 Criteria

### **CRITERION 1: Manual Admin Approval** ✅ (Ready Now)

**How to use in Admin:**

1. Go to **Admin → Users**
2. Select one or more users
3. Scroll to "Trusted User Status" section
4. Click "✓ Approve selected users as Trusted"
5. System records: WHO approved, WHEN, WHY (optional reason)

**To verify this works:**
```bash
python manage.py shell
```

```python
from django.contrib.auth import get_user_model
User = get_user_model()

user = User.objects.first()
print(f"Is Trusted: {user.is_trusted}")
print(f"Approved by: {user.is_trusted_approved_by}")
print(f"Approved at: {user.is_trusted_approved_at}")
```

---

### **CRITERION 2: Proven History** ✅ (Ready - Tracks Automatically)

**What it counts:**
- Successful pet adoptions (adoption_requests with status='approved')
- Successful pet listings (pets with is_approved=True)
- Minimum: 3+ combined

**To test this:**

```bash
python manage.py shell
```

```python
from django.contrib.auth import get_user_model
User = get_user_model()

user = User.objects.first()

# Check successful adoptions
adoptions = user.get_successful_adoptions_count()
print(f"Successful Adoptions: {adoptions}")

# Check successful listings
listings = user.get_successful_listings_count()
print(f"Successful Pet Listings: {listings}")

# Check criteria
print(f"Criterion 2 Met: {(adoptions + listings) >= 3}")
```

**To activate:**
Create adoption requests and pet listings, then approve them in admin. The system automatically counts.

---

### **CRITERION 3: Account Age + Profile Complete** ✅ (Ready - Auto-checks)

**Requirements:**
- Account age: 60+ days
- Profile complete: First name + Last name + Email verified + Address filled

**To test:**

```bash
python manage.py shell
```

```python
from django.contrib.auth import get_user_model
User = get_user_model()

user = User.objects.first()

# Check account age
age_ok = user.is_account_old_enough(60)
print(f"Account 60+ days old: {age_ok}")

# Check profile
profile_ok = user.is_profile_complete()
print(f"Profile complete: {profile_ok}")

# Check criterion
print(f"Criterion 3 Met: {age_ok and profile_ok}")
```

**To activate:**

1. Edit user in Admin → Users
2. Fill in:
   - First name
   - Last name
   - Address (in "Contact Information" section)
3. Check "Email verified" in "Verification Status" section
4. Save

For account age: Wait 60 days OR manually set date_joined in database.

---

### **CRITERION 4: Verification Signals** ✅ (Ready to Mark)

**What needs verification:**
- ☐ Email verified
- ☐ Phone verified
- ☐ Address verified
- ☐ Government ID verified

**Minimum: 2+ verified**

**To activate in Admin:**

1. Go to **Admin → Users**
2. Select a user
3. Scroll to "Verification Status" section
4. Check any of:
   - ☑ email_verified
   - ☑ phone_verified
   - ☑ address_verified
   - ☑ government_id_verified
5. Click Save

**Or use code:**

```bash
python manage.py shell
```

```python
from django.contrib.auth import get_user_model
from accounts.utils import verify_user_email, verify_user_phone, verify_user_address, verify_user_government_id

User = get_user_model()
user = User.objects.first()

# Mark as verified
verify_user_email(user)
verify_user_phone(user)
verify_user_address(user)
verify_user_government_id(user)

# User gets email notification for each
```

**To check:**

```bash
python manage.py shell
```

```python
from django.contrib.auth import get_user_model
User = get_user_model()

user = User.objects.first()
verifications = sum([
    user.email_verified,
    user.phone_verified,
    user.address_verified,
    user.government_id_verified
])

print(f"Total verifications: {verifications}/4")
print(f"Criterion 4 Met: {verifications >= 2}")
```

---

### **CRITERION 5: Community Reputation** ✅ (Ready to Add Reviews)

**What it needs:**
- User reviews/ratings (1-5 stars)
- Average rating: 4.0+ for criterion

**To add reviews in Admin:**

1. Go to **Admin → User Reviews** (new section)
2. Click "Add User Review"
3. Fill in:
   - **Reviewed User**: Select the user being reviewed
   - **Reviewer**: Select the user giving review
   - **Rating**: Choose 1-5 stars
   - **Comment**: Optional feedback
4. Click Save

**Or use code:**

```bash
python manage.py shell
```

```python
from django.contrib.auth import get_user_model
from accounts.models import UserReview

User = get_user_model()
reviewed_user = User.objects.first()
reviewer = User.objects.last()

# Create review
review = UserReview.objects.create(
    reviewed_user=reviewed_user,
    reviewer=reviewer,
    rating=5,
    comment="Excellent user! Very trustworthy."
)

# Check average rating
avg_rating = reviewed_user.get_average_rating()
print(f"Average Rating: {avg_rating}")
print(f"Criterion 5 Met: {avg_rating >= 4.0}")
```

---

## Step 4: Check Trust Score & Criteria Status

```bash
python manage.py shell
```

```python
from django.contrib.auth import get_user_model
from accounts.utils import check_trusted_user_criteria

User = get_user_model()
user = User.objects.first()

# Get detailed criteria status
criteria = check_trusted_user_criteria(user)

print("=" * 60)
print(f"TRUST STATUS FOR: {user.email}")
print("=" * 60)

for key, criterion in criteria.items():
    status = "✅ MET" if criterion['met'] else "❌ NOT MET"
    print(f"\n{criterion['name']}: {status}")
    print(f"Details: {criterion['details']}")

# Trust score
print("\n" + "=" * 60)
trust_score = user.calculate_trust_score()
print(f"TRUST SCORE: {trust_score}/100")
print(f"IS TRUSTED: {user.is_trusted}")
print("=" * 60)
```

---

## Step 5: Admin Actions (Bulk Operations)

### **Approve Users as Trusted:**

1. Go to **Admin → Users**
2. Check boxes next to users you want to approve
3. In "Action" dropdown, select: **"✓ Approve selected users as Trusted"**
4. Click "Go"

### **Revoke Trusted Status:**

1. Go to **Admin → Users**
2. Filter by: **is_trusted = True** (shows only trusted users)
3. Check boxes next to users
4. In "Action" dropdown, select: **"✗ Revoke Trusted status"**
5. Click "Go"

---

## Complete Setup Example

Follow this to get everything working:

### **Setup Test Data:**

```bash
python manage.py shell
```

```python
from django.contrib.auth import get_user_model
from django.utils import timezone
from datetime import timedelta
from pets.models import Pet, AdoptionRequest
from accounts.models import UserReview
from accounts.utils import verify_user_email, verify_user_phone

User = get_user_model()

# Create two test users
print("Creating test users...")
user1, created = User.objects.get_or_create(
    email="john@example.com",
    defaults={
        "first_name": "John",
        "last_name": "Doe",
        "email_verified": True,
        "phone_verified": True,
        "address": "123 Main Street, Springfield",
    }
)

user2, created = User.objects.get_or_create(
    email="jane@example.com",
    defaults={
        "first_name": "Jane",
        "last_name": "Smith",
        "email_verified": True,
        "phone_verified": True,
        "address": "456 Oak Avenue, Shelbyville",
    }
)

# Make john's account old (simulate 65 days)
print("Making john's account 65 days old...")
user1.date_joined = timezone.now() - timedelta(days=65)
user1.save()

# Add address verification to john
print("Verifying john's details...")
user1.address_verified = True
user1.government_id_verified = True
user1.save()

# Create some adoption requests (successful history)
print("Adding successful adoption history...")
pet = Pet.objects.first()
if pet:
    adoption1 = AdoptionRequest.objects.create(
        pet=pet,
        applicant=user1,
        status='approved'  # Counts toward history
    )

# Add reviews for john (reputation)
print("Adding user reviews...")
review1 = UserReview.objects.create(
    reviewed_user=user1,
    reviewer=user2,
    rating=5,
    comment="Great person to adopt from!"
)

review2 = UserReview.objects.create(
    reviewed_user=user1,
    reviewer=User.objects.create_user(email="bob@example.com", password="test"),
    rating=5,
    comment="Very trustworthy!"
)

print("\n" + "=" * 60)
print("TEST DATA CREATED!")
print("=" * 60)

# Check criteria
from accounts.utils import check_trusted_user_criteria

criteria = check_trusted_user_criteria(user1)

print(f"\nUser: {user1.email}")
for key, criterion in criteria.items():
    status = "✅" if criterion['met'] else "❌"
    print(f"{status} {criterion['name']}")

print(f"\nTrust Score: {user1.calculate_trust_score()}/100")
```

---

## How Users Become Trusted

### **Path 1: Manual Admin Approval (Fastest)**
1. Admin reviews user profile
2. Admin selects user in Users list
3. Admin clicks "Approve selected users as Trusted"
4. User is marked as trusted immediately

### **Path 2: Auto-Detection (Meets 3+ Criteria)**
1. User creates account
2. User completes profile (60+ days pass naturally)
3. User verifies email + phone (2+ verifications)
4. User successfully adopts pets (2+ adoptions)
5. Other users give good reviews (4.0+ rating)
6. Admin can then click approve button

### **Path 3: Criteria-Based Check**
Use utility function to check if user qualifies:

```python
from accounts.utils import should_be_trusted

# Manual approval required
if should_be_trusted(user, require_manual_approval=True):
    print("Admin approved this user")

# Or check if they meet 3+ criteria
if should_be_trusted(user, require_manual_approval=False):
    print("User meets 3+ criteria automatically")
```

---

## Quick Checklist

- [ ] Run: `python manage.py migrate accounts`
- [ ] Run: `python manage.py runserver`
- [ ] Go to: `http://127.0.0.1:8000/admin/`
- [ ] Create test users
- [ ] Fill in user profiles (first name, last name, address)
- [ ] Check email verification
- [ ] Create/approve adoption requests
- [ ] Add user reviews
- [ ] See trust score calculate
- [ ] Approve users as trusted using admin action

---

## Troubleshooting

**Q: Users not showing new columns?**
A: Run `python manage.py migrate accounts` and refresh page

**Q: "✓ Approve selected users as Trusted" button not showing?**
A: Clear browser cache or use Ctrl+Shift+R to hard refresh

**Q: UserReview not in admin?**
A: Migration may not have run. Run `python manage.py migrate accounts`

**Q: Need to verify email for 3 test users?**
A: Use shell:
```python
from django.contrib.auth import get_user_model
User = get_user_model()
User.objects.all().update(email_verified=True)
```

