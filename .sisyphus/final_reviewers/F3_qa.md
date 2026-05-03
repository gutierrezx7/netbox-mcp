# F3 — QA Reviewer

Goal: Run end-to-end scenarios and verify user-visible behavior.

Test scenarios:

1. Create -> Read -> Update -> Delete flow for a safe test object
2. Global search returns expected items
3. Changelog entries recorded for create/update/delete

Commands (example harness):

  ./e2e/run_create_update_delete.sh --url $NETBOX_URL --token $NETBOX_TOKEN

Deliverables:
- Test logs, screenshots (if UI involved), and any failures with reproduction steps
