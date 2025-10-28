# Generated migration file for adding base metrics fields to LandingConfig

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='landingconfig',
            name='base_voluntarios',
            field=models.IntegerField(
                blank=True,
                default=0,
                help_text='Número base a agregar al conteo de voluntarios activos. Útil para incluir datos históricos.',
                verbose_name='Base Voluntarios'
            ),
        ),
        migrations.AddField(
            model_name='landingconfig',
            name='base_organizaciones',
            field=models.IntegerField(
                blank=True,
                default=0,
                help_text='Número base a agregar al conteo de organizaciones. Útil para incluir datos históricos.',
                verbose_name='Base Organizaciones'
            ),
        ),
        migrations.AddField(
            model_name='landingconfig',
            name='base_proyectos',
            field=models.IntegerField(
                blank=True,
                default=0,
                help_text='Número base a agregar al conteo de proyectos/voluntariados. Útil para incluir datos históricos.',
                verbose_name='Base Proyectos'
            ),
        ),
        migrations.AddField(
            model_name='landingconfig',
            name='base_horas',
            field=models.DecimalField(
                blank=True,
                decimal_places=2,
                default=0,
                help_text='Número base de horas a agregar a las horas totales calculadas dinámicamente. Útil para incluir horas históricas.',
                max_digits=10,
                verbose_name='Base Horas'
            ),
        ),
    ]
