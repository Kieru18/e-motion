import * as React from 'react';
import Table from '@mui/material/Table';
import TableBody from '@mui/material/TableBody';
import TableCell from '@mui/material/TableCell';
import TableHead from '@mui/material/TableHead';
import TableRow from '@mui/material/TableRow';
import Title from './Title';


function preventDefault(event) {
  event.preventDefault();
}

/**
 * ProjectsTable Component
 *
 * A table component for displaying a list of projects.
 *
 * @component
 * @example
 * // Example usage:
 * <ProjectsTable data={projectsData} onChange={handleProjectChange} />
 *
 * @param {Object} props - Component properties.
 * @param {Array} props.data - An array of project data.
 * @param {Function} props.onChange - Callback function triggered when a project is clicked.
 * @returns {JSX.Element} Rendered ProjectsTable component.
 */
export default function ProjectsTable(props) {

  const handleClick = (row) => {
    props.onChange(row);
  };

  return (
    <React.Fragment>
      <Title>Your Projects</Title>
      <Table>
        <TableHead>
          <TableRow>
            <TableCell>Name</TableCell>
            <TableCell>Description</TableCell>
            <TableCell>Dataset URL</TableCell>
          </TableRow>
        </TableHead>
        <TableBody>
          {props.data.map((row) => (
            <TableRow key={row.id} onClick={() => handleClick(row)} hover>
              <TableCell>{row.title}</TableCell>
              <TableCell>{row.description}</TableCell>
              <TableCell>{row.dataset_url}</TableCell>
            </TableRow>
          ))}
        </TableBody>
      </Table>
    </React.Fragment>
  );
}
