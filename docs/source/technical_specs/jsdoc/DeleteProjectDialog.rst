.. js:module:: DeleteProjectDialog

DeleteProjectDialog Component
===============================

A dialog component for confirming the deletion of a project.

Example usage:
--------------

.. code-block:: jsx

   <DeleteProjectDialog projectId={123} close={() => console.log('Dialog closed')} />

Parameters
----------

- ``projectId`` (number): The ID of the project to be deleted.

- ``close`` (function): Callback function to close the parent dialog.

Returns
-------

- :literal:`JSX.Element` - Rendered DeleteProjectDialog component.
