from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.db import IntegrityError, transaction
from django.test import TestCase

from .models import UserProfile


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def make_user(username="testuser", password="testpass123"):
    """Create and return a fresh User instance via User.objects.create_user."""
    return User.objects.create_user(username=username, password=password)


# ---------------------------------------------------------------------------
# UserProfile model tests
# ---------------------------------------------------------------------------

class UserProfileAutoCreationTest(TestCase):
    """Tests that verify the post_save signal creates UserProfile records."""

    def test_profile_created_on_user_create(self):
        """UserProfile is automatically created when a new User is saved for the first time."""
        user = make_user()
        self.assertTrue(
            UserProfile.objects.filter(user=user).exists(),
            "Expected a UserProfile to exist for the newly created user.",
        )

    def test_profile_linked_to_correct_user(self):
        """The auto-created UserProfile is linked to the User that triggered the signal."""
        user = make_user()
        profile = UserProfile.objects.get(user=user)
        self.assertEqual(profile.user, user)

    def test_only_one_profile_created_per_user(self):
        """Saving an existing User multiple times does not create additional UserProfile records."""
        user = make_user()
        # Trigger additional saves — the signal should be a no-op for existing users.
        user.first_name = "Updated"
        user.save()
        user.last_name = "Again"
        user.save()

        profile_count = UserProfile.objects.filter(user=user).count()
        self.assertEqual(
            profile_count,
            1,
            "Expected exactly one UserProfile even after multiple saves of the same user.",
        )

    def test_separate_profiles_for_different_users(self):
        """Each User gets its own distinct UserProfile."""
        user_a = make_user(username="user_a")
        user_b = make_user(username="user_b")

        profile_a = UserProfile.objects.get(user=user_a)
        profile_b = UserProfile.objects.get(user=user_b)

        self.assertNotEqual(profile_a.pk, profile_b.pk)


# ---------------------------------------------------------------------------
# UserProfile __str__ tests
# ---------------------------------------------------------------------------

class UserProfileStrTest(TestCase):
    """Tests for the __str__ representation of UserProfile."""

    def test_str_returns_username(self):
        """__str__ returns the username of the associated User."""
        user = make_user(username="hotelguest")
        profile = UserProfile.objects.get(user=user)
        self.assertEqual(str(profile), "hotelguest")

    def test_str_reflects_username_change(self):
        """__str__ reflects any change to the User's username at call time."""
        user = make_user(username="oldname")
        profile = UserProfile.objects.get(user=user)

        user.username = "newname"
        user.save()
        # Re-fetch to ensure the profile still delegates to the live user object.
        profile.refresh_from_db()
        self.assertEqual(str(profile), "newname")


# ---------------------------------------------------------------------------
# Default field value tests
# ---------------------------------------------------------------------------

class UserProfileDefaultFieldsTest(TestCase):
    """Tests that verify UserProfile is initialised with the correct default values."""

    def setUp(self):
        self.user = make_user()
        self.profile = UserProfile.objects.get(user=self.user)

    def test_default_language_is_english(self):
        """language field defaults to 'en' (English)."""
        self.assertEqual(self.profile.language, "en")

    def test_default_contact_number_is_none(self):
        """contact_number defaults to None (null) when not supplied."""
        self.assertIsNone(self.profile.contact_number)

    def test_default_other_details_is_none(self):
        """other_details defaults to None (null) when not supplied."""
        self.assertIsNone(self.profile.other_details)


# ---------------------------------------------------------------------------
# contact_number field tests
# ---------------------------------------------------------------------------

