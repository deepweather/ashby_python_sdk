#!/usr/bin/env python3
"""
Example: Fetch questionnaire/form responses for candidates.

Demonstrates how to get form data from both sources:
- applicationFormSubmissions (newer candidates)
- surveySubmission (older candidates)
"""

import json
from ashby_sdk import AshbyClient


def get_all_form_data(client: AshbyClient, application_id: str, candidate_id: str) -> dict:
    """Get form responses from all sources for a candidate."""
    all_answers = {}

    # Source 1: Application form submissions (newer candidates)
    app = client.applications.get_with_forms(application_id)
    for form_sub in app.form_submissions:
        parsed = client.surveys.parse_submission(form_sub)
        all_answers.update(parsed.get("answers", {}))

    # Source 2: Survey submissions (older candidates)
    surveys = client.surveys.get_for_candidate(candidate_id)
    for survey in surveys:
        parsed = client.surveys.parse_submission(survey)
        all_answers.update(parsed.get("answers", {}))

    return all_answers


def main():
    client = AshbyClient()

    # Get first job with applications
    jobs = client.jobs.list(status=["Open"])
    if not jobs:
        print("No open jobs found")
        return 1

    for job in jobs:
        applications = client.applications.list(job_id=job.id)
        if applications:
            break
    else:
        print("No applications found")
        return 1

    print(f"Job: {job.title}")
    print(f"Applications: {len(applications)}\n")

    # Check first few candidates for form data
    found_data = False
    for app in applications[:10]:
        answers = get_all_form_data(client, app.id, app.candidate_id)

        if answers:
            print(f"Candidate: {app.candidate_name}")
            print("-" * 50)
            for question, answer in list(answers.items())[:5]:
                answer_str = str(answer)[:60] + "..." if len(str(answer)) > 60 else str(answer)
                print(f"Q: {question}")
                print(f"A: {answer_str}\n")
            found_data = True
            break

    if not found_data:
        print("No questionnaire responses found in first 10 candidates")

    return 0


if __name__ == "__main__":
    exit(main())
