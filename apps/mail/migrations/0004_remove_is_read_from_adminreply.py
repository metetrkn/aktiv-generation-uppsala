from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('mail', '0003_adminreply'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='adminreply',
            name='is_read',
        ),
    ] 