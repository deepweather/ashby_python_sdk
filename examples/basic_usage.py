#!/usr/bin/env python3
"""
Basic usage example for the Ashby SDK.

Make sure to set ASHBY_API_KEY in your environment or .env file.
"""

from ashby_sdk import AshbyClient, AshbyAuthError, AshbyAPIError


def main():
    # Initialize client
    try:
        client = AshbyClient()
    except AshbyAuthError as e:
        print(f"Authentication error: {e}")
        print("Make sure ASHBY_API_KEY is set in your environment")
        return 1

    # List open jobs
    print("Fetching open jobs...")
    jobs = client.jobs.list(status=["Open"])
    print(f"Found {len(jobs)} open jobs:\n")

    for job in jobs[:5]:
        print(f"  - {job.title} ({job.status})")

    if not jobs:
        print("No jobs found")
        return 0

    # Get applications for first job
    job = jobs[0]
    print(f"\nFetching applications for: {job.title}")
    applications = client.applications.list(job_id=job.id)
    print(f"Found {len(applications)} applications\n")

    # Show first few candidates
    for app in applications[:3]:
        print(f"  - {app.candidate_name}: {app.status}")

        # Get full candidate details
        candidate = client.candidates.get(app.candidate_id)
        print(f"    Email: {candidate.email}")
        print(f"    Has resume: {bool(candidate.resume_handle)}")
        print()

    # Demonstrate new features
    print("\n--- New SDK Features ---\n")

    # Sources
    sources = client.sources.list()
    print(f"Sources: {len(sources)} available")
    for src in sources[:3]:
        print(f"  - {src.name}")

    # Departments
    departments = client.departments.list()
    print(f"\nDepartments: {len(departments)} available")
    for dept in departments[:3]:
        print(f"  - {dept.name}")

    # Search for candidates
    print("\nSearching for candidates named 'John'...")
    results = client.candidates.search(name="John")
    print(f"Found {len(results)} candidates")

    # Archive reasons
    reasons = client.archive_reasons.list()
    print(f"\nArchive reasons: {len(reasons)} available")
    for reason in reasons[:3]:
        print(f"  - {reason.name}")

    return 0


if __name__ == "__main__":
    exit(main())
