# -*- coding: utf-8 -*-
# Generated by Django 1.10.4 on 2017-01-12 19:17
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import modelcluster.contrib.taggit
import modelcluster.fields
import taggit.managers
import wagtail.wagtailcore.blocks
import wagtail.wagtailcore.fields
import wagtail.wagtailcore.models
import wagtail.wagtailimages.blocks
import wagtail.wagtailimages.models
import wagtail.wagtailsearch.index


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('taggit', '0002_auto_20150616_2121'),
        ('business', '0001_initial'),
        ('wagtailimages', '0016_deprecate_rendition_filter_relation'),
        ('wagtailcore', '0032_add_bulk_delete_page_permission'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='AmountNode',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('sort_order', models.IntegerField(blank=True, editable=False, null=True)),
                ('amount_label', models.CharField(default=None, max_length=15, verbose_name='Label Amount')),
                ('amount', models.PositiveIntegerField(default=0.0, verbose_name='Amount')),
            ],
            options={
                'ordering': ['sort_order'],
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('url', models.URLField(blank=True, null=True)),
                ('text', models.CharField(blank=True, max_length=255, null=True, verbose_name='Label')),
            ],
            options={
                'verbose_name': 'Category',
                'verbose_name_plural': 'Categories',
            },
        ),
        migrations.CreateModel(
            name='ImageCategory',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('url', models.URLField(blank=True, null=True)),
                ('text', models.CharField(blank=True, max_length=255, null=True, verbose_name='Label')),
            ],
            options={
                'verbose_name': 'Image Snip',
                'verbose_name_plural': 'Image Snips',
            },
        ),
        migrations.CreateModel(
            name='PageChannel',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('sort_order', models.IntegerField(blank=True, editable=False, null=True)),
                ('amount', models.FloatField(default=0.0, verbose_name='Amount')),
            ],
            options={
                'ordering': ['sort_order'],
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='PrePageTag',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='PrepyDocs',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=255, verbose_name='title')),
                ('file', models.FileField(upload_to='documents', verbose_name='file')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='created at')),
                ('to_render', models.BooleanField(default=False, verbose_name='Renderize')),
                ('active', models.BooleanField(default=False, verbose_name='Current rate')),
                ('collection', models.ForeignKey(default=wagtail.wagtailcore.models.get_root_collection_id, on_delete=django.db.models.deletion.CASCADE, related_name='+', to='wagtailcore.Collection', verbose_name='collection')),
                ('currency', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to='business.Currency')),
                ('tags', taggit.managers.TaggableManager(blank=True, help_text=None, through='taggit.TaggedItem', to='taggit.Tag', verbose_name='tags')),
                ('uploaded_by_user', models.ForeignKey(blank=True, editable=False, null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL, verbose_name='uploaded by user')),
            ],
            options={
                'verbose_name': 'document',
                'abstract': False,
            },
            bases=(wagtail.wagtailsearch.index.Indexed, models.Model),
        ),
        migrations.CreateModel(
            name='PrepyImage',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=255, verbose_name='title')),
                ('file', models.ImageField(height_field='height', upload_to=wagtail.wagtailimages.models.get_upload_to, verbose_name='file', width_field='width')),
                ('width', models.IntegerField(editable=False, verbose_name='width')),
                ('height', models.IntegerField(editable=False, verbose_name='height')),
                ('created_at', models.DateTimeField(auto_now_add=True, db_index=True, verbose_name='created at')),
                ('focal_point_x', models.PositiveIntegerField(blank=True, null=True)),
                ('focal_point_y', models.PositiveIntegerField(blank=True, null=True)),
                ('focal_point_width', models.PositiveIntegerField(blank=True, null=True)),
                ('focal_point_height', models.PositiveIntegerField(blank=True, null=True)),
                ('file_size', models.PositiveIntegerField(editable=False, null=True)),
                ('caption', models.CharField(blank=True, max_length=255, null=True, verbose_name='Caption')),
                ('collection', models.ForeignKey(default=wagtail.wagtailcore.models.get_root_collection_id, on_delete=django.db.models.deletion.CASCADE, related_name='+', to='wagtailcore.Collection', verbose_name='collection')),
                ('snip', models.ForeignKey(blank=True, default=1, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to='cms.ImageCategory')),
                ('tags', taggit.managers.TaggableManager(blank=True, help_text=None, through='taggit.TaggedItem', to='taggit.Tag', verbose_name='tags')),
                ('uploaded_by_user', models.ForeignKey(blank=True, editable=False, null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL, verbose_name='uploaded by user')),
            ],
            options={
                'abstract': False,
            },
            bases=(wagtail.wagtailsearch.index.Indexed, models.Model),
        ),
        migrations.CreateModel(
            name='Prepyme',
            fields=[
                ('page_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='wagtailcore.Page')),
                ('body', wagtail.wagtailcore.fields.StreamField((('Heading', wagtail.wagtailcore.blocks.CharBlock(classname='field heading')), ('Paragraph', wagtail.wagtailcore.blocks.RichTextBlock()), ('Image', wagtail.wagtailimages.blocks.ImageChooserBlock())))),
            ],
            options={
                'verbose_name': 'Root Page',
                'verbose_name_plural': 'Root Pages',
            },
            bases=('wagtailcore.page',),
        ),
        migrations.CreateModel(
            name='PrepyRendition',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('filter_spec', models.CharField(db_index=True, max_length=255)),
                ('file', models.ImageField(height_field='height', upload_to=wagtail.wagtailimages.models.get_rendition_upload_to, width_field='width')),
                ('width', models.IntegerField(editable=False)),
                ('height', models.IntegerField(editable=False)),
                ('focal_point_key', models.CharField(blank=True, default='', editable=False, max_length=255)),
                ('filter', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='+', to='wagtailimages.Filter')),
                ('image', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='renditions', to='cms.PrepyImage')),
            ],
        ),
        migrations.CreateModel(
            name='WebServiceOperators',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('iso_country', models.CharField(blank=True, max_length=255, null=True, verbose_name='ISO 2')),
                ('iso_operator', models.CharField(blank=True, max_length=255, null=True, verbose_name='Operator')),
                ('operator_name', models.CharField(blank=True, max_length=255, null=True, verbose_name='Operator Name')),
                ('prefix', models.CharField(blank=True, max_length=255, null=True, verbose_name='Operator Name')),
            ],
        ),
        migrations.CreateModel(
            name='Pages',
            fields=[
                ('prepyme_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='cms.Prepyme')),
            ],
            options={
                'verbose_name': 'Page',
                'verbose_name_plural': 'Pages',
            },
            bases=('cms.prepyme',),
        ),
        migrations.CreateModel(
            name='Promotion',
            fields=[
                ('prepyme_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='cms.Prepyme')),
            ],
            options={
                'verbose_name': 'Promotion',
                'verbose_name_plural': 'Promotions',
            },
            bases=('cms.prepyme',),
        ),
        migrations.AddField(
            model_name='prepyme',
            name='cat',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to='cms.Category', verbose_name='Category'),
        ),
        migrations.AddField(
            model_name='prepyme',
            name='country',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to='business.Country'),
        ),
        migrations.AddField(
            model_name='prepyme',
            name='document',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to='cms.PrepyDocs'),
        ),
        migrations.AddField(
            model_name='prepyme',
            name='main_image',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to='cms.PrepyImage'),
        ),
        migrations.AddField(
            model_name='prepyme',
            name='parent',
            field=modelcluster.fields.ParentalKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='children', to='wagtailcore.Page'),
        ),
        migrations.AddField(
            model_name='prepyme',
            name='tags',
            field=modelcluster.contrib.taggit.ClusterTaggableManager(blank=True, help_text='A comma-separated list of tags.', through='cms.PrePageTag', to='taggit.Tag', verbose_name='Tags'),
        ),
        migrations.AddField(
            model_name='prepagetag',
            name='content_object',
            field=modelcluster.fields.ParentalKey(on_delete=django.db.models.deletion.CASCADE, related_name='tagged_items', to='cms.Prepyme'),
        ),
        migrations.AddField(
            model_name='prepagetag',
            name='tag',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='cms_prepagetag_items', to='taggit.Tag'),
        ),
    ]
