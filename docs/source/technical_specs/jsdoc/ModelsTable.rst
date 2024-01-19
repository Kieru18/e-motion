.. js:module:: ModelsTable

ModelsTable Component
=====================

A table component for displaying a list of models associated with a project.

Example usage:
--------------

.. code-block:: jsx

   <ModelsTable data={modelsData} project_name="Project ABC" onSelect={handleSelect} />

Props
-----

- ``props``: Additional properties that can be passed to the ModelsTable component.

  - ``data``: An array of model data.

  - ``project_name``: The name of the project.

  - ``onSelect``: Callback function triggered when a model is selected.

Returns
-------

- :literal:`JSX.Element` - Rendered ModelsTable component.