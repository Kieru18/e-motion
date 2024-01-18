.. js:module:: ProjectsTable

ProjectsTable Component
=======================

A table component for displaying a list of projects.

Example usage:
--------------

.. code-block:: jsx

   <ProjectsTable data={projectsData} onChange={handleProjectChange} />

Props
-----

- ``props``: Additional properties that can be passed to the ProjectsTable component.

  - ``data``: An array of project data.

  - ``onChange``: Callback function triggered when a project is clicked.

Returns
-------

- :literal:`JSX.Element` - Rendered ProjectsTable component.
