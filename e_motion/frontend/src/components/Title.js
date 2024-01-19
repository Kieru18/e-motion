import * as React from 'react';
import PropTypes from 'prop-types';
import Typography from '@mui/material/Typography';

/**
 * Title Component
 *
 * A reusable component for rendering a title with specified styling.
 *
 * @component
 * @example
 * // Example usage:
 * <Title>Title Text</Title>
 *
 * @param {Object} props - The properties passed to the component.
 * @param {ReactNode} props.children - The content to be displayed as the title.
 *
 * @returns {JSX.Element} Rendered Title component.
 */
function Title(props) {
  return (
    <Typography component="h2" variant="h6" color="primary" gutterBottom>
      {props.children}
    </Typography>
  );
}

Title.propTypes = {
  children: PropTypes.node,
};

export default Title;