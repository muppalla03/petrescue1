# Trusted User Feature Documentation

## Overview
The Trusted User feature implements a multi-criteria system to identify and mark reliable users in the Pet Rescue platform. Users can be trusted based on 5 key criteria.

---

## 5 Criteria for Trusted User Status

### 1. **Manual Admin Approval** (Highest Priority)
**Criterion**: Admin approval after identity/contact verification

**How it works**:
- Admins review user profiles in the Django admin panel
- Check user's identity and contact information
- Use the "Approve selected users as Trusted" action in admin interface
- Records who approved and when

**Implementation**:
- Fields: `is_trusted_approved_by`, `is_trusted_approved_at`, `trusted_approval_reason`
- Admin action: `approve_as_trusted`
- Can be revoked with: `revoke_trusted_status`

---

### 2. **Proven History** 
**Criterion**: 3–5 successful adoptions or listings with no reports

**How it works**:
- System tracks successful pet adoptions (adoption requests with status='approved')
- System tracks successful pet listings/requests (pets with is_approved=True)
- Counts both types together (minimum 3 required)

**Implementation**:
- Methods:
  - `user.get_successful_adoptions_count()` - Returns number of approved adoptions
  - `user.get_successful_listings_count()` - Returns number of approved pet posts
- Trust score bonus: 25 points (for 3+), 10 points (for 1-2)

**Admin Display**:
- Shows in list view under "Successful History" column
- Format: "Total: X (Adoptions: Y, Listings: Z)"

---

### 3. **Account Age + Activity**
**Criterion**: Account older than 60 days and completed profile

**How it works**:
- Account age: 60+ days since registration (date_joined)
- Profile completeness: First name + Last name + Email verified + Address filled
- Both conditions must be true

**Implementation**:
- Methods:
  - `user.is_account_old_enough(days=60)` - Checks account age
  - `user.is_profile_complete()` - Checks profile completion
- Trust score bonus: 25 points (both met), 10 points (age only)

**Admin Display**:
- Shows in list view under "Account Age" column
- Color-coded: Green (60+ days), Orange (30-60 days), Red (< 30 days)

---

### 4. **Verification Signals**
**Criterion**: Phone/Email verified, Address verified, Government ID check

**How it works**:
- Multiple verification fields tracked
- At least 2 verifications required for criterion to be met
- Each verification is a boolean flag

**Verification Fields**:
1. `email_verified` - Email address verified
2. `phone_verified` - Phone number verified
3. `address_verified` - Physical address verified
4. `government_id_verified` - Government ID check passed

**Implementation**:
- Utility functions to mark verified:
  - `verify_user_email(user)` 
  - `verify_user_phone(user)`
  - `verify_user_address(user)`
  - `verify_user_government_id(user)`
- Trust score bonus: 5 points per verification (max 20)

**Admin Display**:
- Shows in list filter and fieldset
- Summary: "✓ Email | ✓ Phone | ✓ Address | ✓ ID"

---

### 5. **Community Reputation**
**Criterion**: Positive reviews or endorsements (4+ rating average)

**How it works**:
- Other users rate/review this user (1-5 stars)
- System calculates average rating
- 4.0+ average rating qualifies

**Implementation**:
- Model: `UserReview`
  - Fields: `reviewed_user`, `reviewer`, `rating` (1-5), `comment`, `created_at`
  - One review per reviewer (unique_together constraint)
- Methods:
  - `user.get_average_rating()` - Returns average rating
- Trust score bonus: 15 points (4.5+), 10 points (4.0-4.5), 5 points (1+)

**Admin Interface**:
- Dedicated UserReview admin with star rating display
- Filter by rating and date
- Search by reviewer and reviewed user email

---

## Usage Guide

### For Admins

#### Approve a User as Trusted:
1. Go to Django Admin → Users
2. Select one or more users
3. Choose action: "✓ Approve selected users as Trusted"
4. Click "Go"
5. Confirmation message shows how many users were approved

#### Revoke Trusted Status:
1. Go to Django Admin → Users
2. Filter by "is_trusted" = True
3. Select users to revoke
4. Choose action: "✗ Revoke Trusted status"
5. Click "Go"

#### Mark Verifications:
1. Open user profile in admin
2. Check verification fields:
   - Email verified
   - Phone verified
   - Address verified
   - Government ID verified
3. Save changes

#### View User Trust Details:
- Trust Status: Green checkmark if trusted, red X if not
- Verifications: Shows status of all 4 verification types
- Account Age: Shows days since registration with color coding
- Successful History: Shows adoption and listing counts

#### Add User Review:
1. Go to Django Admin → User Reviews
2. Click "Add User Review"
3. Select reviewed user and reviewer
4. Choose rating (1-5 stars)
5. Add optional comment
6. Save

---

### For Developers

#### Check if User is Trusted:
```python
from django.contrib.auth import get_user_model

User = get_user_model()
user = User.objects.get(email="example@example.com")

# Direct check
if user.is_trusted:
    print("User is trusted!")

# Check individual criteria
score = user.calculate_trust_score()  # Returns 0-100
print(f"Trust score: {score}")
```

