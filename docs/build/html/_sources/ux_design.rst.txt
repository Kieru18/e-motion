User Experience Design
=======================

Actors & User Stories
-----------------------

Employee of a Data Labeling Company:
User Story 1:
As an employee of a data labeling company, I want to create and manage multiple annotation projects simultaneously, so that I can efficiently coordinate the labeling efforts of our team across different clients.
Acceptance Criteria:
The user can create a new annotation project.
The user can easily switch between existing annotation projects.
Each project allows the definition of unique data categories and attributes.
User Story 2:
As an employee of a data labeling company, I need the ability to easily switch between manual annotation and the ML model prediction correction mode, ensuring flexibility in our labeling workflows.
Acceptance Criteria:
The user can seamlessly switch between manual annotation and ML model prediction correction modes.
Changes made in one mode are reflected in the other to ensure consistency.
The transition between modes is intuitive and requires minimal effort.
User Story 3:
As an employee of a data labeling company, I want to be able to download annotated data in a standardized format, allowing seamless integration with our clients' machine learning pipelines.
Acceptance Criteria:
The user can download annotated data in a standardized format (e.g., JSON).
The downloaded data includes all relevant annotations and metadata.
The downloaded data is compatible with common machine learning frameworks.

Use Cases
---------
Use case diagram:

.. image:: images/use_case_diagram.png
  :width: 600

Activity Diagrams
-----------------

Activity diagram for usage of new ML model:

.. image:: images/activity_diagram1.png
  :width: 600

Activity diagram for usage of existing pretrained ML model for new data in dataset (existing projects):

.. image:: images/activity_diagram2.png
  :width: 600
