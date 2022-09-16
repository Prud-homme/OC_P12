# Generated by Django 4.1 on 2022-09-01 12:46

from django.db import migrations


def create_groups(apps, schema_migration):
    Group = apps.get_model("auth", "Group")
    Permission = apps.get_model("auth", "Permission")
    ContentType = apps.get_model("contenttypes", "ContentType")

    User = apps.get_model("authentication", "User")
    Client = apps.get_model("client", "Client")
    Contract = apps.get_model("contract", "Contract")
    Event = apps.get_model("event", "Event")

    sales_group, created = Group.objects.get_or_create(name="sales")
    support_group, created = Group.objects.get_or_create(name="support")
    management_group, created = Group.objects.get_or_create(name="management")

    ct = ContentType.objects.get_for_model(User)
    add_user = Permission.objects.create(
        codename="add_user", name="Can add user", content_type=ct
    )
    change_user = Permission.objects.create(
        codename="change_user", name="Can change user", content_type=ct
    )
    delete_user = Permission.objects.create(
        codename="delete_user", name="Can delete user", content_type=ct
    )
    view_user = Permission.objects.create(
        codename="view_user", name="Can view user", content_type=ct
    )

    ct = ContentType.objects.get_for_model(Group)
    view_group = Permission.objects.create(
        codename="view_group", name="Can view group", content_type=ct
    )

    ct = ContentType.objects.get_for_model(Client)
    add_client = Permission.objects.create(
        codename="can_add_client", name="Can add client", content_type=ct
    )
    change_client = Permission.objects.create(
        codename="change_client", name="Can change client", content_type=ct
    )
    view_client = Permission.objects.create(
        codename="view_client", name="Can view client", content_type=ct
    )

    ct = ContentType.objects.get_for_model(Contract)
    add_contract = Permission.objects.create(
        codename="add_contract", name="Can add contract", content_type=ct
    )
    change_contract = Permission.objects.create(
        codename="change_contract", name="Can change contract", content_type=ct
    )
    view_contract = Permission.objects.create(
        codename="view_contract", name="Can view contract", content_type=ct
    )

    ct = ContentType.objects.get_for_model(Event)
    add_event = Permission.objects.create(
        codename="add_event", name="Can add event", content_type=ct
    )
    change_event = Permission.objects.create(
        codename="change_event", name="Can change event", content_type=ct
    )
    view_event = Permission.objects.create(
        codename="view_event", name="Can view event", content_type=ct
    )

    sales_permissions = [
        add_client,
        change_client,
        view_client,
        add_contract,
        change_contract,
        view_contract,
        add_event,
    ]

    support_permissions = [
        change_event,
        view_event,
        view_client,
    ]

    management_permissions = [
        add_user,
        change_user,
        delete_user,
        view_user,
        change_client,
        view_client,
        change_contract,
        view_contract,
        change_event,
        view_event,
        view_group,
    ]

    sales_group.permissions.set(sales_permissions)
    support_group.permissions.set(support_permissions)
    management_group.permissions.set(management_permissions)


class Migration(migrations.Migration):

    dependencies = [
        ("authentication", "0001_initial"),
        ("client", "0001_initial"),
        ("contract", "0001_initial"),
        ("event", "0001_initial"),
    ]

    operations = [migrations.RunPython(create_groups)]
