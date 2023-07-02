import React, { useEffect, useState } from 'react';
import CountryReportForm from './CountryReportForm';
import GlobalReportForm from './GlobalReportForm';
import BeatLoader from 'react-spinners/BeatLoader'
import { Button } from '@material-ui/core';

function ReportTables() {

    const [countryReports, setCountryReports] = useState([])
    const [globalReports, setGlobalReports] = useState([])
    const [loading ,setLoading] = useState([])
    const [modalIsOpen, setModalIsOpen] = useState(false);


    useEffect(() => {
        fetch('https://zrba2hfr19.execute-api.ca-central-1.amazonaws.com/default/GetReports')
        .then(res => res.json())
        .then(data => {
            setCountryReports(data['country'])
            setGlobalReports(data['global'])
            setLoading(false)
        })

    }, [])

    const openModal = () => {
        setModalIsOpen(true);
    };

    const closeModal = () => {
        setModalIsOpen(false);
    };

    return (
        <div className="tables-container">
            <div className="table-wrapper">
                <div className="table-buttons table-buttons-center">
                    <CountryReportForm />
                </div>
                <h5>Country Reports</h5>
                <table className='report-table'>

                    <thead>
                        <tr>
                            <th>Report Name</th>
                            <th>Creation Date</th>
                            <th>Report</th>
                        </tr>
                    </thead>
                    {loading ?
                            // <div className="db-table">
                                <BeatLoader color="#36d7b7" />
                        :
                            countryReports.length === 0 ?

                                <h6>No Country Reports Have Been Generated</h6>
                            :

                            <tbody>
                                    {
                                    countryReports.map((report, i) => (
                                        <tr key = {i}> 
                                            <td key={report.file}>{report['file']}</td>
                                            <td key={report.file + '-date'}>{report['creation-date']}</td>
                                            <td key={report.file + '-report'}><Button 
                                                                                variant="contained" 
                                                                                color='red' 
                                                                                onClick={openModal}
                                                                                >View</Button> </td>
                                        
                                        </tr>
                                    ))
                                    }
                            </tbody>
                    }
                </table>
            </div>
            <div className="table-wrapper">
                <div className="table-buttons table-buttons-center">
                    <GlobalReportForm />
                </div>
                <h5>Global Reports</h5>
                <table className='report-table'>
                    <thead>
                        <tr>
                            <th>Report Name</th>
                            <th>Creation Date</th>
                            <th>Report</th>
                        </tr>
                    </thead>
                    {loading ?
                            <div className="db-table">
                                <BeatLoader color="#36d7b7" />
                            </div>
                        :
                            globalReports.length === 0 ?

                                <h6>No Global Reports Have Been Generated</h6>
                            :

                            <tbody>
                                <tr>
                                    <td>Testing 1</td>
                                    <td>Testing 2</td>
                                    <td>Testing 3</td>
                                </tr>
                            </tbody>
                    }

                </table>
            </div>
        </div>
    );
}

export default ReportTables;