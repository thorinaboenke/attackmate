.. _c2url_config:

============
c2url_config
============

``c2url_config`` stores settings for one or more c2url controllers. Each
controller is identified by a name. The first defined controller is used by
default when a command does not specify one explicitly. A playbook that defines
no ``c2url_config`` still works: an unconfigured ``default`` controller is used.

.. code-block:: yaml

   c2url_config:
     primary:
       token: shared-secret

Multiple controllers can be defined and selected per command via the
:confval:`connection` field (each listener must bind its own port):

.. code-block:: yaml

   c2url_config:
     primary:
       token: secret-1
     secondary:
       token: secret-2
       certificate: /path/cert.pem
       private_key: /path/key.pem

.. confval:: token

   Shared secret required from targets. If unset, no token is enforced.

   :type: str
   :default: None

.. confval:: certificate

   Path to a TLS certificate. Requires :confval:`private_key`; enables HTTPS.

   :type: str
   :default: None

.. confval:: private_key

   Path to the TLS private key. Requires :confval:`certificate`.

   :type: str
   :default: None

.. confval:: merge_stderr

   Merge the target's stderr into stdout.

   :type: bool
   :default: ``True``

.. confval:: upgrade_pty

   Attempt to upgrade the target shell to a PTY on connect.

   :type: bool
   :default: ``False``
