#!/usr/bin/env python
# Unlock any non-200'ish photo URLs for a state

import sys
import requests
from billy.core import db


def unlock(person):
    if not person.get("photo_url"):
        return

    if requests.get(person['photo_url']).status_code % 100 == 2:
        return

    # Right, we've got a photo_url, but it sucks. Let's go and unlock
    # and save this homie.

    locked = person.get('_locked_fields')
    if 'photo_url' not in locked:
        # We're not locked, so that's fine.
        return

    locked.remove("photo_url")
    person['_locked_fields'] = locked
    db.legislators.save(person)


def main(state):
    for _ in map(unlock, db.legislators.find({"abbr": state})):
        pass



if __name__ == "__main__":
    main(*sys.argv[1:])
