from django import forms
from users.models import UserProfile
from users.choices import STATE_CHOICES


class SignUpForm(forms.ModelForm):
    password = forms.CharField(
        widget=forms.PasswordInput(
            attrs={
                "placeholder": "********",
                "autocomplete": "off",
                "data-toggle": "password",
            }
        )
    )
    confirm_password = forms.CharField(
        widget=forms.PasswordInput(
            attrs={
                "placeholder": "********",
                "autocomplete": "off",
                "data-toggle": "password",
            }
        ),
        label="Confirm Password",
    )

    # Build Address
    street1 = forms.CharField(max_length=255, label="Street 1")
    street2 = forms.CharField(max_length=255, required=False, label="Street 2")
    city = forms.CharField(max_length=100, label="City")
    state = forms.ChoiceField(choices=STATE_CHOICES, label="State")
    zipcode = forms.CharField(max_length=20, label="Zipcode")

    class Meta:
        model = UserProfile
        fields = [
            "first_name",
            "last_name",
            "email_address",
            "phone_number",
            "street1",
            "street2",
            "city",
            "state",
            "zipcode",
            "username",
            "password",
            "confirm_password",
        ]
        labels = {
            "first_name": "First Name",
            "last_name": "Last Name",
            "email_address": "Email Address",
            "phone_number": "Phone Number (optional)",
        }

    # Ensure passwords match
    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        confirm_password = cleaned_data.get("confirm_password")

        if password != confirm_password:
            raise forms.ValidationError("Passwords do not match.")

        # Clean and update the address
        address = self.clean_address(cleaned_data)
        cleaned_data["address"] = address

        return cleaned_data

    def clean_address(self, cleaned_data):
        street1 = cleaned_data.get("street1")
        street2 = cleaned_data.get("street2")
        city = cleaned_data.get("city")
        state = cleaned_data.get("state")
        zipcode = cleaned_data.get("zipcode")

        # Handle optional street2
        address_parts = [street1, street2, city, state, zipcode]

        # Only join non-empty parts
        address = ", ".join(filter(None, address_parts))
        return address.strip()
