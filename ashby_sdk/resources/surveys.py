"""Surveys/questionnaires API resource."""

from __future__ import annotations

from .base import BaseResource


class SurveysResource(BaseResource):
    """API resource for survey/questionnaire submissions."""

    def list(
        self,
        survey_type: str = "Questionnaire",
        limit: int = 100,
    ) -> list[dict]:
        """
        List all survey submissions of a given type.

        Args:
            survey_type: Type of survey (default "Questionnaire")
            limit: Results per page (default 100)

        Returns:
            List of survey submission dicts
        """
        return list(self._paginate(
            "surveySubmission.list",
            {"surveyType": survey_type},
            limit
        ))

    def get_for_candidate(
        self,
        candidate_id: str,
        survey_type: str = "Questionnaire",
    ) -> list[dict]:
        """
        Get all survey submissions for a specific candidate.

        Args:
            candidate_id: The candidate ID
            survey_type: Type of survey (default "Questionnaire")

        Returns:
            List of survey submissions for this candidate
        """
        all_surveys = self.list(survey_type=survey_type)
        return [s for s in all_surveys if s.get("candidateId") == candidate_id]

    def parse_submission(self, submission: dict) -> dict:
        """
        Parse a survey or application form submission into a readable format.

        Works for both surveySubmission and applicationFormSubmissions data.

        Args:
            submission: Raw submission dict (from survey or application form)

        Returns:
            Dict with field titles mapped to values
        """
        # Build field ID -> title mapping
        field_map = {}
        form_def = submission.get("formDefinition", {})
        for section in form_def.get("sections", []):
            for field_def in section.get("fields", []):
                field = field_def.get("field", {})
                field_id = field.get("id")
                field_title = field.get("title")
                field_path = field.get("path", "")
                if field_id:
                    field_map[field_id] = field_title
                if field_path:
                    field_map[field_path] = field_title

        # Map submitted values to titles
        result = {
            "submitted_at": submission.get("submittedAt"),
            "candidate_id": submission.get("candidateId"),
            "application_id": submission.get("applicationId"),
            "survey_type": submission.get("surveyType"),
            "form_id": submission.get("id"),
            "answers": {},
        }

        # System fields to skip (these are basic info, not questionnaire answers)
        skip_fields = {
            "_systemfield_resume",
            "_systemfield_pre_parsed_resume",
            "_systemfield_name",
            "_systemfield_email",
            "_systemfield_phone",
        }

        submitted = submission.get("submittedValues", {})
        for field_key, value in submitted.items():
            title = field_map.get(field_key, field_key)

            # Skip system fields that contain basic candidate info
            if field_key in skip_fields:
                continue
            if field_key.startswith("_systemfield_") and field_key not in field_map:
                continue

            # Format value
            if isinstance(value, dict):
                if "text" in value:
                    value = value.get("text")
                elif "name" in value:
                    value = value.get("name")
            elif isinstance(value, bool):
                value = "Yes" if value else "No"
            elif isinstance(value, list):
                value = ", ".join(
                    str(v.get("name", v) if isinstance(v, dict) else v) for v in value
                )

            result["answers"][title] = value

        return result
