public: yes

============
To-Do List
============

**In descending order by priority:**

1. *Implement private & public flags for all objects (RSS feeds, individual
   links, notes, etc.)* **3/5/11:** Done

2. *Implement `pinboard`_-like "Notes".* **3/6/11:** Done

3. *Implement "Quotes" - Model: two CharFields (quote, who said it), one URLField
   (link to source/twitter profile of source/etc.)* **3/6/11:** Done

4. *Improve landing page for new/unauthenticated users with better explanation of the service up front.* **Done**

5. User profiles for preferences/settings (change password, update email, etc.)

6. *Refactor database to incorporate multi-table inheritance. Urls, Notes and 
Quotes as child tables, and an "Item" table as parent.* **Done** 

.. _`pinboard`: http://pinboard.in
