.. _c2url:

=====
c2url
=====

Control a c2url HTTP shell controller. The listener and session commands share
one running controller per connection: ``type: c2url`` drives the controller
lifecycle, ``type: c2url-session`` runs commands on connected targets.

.. note::

   To configure a controller (token, TLS, stderr handling), see
   :ref:`c2url_config`. The listener runs in c2url's own background threads, so
   ``listen`` returns immediately and targets register while the playbook
   continues.

.. confval:: connection

   Name of the c2url connection to use, as defined in :ref:`c2url_config`.
   If omitted, the first configured connection is used (or an unconfigured
   ``default`` controller if none are defined).

   :type: str

listen
------

Start the HTTP listener. Returns as soon as the listener thread is running.

.. code-block:: yaml

   commands:
     - type: c2url
       cmd: listen
       host: 0.0.0.0
       port: 8080

.. confval:: host

   Interface to bind the listener to.

   :type: str
   :default: ``0.0.0.0``

.. confval:: port

   Port to bind the listener to.

   :type: int
   :default: ``8080``

wait_for_session
----------------

Block until a target connects back, then return its label and id. Fails with a
timeout if no target connects in time.

.. code-block:: yaml

   commands:
     - type: c2url
       cmd: wait_for_session
       timeout: 30

.. confval:: timeout

   Seconds to wait for a session before failing.

   :type: int
   :default: ``30``

stop
----

Stop the listener and close its sessions.

.. code-block:: yaml

   commands:
     - type: c2url
       cmd: stop

c2url-session
-------------

Run a shell command on a connected target. ``cmd`` holds the command to run.
If ``session`` is omitted, the single connected session is used.

.. code-block:: yaml

   commands:
     - type: c2url-session
       cmd: id
       session: s1

.. confval:: session

   Target session, by label (``s1``), number, or UUID. Omit to use the only
   connected session.

   :type: str
   :default: None

.. confval:: timeout

   Seconds to wait for the command to complete.

   :type: int
   :default: ``30``
