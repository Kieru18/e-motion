Requirements
============

Business requirements
---------------------
- The tool generates annotations, based on already marked elements, for the remaining elements of the set.
- The tool has the ability to mark data and generate predictions if there are no base annotations, only a clean set.
- The system should allow configuring model training parameters and selecting architectures to provide flexibility for different project needs.

Usage requirements
------------------
- Possibility of continuing work with existing data sets.
- Speeding up data annotation 10 times compared to humans.

System requirements
-------------------
**Functional:**
- The user can add projects by clicking a button, after clicking it, the project is entered into the database and the log is sent.
- The user can add link to cloud storage where the data is stored.
- The user can visually select data in the form of bounding boxes.
- The user can assign a class to the selection.
- The user can choose from pretrained/basic ML models.
- The user can specify model hyperparameters by filling the form.
- The user can see the results of the model in the form of numerical values and charts in the dashboard.
- The user can download the generated annotations by pressing the appropriate button.

**Non-functional:**
- It is possible to serve at least 2 clients.
- It is possible to work with large datasets (more than 10000 images).
- It is possible to store annotations in JSON format.
