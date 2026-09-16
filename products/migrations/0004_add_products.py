from django.db import migrations

def add_sneakers(apps, schema_editor):
    Product = apps.get_model('products', 'Product')
    Product.objects.create(
        name="UltraBoost Blue",
        brand="Adidas",
        product_type="Sneakers",
        size="9",
        color="Blue",
        year_of_manufacture=2024,
        price=180.00,
        rating=4.7,
        image="products/ultraboost_blue.png"
    )
    Product.objects.create(
        name="X",
        brand="Puma",
        product_type="Sneakers",
        size="8",
        color="Black",
        year_of_manufacture=2022,
        price=120.00,
        rating=4.3,
        image="products/classic_black.png"
    )

class Migration(migrations.Migration):

    dependencies = [
        ('products', '0003_alter_product_image'),
    ]

    operations = [
        migrations.RunPython(add_sneakers),
    ]