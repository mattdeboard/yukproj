from yuk.models import *

def migrate_urls():
    for url in Url.objects.all():
        b = Item(user=url.user, date_created=url.date_created, 
                 last_updated=url.last_updated, 
                 privacy_mode=url.privacy_mode, url=url.url, 
                 displays=url.url_name, url_desc=url.url_desc,
                 item_type="bookmark")
        b.save()
        for tag in ur.tags.all():
            b.tags.add(tag)
        b.save()

    return "Done - Bookmarks"

def migrate_notes():
    for note in Note.objects.all():
        n = Item(user=note.user, date_created=note.date_created, 
                 last_updated=note.last_updated, privacy_mode=note.privacy_mode,
                 url=note.url, displays=note.title, description=note.notes, 
                 item_type="note")
    n.save()
    for tag in note.tags.all():
        n.tags.add(tag)
    n.save()

    return "Done - Notes"

def migrate_quotes():
    for quote in Quote.objects.all():
        n = Item(user=quote.user, date_created=quote.date_created, 
                 last_updated=quote.last_updated, 
                 privacy_mode=quote.privacy_mode, url=quote.url, 
                 displays=quote.title, description=quote.notes, 
                 item_type="quote")
    n.save()
    for tag in note.tags.all():
        n.tags.add(tag)
    n.save()

    return "Done - Notes"
    