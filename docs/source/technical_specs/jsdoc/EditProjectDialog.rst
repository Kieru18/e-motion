.. js:module:: EditProjectDialog

EditProjectDialog Component
===========================

A dialog component for editing project details.

Example usage:
--------------

.. code-block:: jsx

   <EditProjectDialog row={{ id: 1, title: 'Project 1', description: 'Description 1', label_studio_project: '1' }} onClose={() => console.log('Dialog closed')} />

Parameters
----------

- ``row`` (Object): The project details to be edited.

- ``onClose`` (function): Callback function to close the parent dialog.

Returns
-------

- :literal:`JSX.Element` - Rendered EditProjectDialog component.