#### Check Which Criteria Are Met:
```python
from accounts.utils import check_trusted_user_criteria

criteria_results = check_trusted_user_criteria(user)

for criterion_key, criterion_data in criteria_results.items():
    print(f"{criterion_data['name']}: {criterion_data['met']}")
    print(f"Details: {criterion_data['details']}")
```

#### Determine if User Should Be Trusted:
```python
from accounts.utils import should_be_trusted

# With manual approval required (default, Criterion 1)
if should_be_trusted(user, require_manual_approval=True):
    print("Admin approved!")

# Without requiring manual approval (meets 3+ criteria)
if should_be_trusted(user, require_manual_approval=False):
    print("Meets automatic criteria!")
```

#### Get Eligible Users:
```python
from accounts.utils import get_users_eligible_for_trusted_status

eligible_users = get_users_eligible_for_trusted_status()
print(f"Found {len(eligible_users)} users eligible for trusted status")

for user in eligible_users:
    print(f"- {user.email}: Trust score {user.calculate_trust_score()}")
```

#### Verify User Details:
```python
from accounts.utils import (
    verify_user_email,
    verify_user_phone,
    verify_user_address,
    verify_user_government_id
)

# Mark email as verified
verify_user_email(user)

# Mark phone as verified
verify_user_phone(user)

# Continue for other fields...
```

---

## Database Schema

### CustomUser Fields (Extended)
```
- is_trusted (Boolean) - Main trusted status flag
- phone_number (String, optional) - User's phone number
- phone_verified (Boolean) - Whether phone is verified
- email_verified (Boolean) - Whether email is verified
- address (Text, optional) - User's address
- address_verified (Boolean) - Whether address is verified
- government_id_verified (Boolean) - Whether government ID is verified
- is_trusted_approved_by (ForeignKey to User) - Admin who approved
- is_trusted_approved_at (DateTime) - When approval occurred
- trusted_approval_reason (Text) - Reason for approval
```

### UserReview Model
```
- reviewed_user (ForeignKey to User) - The user being reviewed
- reviewer (ForeignKey to User) - The user giving the review
- rating (Integer 1-5) - Star rating
- comment (Text) - Review comment
- created_at (DateTime) - When review was created
```

---

## Trust Score Calculation

The system calculates a numerical trust score (0-100):

| Criterion | Points | Conditions |
|-----------|--------|-----------|
| Admin Approval | 30 | is_trusted_approved_by NOT NULL |
| History | 25 (max) | 3+ successful adoptions/listings |
| | 10 | 1-2 successful |
| Account Age | 25 (max) | 60+ days old + profile complete |
| | 10 | 30-60 days old |
| Verifications | 20 (max) | 5 points per verification (×4 max) |
| Reputation | 15 (max) | 4.5+ avg rating |
| | 10 | 4.0-4.5 rating |
| | 5 | 1.0+ rating |

**Total Possible Score: 100+**

---

## Notifications

When verification occurs, user receives email notifications:
- "Your email has been verified! ✓"
- "Your phone number has been verified! ✓"
- "Your address has been verified! ✓"
- "Your government ID has been verified! ✓"

---

## Integration Points

### With Adoption System
- Tracks approval of adoption requests → counts toward "Proven History"
- Higher trust users may get priority in adoption process

### With Pet Listing System
- Tracks approval of pet listings/requests → counts toward "Proven History"

### With Admin Panel
- Full UI integration for managing trusted users
- Custom admin actions for bulk approval/revocation
- Color-coded badges and detailed status displays

---

## Migration Files

File: `accounts/migrations/0004_trusted_user_feature.py`
- Adds all new fields to CustomUser
- Creates UserReview model
- One-time migration (run with: `python manage.py migrate accounts`)

---

## Future Enhancements

1. **Automated Reputation Calculation**: Auto-update trust status when criteria are met
2. **Trust Degradation**: Reduce score if user has complaint reports
3. **Email Verification**: Automatic email verification link system
4. **Phone Verification**: SMS-based phone verification
5. **Address Validation**: API integration with address verification service
6. **Review Visibility**: Show trust scores/reviews on user profiles
7. **Trust Badges**: Display on pet listings and adoption requests
8. **Admin Dashboard**: Charts showing trusted user metrics

---

## Testing Commands

```bash
# Generate migrations
python manage.py makemigrations accounts

# Apply migrations
python manage.py migrate accounts

# Create test users
python manage.py shell
>>> from django.contrib.auth import get_user_model
>>> from datetime import timedelta
>>> from django.utils import timezone
>>> User = get_user_model()
>>> 
>>> # Create test user
>>> user = User.objects.create_user(
...     email="test@example.com",
...     password="testpass123",
...     first_name="Test",
...     last_name="User",
...     email_verified=True,
...     address="123 Main St"
... )
>>> 
>>> # Check if account is old enough (simulate 61 days)
>>> user.date_joined = timezone.now() - timedelta(days=61)
>>> user.save()
>>> 
>>> # Verify criteria
>>> from accounts.utils import check_trusted_user_criteria
>>> criteria = check_trusted_user_criteria(user)
>>> for k, v in criteria.items():
...     print(f"{v['name']}: {v['met']}")
```

---

## Support & Maintenance

- Monitor admin approval trends
- Review trust score distribution regularly
- Update criteria thresholds if needed
- Archive old user review data periodically
- Audit trusted user list quarterly
