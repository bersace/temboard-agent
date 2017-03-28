################
 temBoard Agent
################

| |CircleCI|

`temBoard <http://temboard.io/>`_ is a powerful management tool for PostgreSQL.

temBoard agent is a Python2 service designed to run along PostgreSQL, exposing a
REST API to implement various management tasks on PostgreSQL instance. See
http://temboard.io/ for the big picture.


===========
 Releasing
===========

Choose the next version according to `PEP 440
<https://www.python.org/dev/peps/pep-0440/#version-scheme>`_.

.. code-block

   git tag 1.1
   git push --tags
   make release


.. |CircleCI| image:: https://circleci.com/gh/dalibo/temboard-agent.svg?style=shield
   :target: https://circleci.com/gh/dalibo/temboard-agent
   :alt: CircleCI
