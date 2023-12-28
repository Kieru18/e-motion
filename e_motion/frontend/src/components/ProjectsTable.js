import * as React from 'react';
import Table from '@mui/material/Table';
import TableBody from '@mui/material/TableBody';
import TableCell from '@mui/material/TableCell';
import TableHead from '@mui/material/TableHead';
import TableRow from '@mui/material/TableRow';
import Title from './Title';

// Generate Data
function createData(id, name, description, date, size, status) {
  return { id, name, description, date, size, status };
}

const rows = [
  createData(
    0,
    'CIFAR',
    'object detection',
    '07.12.2023',
    'Small',
    'In progress',
  ),
];

function preventDefault(event) {
  event.preventDefault();
}

export default function ProjectsTable() {
  return (
    <React.Fragment>
      <Title>Your projects</Title>
      <Table size="small">
        <TableHead>
          <TableRow>
            <TableCell>Name</TableCell>
            <TableCell>Description</TableCell>
            <TableCell>Date</TableCell>
            <TableCell>Size</TableCell>
            <TableCell>Status</TableCell>
          </TableRow>
        </TableHead>
        <TableBody>
          {rows.map((row) => (
            <TableRow key={row.id}>
              <TableCell>{row.name}</TableCell>
              <TableCell>{row.description}</TableCell>
              <TableCell>{row.date}</TableCell>
              <TableCell>{row.size}</TableCell>
              <TableCell>{row.status}</TableCell>
            </TableRow>
          ))}
        </TableBody>
      </Table>
    </React.Fragment>
  );
}
