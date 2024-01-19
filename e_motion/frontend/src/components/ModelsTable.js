import * as React from 'react';
import Table from '@mui/material/Table';
import TableBody from '@mui/material/TableBody';
import TableCell from '@mui/material/TableCell';
import TableHead from '@mui/material/TableHead';
import TableRow from '@mui/material/TableRow';
import Title from './Title';
import Radio from '@mui/material/Radio';


/**
 * ModelsTable Component
 *
 * A table component for displaying a list of models associated with a project.
 *
 * @component
 * @example
 * // Example usage:
 * <ModelsTable data={modelsData} project_name="Project ABC" onSelect={handleSelect} />
 *
 * @param {Object} props - Component properties.
 * @param {Array} props.data - An array of model data.
 * @param {string} props.project_name - The name of the project.
 * @param {Function} props.onSelect - Callback function triggered when a model is selected.
 * @returns {JSX.Element} Rendered ModelsTable component.
 */
export default function ModelsTable(props) {
  const [selected, setSelected] = React.useState(0);

  const handleChange = (event) => {
    setSelected(event.target.value);
    props.onSelect(event.target.value);
  };

  return (
    <React.Fragment>
      <Title>Project: {props.project_name}</Title>
      <Table>
        <TableHead>
          <TableRow>
            <TableCell>Name</TableCell>
            <TableCell>Architecture</TableCell>
            <TableCell>Status</TableCell>
            <TableCell>mIoU</TableCell>
            <TableCell>top 1</TableCell>
            <TableCell>top 5</TableCell>
            <TableCell>Select</TableCell>
          </TableRow>
        </TableHead>
        <TableBody>
          {props.data.map((row) => (
            <TableRow key={row.id}>
              <TableCell>{row.name}</TableCell>
              <TableCell>{row.architecture}</TableCell>
              <TableCell>{row.status}</TableCell>
              <TableCell>{row.miou_score}</TableCell>
              <TableCell>{row.top1_score}</TableCell>
              <TableCell>{row.top5_score}</TableCell>
              <TableCell>{<Radio
                            checked={selected == row.id}
                            onChange={handleChange}
                            value={row.id}
                            name="radio-buttons"
                        />}
              </TableCell>
            </TableRow>
          ))}
        </TableBody>
      </Table>
    </React.Fragment>
  );
}
