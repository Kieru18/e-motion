.. js:module:: CreateModelDialog

CreateModelDialog Component
===========================

The component for creating a new machine learning model.

Example usage:
--------------

.. code-block:: jsx

   <CreateModelDialog projectId={projectId} projectTitle={projectTitle} onClose={handleClose} />

Params
------

- ``props``: The properties passed to the component.

- ``projectId`` (string): The ID of the project.

- ``projectTitle`` (string): The title of the project.

- ``onClose`` (function): The function to close the dialog.

Returns
-------

- :literal:`JSX.Element` - Rendered CreateModelDialog component.
