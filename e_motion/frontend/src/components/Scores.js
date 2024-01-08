import React, { useState } from "react";
import Table from '@mui/material/Table';
import TableBody from '@mui/material/TableBody';
import TableCell from '@mui/material/TableCell';
import TableContainer from '@mui/material/TableContainer';
import TableHead from '@mui/material/TableHead';
import TableRow from '@mui/material/TableRow';
import Paper from '@mui/material/Paper';


export default function Scores(props) {

    const data = props.data;

    return (
        <TableContainer component={Paper}>
            <Table aria-label="simple table">
                <TableHead>
                    <TableRow>
                        <TableCell>Metric</TableCell>
                        <TableCell align="right">Score</TableCell>
                    </TableRow>
                </TableHead>
                <TableBody>
                    <TableRow
                        key="miou"
                        sx={{ '&:last-child td, &:last-child th': { border: 0 } }}
                    >
                        <TableCell component="th" scope="row">Mean Intersection over Union (mIoU)</TableCell>
                        <TableCell align="right">{data["miou"]}</TableCell>
                    </TableRow>
                    <TableRow
                        key="top1"
                        sx={{ '&:last-child td, &:last-child th': { border: 0 } }}
                    >
                        <TableCell component="th" scope="row">Top 1 score</TableCell>
                        <TableCell align="right">{data["top1"]}</TableCell>
                    </TableRow>
                    <TableRow
                        key="top5"
                        sx={{ '&:last-child td, &:last-child th': { border: 0 } }}
                    >
                        <TableCell component="th" scope="row">Top 5 score</TableCell>
                        <TableCell align="right">{data["top5"]}</TableCell>
                    </TableRow>
                </TableBody>
            </Table>
        </TableContainer>
    );
}