"""
Replace Wagtail's default 'Welcome' page with a real HomePage and point the
default Site at it, so a fresh install lands on a working homepage.
"""

from django.db import migrations


def create_homepage(apps, schema_editor):
    ContentType = apps.get_model("contenttypes.ContentType")
    Page = apps.get_model("wagtailcore.Page")
    Site = apps.get_model("wagtailcore.Site")
    HomePage = apps.get_model("home.HomePage")

    # Remove the boilerplate page the Wagtail scaffold creates.
    Page.objects.filter(slug="home", content_type__model="page").delete()

    homepage_content_type, _ = ContentType.objects.get_or_create(
        model="homepage", app_label="home"
    )

    root = Page.objects.get(id=1)

    homepage = HomePage.objects.create(
        title="Home",
        draft_title="Home",
        slug="home",
        content_type=homepage_content_type,
        path="00010001",
        depth=2,
        numchild=0,
        url_path="/home/",
        live=True,
        show_in_menus=False,
        locale_id=root.locale_id,
        hero_eyebrow="Engineering partners",
        hero_heading="Build what moves your business forward",
        hero_subheading=(
            "Endeavours designs, builds and runs the digital systems that "
            "serious companies depend on."
        ),
        hero_buttons="[]",
        body="[]",
        cta_buttons="[]",
    )

    root.numchild = 1
    root.save(update_fields=["numchild"])

    Site.objects.update_or_create(
        is_default_site=True,
        defaults={
            "hostname": "localhost",
            "port": 80,
            "root_page": homepage,
            "site_name": "Endeavours",
        },
    )


def remove_homepage(apps, schema_editor):
    HomePage = apps.get_model("home.HomePage")
    HomePage.objects.filter(slug="home").delete()


class Migration(migrations.Migration):
    dependencies = [
        ("home", "0001_initial"),
        ("wagtailcore", "0098_apitoken"),
    ]

    operations = [
        migrations.RunPython(create_homepage, remove_homepage),
    ]
