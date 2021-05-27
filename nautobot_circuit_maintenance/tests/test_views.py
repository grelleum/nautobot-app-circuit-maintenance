# pylint: disable=duplicate-code
"""Test for Circuit Maintenace Views."""
from nautobot.circuits.models import Circuit, CircuitType, Provider
from nautobot.utilities.testing import ViewTestCases
from nautobot_circuit_maintenance.models import (
    CircuitMaintenance,
    CircuitImpact,
    Note,
    NotificationSource,
    ParsedNotification,
    RawNotification,
)


class CircuitMaintenanceTest(ViewTestCases.PrimaryObjectViewTestCase):
    """View tests for CircuitMaintenance."""

    model = CircuitMaintenance

    def _get_base_url(self):
        return "plugins:{}:{}_{{}}".format(self.model._meta.app_label, self.model._meta.model_name)

    def assertInstanceEqual(self, instance, data, api=False):  # pylint: disable=arguments-differ
        """Used to overwrite inbuilt function. Causing type issues for datetimepicker."""

    @classmethod
    def setUpTestData(cls):
        """Setup environment for testing."""
        CircuitMaintenance.objects.create(
            name="UT-TEST-1", start_time="2020-10-04 10:00:00", end_time="2020-10-04 12:00:00"
        )
        CircuitMaintenance.objects.create(
            name="UT-TEST-2", start_time="2020-10-05 10:00:00", end_time="2020-10-05 12:00:00"
        )

        cls.form_data = {
            "name": "UT-TEST-10",
            "start_time": "2020-10-06 10:00:00",
            "end_time": "2020-10-06 12:00:00",
            "description": "TEST 0 descr",
        }

        cls.csv_data = (
            "name,start_time,end_time,description",
            "UT-TEST-20, 2020-10-06 10:00:00, 2020-10-06 12:00:00, TEST 20 descr",
            "UT-TEST-21, 2020-10-06 10:00:00, 2020-10-06 12:00:00, TEST 21 descr",
            "UT-TEST-22, 2020-10-06 10:00:00, 2020-10-06 12:00:00, TEST 22 descr",
        )

        cls.bulk_edit_data = {
            "status": "CANCELLED",
        }


class CircuitImpactTest(ViewTestCases.OrganizationalObjectViewTestCase):
    """View tests for CircuitImpact."""

    model = CircuitImpact

    def _get_base_url(self):
        return "plugins:{}:{}_{{}}".format(self.model._meta.app_label, self.model._meta.model_name)

    def assertInstanceEqual(self, instance, data, api=False):  # pylint: disable=arguments-differ
        """Used to overwrite inbuilt function. Causing type issues for datetimepicker."""

    @classmethod
    def setUpTestData(cls):
        """Setup environment for testing."""
        providers = (
            Provider(name="Provider 3", slug="provider-3"),
            Provider(name="Provider 4", slug="provider-4"),
        )
        Provider.objects.bulk_create(providers)

        circuit_types = (
            CircuitType(name="Circuit Type 3", slug="circuit-type-3"),
            CircuitType(name="Circuit Type 4", slug="circuit-type-4"),
        )
        CircuitType.objects.bulk_create(circuit_types)

        circuits = (
            Circuit(cid="Circuit 4", provider=providers[0], type=circuit_types[0]),
            Circuit(cid="Circuit 5", provider=providers[1], type=circuit_types[1]),
            Circuit(cid="Circuit 6", provider=providers[1], type=circuit_types[0]),
            Circuit(cid="Circuit 7", provider=providers[1], type=circuit_types[0]),
            Circuit(cid="Circuit 8", provider=providers[1], type=circuit_types[0]),
        )
        Circuit.objects.bulk_create(circuits)

        existing_maintenance = [
            CircuitMaintenance(name="UT-TEST-3", start_time="2020-10-04 10:00:00", end_time="2020-10-04 12:00:00"),
            CircuitMaintenance(name="UT-TEST-4", start_time="2020-10-05 10:00:00", end_time="2020-10-05 12:00:00"),
        ]
        CircuitMaintenance.objects.bulk_create(existing_maintenance)

        circuit_impacts = [
            CircuitImpact(
                maintenance=existing_maintenance[0],
                circuit=circuits[0],
            ),
            CircuitImpact(
                maintenance=existing_maintenance[1],
                circuit=circuits[0],
            ),
        ]
        CircuitImpact.objects.bulk_create(circuit_impacts)

        cls.form_data = {"maintenance": existing_maintenance[0], "circuit": circuits[1], "impact": "NO-IMPACT"}

        cls.csv_data = (
            "maintenance,circuit,impact",
            f"{existing_maintenance[0].pk}, {circuits[2].pk}, NO-IMPACT",
            f"{existing_maintenance[0].pk}, {circuits[3].pk}, OUTAGE",
            f"{existing_maintenance[0].pk}, {circuits[4].pk}, DEGRADED",
        )

        cls.bulk_edit_data = {
            "impact": "OUTAGE",
        }

    def test_list_objects_with_constrained_permission(self):
        """TODO: fix because it's checking the get_absolute_url() in a wrong page."""


