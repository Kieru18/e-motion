.. js:module:: CreateProjectDialog

CreateProjectDialog Component
=============================

A dialog component for creating a new project with title, description, and dataset URL.

Example usage:
--------------

.. code-block:: jsx

   <CreateProjectDialog onClose={(success) => console.log(`Project creation ${success ? 'succeeded' : 'failed'}`)} />

Params
------

- ``props``: The properties of the component.

  - ``onClose`` (function): Callback function called when the dialog is closed.

Returns
-------

- :literal:`JSX.Element` - Rendered CreateProjectDialog component.