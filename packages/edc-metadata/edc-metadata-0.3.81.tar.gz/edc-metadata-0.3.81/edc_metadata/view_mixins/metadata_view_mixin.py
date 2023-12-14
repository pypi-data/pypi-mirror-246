from __future__ import annotations

from typing import TYPE_CHECKING, Type

from django.apps import apps as django_apps
from django.contrib import messages
from django.core.exceptions import ObjectDoesNotExist
from django.utils.translation import gettext as _
from edc_appointment.constants import IN_PROGRESS_APPT
from edc_subject_model_wrappers import CrfModelWrapper, RequisitionModelWrapper

from ..constants import CRF, KEYED, NOT_REQUIRED, REQUIRED, REQUISITION
from ..metadata_wrappers import CrfMetadataWrappers, RequisitionMetadataWrappers
from ..utils import refresh_metadata_for_timepoint

if TYPE_CHECKING:
    from edc_lab.models import Panel


class MetadataViewError(Exception):
    pass


class MetadataViewMixin:
    crf_model_wrapper_cls: CrfModelWrapper = CrfModelWrapper
    requisition_model_wrapper_cls: RequisitionModelWrapper = RequisitionModelWrapper
    crf_metadata_wrappers_cls: CrfMetadataWrappers = CrfMetadataWrappers
    requisition_metadata_wrappers_cls: RequisitionMetadataWrappers = (
        RequisitionMetadataWrappers
    )
    panel_model: str = "edc_lab.panel"

    metadata_show_status: list[str] = [REQUIRED, KEYED]

    def get(self, request, *args, **kwargs):
        try:
            referrer = request.headers.get("Referer")
        except TypeError:
            pass
        else:
            if (
                referrer
                and kwargs.get("appointment")
                and "subject_review_listboard" in referrer
            ):
                self.appointment_id = kwargs.get("appointment")
                self.refresh_metadata_for_timepoint()
        return super().get(request, *args, **kwargs)

    def get_context_data(self, **kwargs) -> dict:
        context = super().get_context_data(**kwargs)
        context.update(metadata_show_status=self.metadata_show_status)
        if self.appointment:
            if self.appointment.appt_status != IN_PROGRESS_APPT:
                message = _(
                    'You have selected an appointment that is no longer "in progress". '
                    "Refer to the schedule for the appointment that is "
                    'currently "in progress".'
                )
                self.message_user(message, level=messages.WARNING)

            crf_model_wrappers = self.get_crf_model_wrappers()
            try:
                report_datetime = self.appointment.related_visit.report_datetime
            except AttributeError:
                pass
            else:
                context.update(
                    report_datetime=report_datetime,
                    crfs=crf_model_wrappers,
                    requisitions=self.get_requisition_model_wrapper(),
                    NOT_REQUIRED=NOT_REQUIRED,
                    REQUIRED=REQUIRED,
                    KEYED=KEYED,
                )
        return context

    def refresh_metadata_for_timepoint(self) -> None:
        """Save related visit model instance to run metadata update."""
        refresh_metadata_for_timepoint(self.appointment)

    def get_crf_model_wrappers(self) -> list[CrfModelWrapper]:
        """Returns a list of model wrappers.

        Gets each CrfMetadata instance, validates the entry status and wraps
        in a model wrapper.
        """
        model_wrappers = []
        crf_metadata_wrappers = self.crf_metadata_wrappers_cls(appointment=self.appointment)
        for metadata_wrapper in crf_metadata_wrappers.objects:
            if not metadata_wrapper.source_model_obj:
                metadata_wrapper.source_model_obj = metadata_wrapper.source_model_cls(
                    **{
                        metadata_wrapper.source_model_cls.related_visit_model_attr(): (
                            metadata_wrapper.visit
                        )
                    }
                )
            metadata_wrapper.metadata_obj.object = self.crf_model_wrapper_cls(
                model_obj=metadata_wrapper.source_model_obj,
                model=metadata_wrapper.metadata_obj.model,
                key=CRF,
                request=self.request,
            )
            model_wrappers.append(metadata_wrapper.metadata_obj)
        return [
            model_wrapper
            for model_wrapper in model_wrappers
            if model_wrapper.entry_status in self.metadata_show_status
        ]

    def get_requisition_model_wrapper(self) -> list[RequisitionModelWrapper]:
        """Returns a list of model wrappers."""
        model_wrappers = []
        requisition_metadata_wrappers = self.requisition_metadata_wrappers_cls(
            appointment=self.appointment
        )
        for metadata_wrapper in requisition_metadata_wrappers.objects:
            if not metadata_wrapper.source_model_obj:
                panel = self.get_panel(metadata_wrapper)
                metadata_wrapper.source_model_obj = metadata_wrapper.source_model_cls(
                    **{
                        metadata_wrapper.source_model_cls.related_visit_model_attr(): (
                            metadata_wrapper.visit
                        ),
                        "panel": panel,
                    }
                )
            metadata_wrapper.metadata_obj.object = self.requisition_model_wrapper_cls(
                model_obj=metadata_wrapper.source_model_obj,
                model=metadata_wrapper.metadata_obj.model,
                key=REQUISITION,
                request=self.request,
            )
            model_wrappers.append(metadata_wrapper.metadata_obj)
        return [
            model_wrapper
            for model_wrapper in model_wrappers
            if model_wrapper.entry_status in self.metadata_show_status
        ]

    def get_panel(self, metadata_wrapper=None) -> Panel:
        try:
            panel = self.panel_model_cls.objects.get(name=metadata_wrapper.panel_name)
        except ObjectDoesNotExist as e:
            raise MetadataViewError(
                f"{e} Got panel name '{metadata_wrapper.panel_name}'. "
                f"See {metadata_wrapper}."
            )
        return panel

    @property
    def panel_model_cls(self) -> Type[Panel]:
        return django_apps.get_model(self.panel_model)