class NoteTest(ViewTestCases.OrganizationalObjectViewTestCase):
    """View tests for Note."""

    model = Note

    def _get_base_url(self):
        return "plugins:{}:{}_{{}}".format(self.model._meta.app_label, self.model._meta.model_name)

    def assertInstanceEqual(self, instance, data, api=False):  # pylint: disable=arguments-differ
        """Used to overwrite inbuilt function. Causing type issues for datetimepicker."""

    @classmethod
    def setUpTestData(cls):
        """Setup environment for testing."""

        maintenance = CircuitMaintenance.objects.create(
            name="UT-TEST-1", start_time="2020-10-04 10:00:00", end_time="2020-10-04 12:00:00"
        )

        Note.objects.create(maintenance=maintenance, title="Note 1", comment="comment 1")
        Note.objects.create(maintenance=maintenance, title="Note 2", comment="comment 2")

        cls.form_data = {"maintenance": maintenance, "title": "Note 3", "level": "INFO", "comment": "comment 3"}

        cls.csv_data = (
            "maintenance,title,comment",
            f"{maintenance.pk}, Note 4, comment 4",
            f"{maintenance.pk}, Note 5, comment 5",
        )

        cls.bulk_edit_data = {"level": "WARNING"}

    def test_list_objects_with_constrained_permission(self):
        """TODO: fix because it's checking the get_absolute_url() in a wrong page."""


class NotificationSourceTest(ViewTestCases.OrganizationalObjectViewTestCase):
    """View tests for NotificationSource."""

    model = NotificationSource

    def _get_base_url(self):
        return "plugins:{}:{}_{{}}".format(self.model._meta.app_label, self.model._meta.model_name)

    def assertInstanceEqual(self, instance, data, api=False):  # pylint: disable=arguments-differ
        """Used to overwrite inbuilt function. Causing type issues for datetimepicker."""

    @classmethod
    def setUpTestData(cls):
        """Setup environment for testing."""
        providers = (
            Provider(name="Provider 3", slug="provider-3"),
            Provider(name="Provider 4", slug="provider-4"),
        )
        Provider.objects.bulk_create(providers)

        notificationsource_1 = NotificationSource.objects.create(
            source_id="whatever1@validemail.com", _password="password", server="whatever"
        )
        notificationsource_2 = NotificationSource.objects.create(
            source_id="whatever2@validemail.com", _password="password", server="whatever"
        )

        notificationsource_1.providers.set(providers)
        notificationsource_2.providers.set(providers)

        cls.form_data = {
            "source_id": "whatever3@validemail.com",
            "_password": "password",
            "server": "whatever",
            "providers": providers,
        }

        cls.csv_data = (
            "source_id,_password,server,port",
            "whatever4@validemail.com, password, whatever, 995",
            "whatever5@validemail.com, password, whatever, 996",
        )

        cls.bulk_edit_data = {"source_type": "GMAIL"}

    def test_list_objects_with_constrained_permission(self):
        """TODO: fix because it's checking the get_absolute_url() in a wrong page."""


