#!/usr/bin/env python3
"""
pull_funnel_truth.py — read-only funnel snapshot from your app database (Supabase or any
PostgREST-compatible endpoint).

Reads signups, contacts, and conversion truth so the Pipeline agent can reconcile the shared
CRM. READ-ONLY: this script never writes to the app database.

The column names below (email, segment, amount_cents, quota, etc.) are illustrative
placeholders, not a real schema. They exist to show what the script does with each table, not
to describe any specific product. Replace every DEFAULT_*_SELECT constant with your own app
database's actual column names before you rely on this in production.

WHAT A FORKER MUST SET (all via environment variables — never hard-code these in the script
or commit them anywhere):
    APP_DB_URL          Base REST URL of your app database (a PostgREST-compatible endpoint,
                          e.g. a Supabase project's REST URL)
    APP_DB_READ_KEY      A READ-ONLY credential. Use a custom Postgres role with SELECT-only
                          grants, or an anon key constrained by RLS policies that permit only
                          the SELECTs this script performs. Do NOT use a service-role / admin
                          key here — it bypasses row-level security and can write/delete,
                          which contradicts rules/03 and rules/04 ("the app database is
                          READ-ONLY from the bench") at the credential level, not just by
                          convention.
    APP_DB_TABLE_SIGNUPS         table name for signup/waitlist events (optional)
    APP_DB_TABLE_CONTACTS        table name for inbound contact/lead records (optional)
    APP_DB_TABLE_CONVERSIONS     table name for the conversion event (a purchase, an upgrade,
                                   an activation — whatever "converted" means for your
                                   product) — this is the same `<APP_DB_TABLE_CONVERSIONS>`
                                   token used throughout the rest of this repo (SETUP.md,
                                   rules/04-crm-conventions.md, sync/sync-contract.md,
                                   active-focus/focus.md, brain/offer.md) (optional)
    APP_DB_TABLE_PLANS           table name for plan/pricing definitions (optional)

This script reads exactly six environment variables: APP_DB_URL, APP_DB_READ_KEY (or the
legacy APP_DB_SERVICE_KEY fallback), APP_DB_TABLE_SIGNUPS, APP_DB_TABLE_CONTACTS,
APP_DB_TABLE_CONVERSIONS, and APP_DB_TABLE_PLANS.

Any table you don't set is simply skipped in the output — configure only the tables your
product actually has. See sync/field-map.md and sync/sync-contract.md for how these map onto
the shared CRM.

Usage:
    export APP_DB_URL="https://<your-project-ref>.example.com"
    export APP_DB_READ_KEY="<read-only key — never the service_role/admin key>"
    export APP_DB_TABLE_SIGNUPS="signups"
    export APP_DB_TABLE_CONTACTS="contacts"
    export APP_DB_TABLE_CONVERSIONS="conversions"
    export APP_DB_TABLE_PLANS="plans"
    python3 pull_funnel_truth.py > outputs/funnel_snapshot.json

    python3 pull_funnel_truth.py --help    # show this usage

This script is stdlib-only (urllib) so it runs anywhere Python 3 does, with no dependencies
to install. If your app database exposes a different API shape than PostgREST, treat this as
a template and adjust the `fetch()` calls rather than the overall structure.
"""
import argparse
import json
import os
import sys
import urllib.request
import urllib.error

# These column lists are placeholders that show the script's mechanics, not a real schema.
# Map every name below to your own app database's columns via the DEFAULT_*_SELECT constants
# or by passing your own `select=` value if you adapt fetch() calls directly.
DEFAULT_SIGNUP_SELECT = "id,email,name,segment,source,created_at,status"
DEFAULT_CONTACTS_SELECT = "id,email,name,company,status,source,campaign"
DEFAULT_CONVERSIONS_SELECT = "id,status,created_at,amount_cents"
DEFAULT_PLANS_SELECT = "id,name,amount_cents,interval,active,quota"


def fetch(base_url, key, table, select="*", extra=""):
    """Read-only GET against a PostgREST-style endpoint. Never issues a write."""
    url = f"{base_url}/rest/v1/{table}?select={select}{extra}"
    req = urllib.request.Request(
        url,
        headers={"apikey": key, "Authorization": f"Bearer {key}"},
        method="GET",
    )
    try:
        with urllib.request.urlopen(req) as r:
            return json.loads(r.read().decode())
    except urllib.error.HTTPError as e:
        print(f"ERROR: {table} fetch failed: HTTP {e.code} {e.reason}", file=sys.stderr)
        sys.exit(1)
    except urllib.error.URLError as e:
        print(f"ERROR: could not reach {base_url}: {e.reason}", file=sys.stderr)
        sys.exit(1)


def main():
    parser = argparse.ArgumentParser(
        description=(
            "Read-only funnel snapshot from your app database, for the LeadBench Pipeline "
            "agent to reconcile against the shared CRM. Never writes to the database."
        ),
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=__doc__,
    )
    parser.add_argument(
        "--out",
        default=None,
        help="Write JSON to this file instead of stdout.",
    )
    args = parser.parse_args()

    base_url = os.environ.get("APP_DB_URL", "").rstrip("/")
    # Prefer a read-only key; fall back to a legacy var name if that's what's set.
    key = os.environ.get("APP_DB_READ_KEY", "") or os.environ.get("APP_DB_SERVICE_KEY", "")

    if not base_url or not key:
        print(
            "ERROR: set APP_DB_URL and APP_DB_READ_KEY environment variables.\n"
            "Run with --help for the full list of variables this script reads.",
            file=sys.stderr,
        )
        sys.exit(1)

    signups_table = os.environ.get("APP_DB_TABLE_SIGNUPS")
    contacts_table = os.environ.get("APP_DB_TABLE_CONTACTS")
    conversions_table = os.environ.get("APP_DB_TABLE_CONVERSIONS")
    plans_table = os.environ.get("APP_DB_TABLE_PLANS")

    snapshot = {}

    if signups_table:
        snapshot["signups"] = fetch(
            base_url, key, signups_table, DEFAULT_SIGNUP_SELECT
        )
    if contacts_table:
        snapshot["contacts"] = fetch(base_url, key, contacts_table, DEFAULT_CONTACTS_SELECT)
    if conversions_table:
        snapshot["conversions"] = fetch(
            base_url,
            key,
            conversions_table,
            DEFAULT_CONVERSIONS_SELECT,
            "&status=eq.active",
        )
    if plans_table:
        snapshot["plans"] = fetch(base_url, key, plans_table, DEFAULT_PLANS_SELECT)

    if not snapshot:
        print(
            "WARNING: no APP_DB_TABLE_* variables set — nothing to fetch. "
            "See --help.",
            file=sys.stderr,
        )

    output = json.dumps(snapshot, indent=2, default=str)
    if args.out:
        with open(args.out, "w") as f:
            f.write(output)
    else:
        print(output)


if __name__ == "__main__":
    main()