class UserProfileContactNumberTest(TestCase):
    """Tests for the contact_number CharField."""

    def setUp(self):
        self.user = make_user()
        self.profile = UserProfile.objects.get(user=self.user)

    def test_contact_number_accepts_valid_string(self):
        """contact_number persists a valid phone-number string correctly."""
        self.profile.contact_number = "+94771234567"
        self.profile.save()
        self.profile.refresh_from_db()
        self.assertEqual(self.profile.contact_number, "+94771234567")

    def test_contact_number_accepts_blank_string(self):
        """contact_number accepts an empty string (blank=True)."""
        self.profile.contact_number = ""
        self.profile.save()
        self.profile.refresh_from_db()
        self.assertEqual(self.profile.contact_number, "")

    def test_contact_number_accepts_null(self):
        """contact_number can be set back to None (null=True)."""
        self.profile.contact_number = "+94771234567"
        self.profile.save()
        self.profile.contact_number = None
        self.profile.save()
        self.profile.refresh_from_db()
        self.assertIsNone(self.profile.contact_number)

    def test_contact_number_max_length(self):
        """contact_number rejects strings longer than 20 characters via full_clean."""
        self.profile.contact_number = "0" * 21  # one character over the limit
        with self.assertRaises(ValidationError):
            self.profile.full_clean()


# ---------------------------------------------------------------------------
# language field tests
# ---------------------------------------------------------------------------

class UserProfileLanguageFieldTest(TestCase):
    """Tests for the language CharField with restricted choices."""

    def setUp(self):
        self.user = make_user()
        self.profile = UserProfile.objects.get(user=self.user)

    def test_language_accepts_en(self):
        """language field accepts 'en' as a valid choice."""
        self.profile.language = "en"
        self.profile.full_clean()  # should not raise
        self.profile.save()
        self.profile.refresh_from_db()
        self.assertEqual(self.profile.language, "en")

    def test_language_accepts_sin(self):
        """language field accepts 'sin' (Sinhala) as a valid choice."""
        self.profile.language = "sin"
        self.profile.full_clean()  # should not raise
        self.profile.save()
        self.profile.refresh_from_db()
        self.assertEqual(self.profile.language, "sin")

    def test_language_accepts_tl(self):
        """language field accepts 'tl' (Tamil) as a valid choice."""
        self.profile.language = "tl"
        self.profile.full_clean()  # should not raise
        self.profile.save()
        self.profile.refresh_from_db()
        self.assertEqual(self.profile.language, "tl")

    def test_language_rejects_invalid_choice(self):
        """language field raises ValidationError for a value not in the defined choices."""
        self.profile.language = "fr"
        with self.assertRaises(ValidationError):
            self.profile.full_clean()

    def test_language_rejects_empty_string(self):
        """language field raises ValidationError for an empty string (not a valid choice)."""
        self.profile.language = ""
        with self.assertRaises(ValidationError):
            self.profile.full_clean()


# ---------------------------------------------------------------------------
# other_details JSONField tests
# ---------------------------------------------------------------------------

class UserProfileOtherDetailsTest(TestCase):
    """Tests for the other_details JSONField."""

    def setUp(self):
        self.user = make_user()
        self.profile = UserProfile.objects.get(user=self.user)

    def test_other_details_accepts_dict(self):
        """other_details persists a JSON object (dict) correctly."""
        payload = {"vip": True, "notes": "late checkout requested"}
        self.profile.other_details = payload
        self.profile.save()
        self.profile.refresh_from_db()
        self.assertEqual(self.profile.other_details, payload)

    def test_other_details_accepts_list(self):
        """other_details persists a JSON array (list) correctly."""
        payload = ["breakfast", "airport-transfer", "spa"]
        self.profile.other_details = payload
        self.profile.save()
        self.profile.refresh_from_db()
        self.assertEqual(self.profile.other_details, payload)

    def test_other_details_accepts_none(self):
        """other_details can be explicitly set to None (null)."""
        self.profile.other_details = {"key": "value"}
        self.profile.save()
        self.profile.other_details = None
        self.profile.save()
        self.profile.refresh_from_db()
        self.assertIsNone(self.profile.other_details)

    def test_other_details_accepts_nested_structure(self):
        """other_details handles arbitrarily nested JSON structures."""
        payload = {"preferences": {"room": "sea-view", "floor": 5}, "tags": ["vip"]}
        self.profile.other_details = payload
        self.profile.save()
        self.profile.refresh_from_db()
        self.assertEqual(self.profile.other_details, payload)


