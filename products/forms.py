from django import forms


class RatingForm(forms.Form):
    """
    Form for submitting a product rating and an optional written review.

    This form is used on the product detail page to allow users to:
    - Select a rating between 1 and 5
    - Optionally write a text review

    Fields
    ------
    rating : ChoiceField
        A required field allowing users to choose a rating from 1 to 5.
        Displayed using radio buttons.
    review : CharField
        An optional text field for writing a review.
        Rendered as a textarea with placeholder text.

    Notes
    -----
    - The `review` field is optional.
    - The `rating` field is required and must be one of the predefined choices.
    """

    rating = forms.ChoiceField(
        choices=[(i, i) for i in range(1, 6)],
        widget=forms.RadioSelect
    )
    review = forms.CharField(
        widget=forms.Textarea(
            attrs={
                'placeholder': 'Write a review (optional)',
                'rows': 4
            }
        ),
        required=False
    )