class RawNotificationTest(
    ViewTestCases.GetObjectViewTestCase,
    # ViewTestCases.GetObjectChangelogViewTestCase,
    # ViewTestCases.CreateObjectViewTestCase,
    # ViewTestCases.EditObjectViewTestCase,
    ViewTestCases.DeleteObjectViewTestCase,
    ViewTestCases.ListObjectsViewTestCase,
    # ViewTestCases.BulkImportObjectsViewTestCase,
    ViewTestCases.BulkDeleteObjectsViewTestCase,
):
    """View tests for RawNotification."""

    model = RawNotification

    def _get_base_url(self):
        return "plugins:{}:{}_{{}}".format(self.model._meta.app_label, self.model._meta.model_name)

    def assertInstanceEqual(self, instance, data, api=False):  # pylint: disable=arguments-differ
        """Used to overwrite inbuilt function. Causing type issues for datetimepicker."""

    @classmethod
    def setUpTestData(cls):
        """Setup environment for testing."""
        providers = (
            Provider(name="Provider 3", slug="provider-3"),
            Provider(name="Provider 4", slug="provider-4"),
        )
        Provider.objects.bulk_create(providers)

        RawNotification.objects.create(
            subject="whatever", provider=providers[0], sender="whatever", source="whatever", raw="whatever 1"
        )

        RawNotification.objects.create(
            subject="whatever", provider=providers[1], sender="whatever", source="whatever", raw="whatever 2"
        )

    def test_list_objects_with_constrained_permission(self):
        """TODO: fix because it's checking the get_absolute_url() in a wrong page."""


class ParsedNotificationTest(
    ViewTestCases.GetObjectViewTestCase,
    # ViewTestCases.GetObjectChangelogViewTestCase,
    # ViewTestCases.CreateObjectViewTestCase,
    # ViewTestCases.EditObjectViewTestCase,
    # ViewTestCases.DeleteObjectViewTestCase,
    # ViewTestCases.ListObjectsViewTestCase,
    # ViewTestCases.BulkImportObjectsViewTestCase,
    # ViewTestCases.BulkDeleteObjectsViewTestCase,
):
    """View tests for ParsedNotification."""

    model = ParsedNotification

    def _get_base_url(self):
        return "plugins:{}:{}_{{}}".format(self.model._meta.app_label, self.model._meta.model_name)

    def assertInstanceEqual(self, instance, data, api=False):  # pylint: disable=arguments-differ
        """Used to overwrite inbuilt function. Causing type issues for datetimepicker."""

    @classmethod
    def setUpTestData(cls):
        """Setup environment for testing."""
        providers = (
            Provider(name="Provider 3", slug="provider-3"),
            Provider(name="Provider 4", slug="provider-4"),
        )
        Provider.objects.bulk_create(providers)

        raw_notification = RawNotification.objects.create(
            subject="whatever", provider=providers[0], sender="whatever", source="whatever", raw="whatever 1"
        )
        circuit_maintenance = CircuitMaintenance.objects.create(
            name="UT-TEST-1", start_time="2020-10-04 10:00:00", end_time="2020-10-04 12:00:00"
        )
        ParsedNotification.objects.create(maintenance=circuit_maintenance, raw_notification=raw_notification, json="{}")

        raw_notification_2 = RawNotification.objects.create(
            subject="whatever", provider=providers[0], sender="whatever", source="whatever", raw="whatever 2"
        )
        circuit_maintenance_2 = CircuitMaintenance.objects.create(
            name="UT-TEST-2", start_time="2020-10-04 10:00:00", end_time="2020-10-04 12:00:00"
        )
        ParsedNotification.objects.create(
            maintenance=circuit_maintenance_2, raw_notification=raw_notification_2, json="{}"
        )