# ---------------------------------------------------------------------------
# OneToOne constraint tests
# ---------------------------------------------------------------------------

class UserProfileOneToOneConstraintTest(TestCase):
    """Tests for the OneToOneField uniqueness constraint between User and UserProfile."""

    def test_duplicate_profile_raises_integrity_error(self):
        """Creating a second UserProfile for the same User raises an IntegrityError."""
        user = make_user()
        # The signal already created one profile; attempting a second must fail.
        with self.assertRaises(IntegrityError):
            with transaction.atomic():
                UserProfile.objects.create(user=user)

    def test_different_users_can_each_have_a_profile(self):
        """Two different Users can each hold a UserProfile without constraint violation."""
        user_a = make_user(username="user_alpha")
        user_b = make_user(username="user_beta")
        # Both profiles were auto-created; no error should have been raised.
        self.assertTrue(UserProfile.objects.filter(user=user_a).exists())
        self.assertTrue(UserProfile.objects.filter(user=user_b).exists())


# ---------------------------------------------------------------------------
# Cascade delete tests
# ---------------------------------------------------------------------------

class UserProfileCascadeDeleteTest(TestCase):
    """Tests that verify cascading behaviour when a User is deleted."""

    def test_profile_deleted_when_user_deleted(self):
        """Deleting a User also deletes its associated UserProfile (CASCADE)."""
        user = make_user()
        profile_pk = UserProfile.objects.get(user=user).pk

        user.delete()

        self.assertFalse(
            UserProfile.objects.filter(pk=profile_pk).exists(),
            "Expected the UserProfile to be deleted when its User was deleted.",
        )

    def test_other_profiles_unaffected_by_unrelated_user_deletion(self):
        """Deleting one User does not remove profiles belonging to other Users."""
        user_to_delete = make_user(username="deleteme")
        user_to_keep = make_user(username="keepme")

        keep_profile_pk = UserProfile.objects.get(user=user_to_keep).pk
        user_to_delete.delete()

        self.assertTrue(
            UserProfile.objects.filter(pk=keep_profile_pk).exists(),
            "Expected the unrelated UserProfile to remain after deleting a different user.",
        )


# ---------------------------------------------------------------------------
# Signal behaviour tests
# ---------------------------------------------------------------------------

class CreateUserProfileSignalTest(TestCase):
    """Tests that verify the create_user_profile post_save signal behaviour."""

    def test_signal_fires_on_user_create(self):
        """The post_save signal creates a UserProfile exactly once when a User is first created."""
        initial_count = UserProfile.objects.count()
        make_user(username="signaluser")
        self.assertEqual(UserProfile.objects.count(), initial_count + 1)

    def test_signal_does_not_fire_on_user_update(self):
        """Updating (not creating) a User does not trigger an additional UserProfile creation."""
        user = make_user(username="updateuser")
        count_after_create = UserProfile.objects.count()

        # Perform several updates that fire post_save with created=False.
        user.email = "update1@example.com"
        user.save()
        user.first_name = "Updated"
        user.save()

        self.assertEqual(
            UserProfile.objects.count(),
            count_after_create,
            "Expected no new UserProfile records after updating an existing user.",
        )

    def test_signal_creates_profile_with_default_values(self):
        """The profile auto-created by the signal carries the correct field defaults."""
        user = make_user(username="defaultsuser")
        profile = UserProfile.objects.get(user=user)

        self.assertEqual(profile.language, "en")
        self.assertIsNone(profile.contact_number)
        self.assertIsNone(profile.other_details)

    def test_signal_not_called_when_created_flag_is_false(self):
        """
        Directly verifies the guard condition: when post_save fires with created=False
        (simulated by a manual save), no second profile is created.
        """
        user = make_user(username="guardtest")
        profile_pk_before = UserProfile.objects.get(user=user).pk

        # Force another post_save with created=False.
        user.save()

        profile_after = UserProfile.objects.get(user=user)
        self.assertEqual(
            profile_after.pk,
            profile_pk_before,
            "Expected the same UserProfile instance (same pk) after re-saving the user.",
        )