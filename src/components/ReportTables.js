import React, { useEffect, useState } from 'react';
import CountryReportForm from './CountryReportForm';
import GlobalReportForm from './GlobalReportForm';
import BeatLoader from 'react-spinners/BeatLoader'
import { Button, Dialog, DialogActions} from '@material-ui/core';

function ReportTables() {

    const [countryReports, setCountryReports] = useState([])
    const [globalReports, setGlobalReports] = useState([])
    const [loading, setLoading] = useState([])
    const [modalIsOpen, setModalIsOpen] = useState(false);
    const [modalBody, setModalBody] = useState('')
    const [modalTitle, setModalTitle] = useState ('')
    const [countryDelete, setCountryDelete] = useState(false)
    const [globalDelete, setGlobalDelete] = useState(false)


    useEffect(() => {
        fetch(process.env.REACT_APP_API + 'GetReports')
            .then(res => res.json())
            .then(data => {
                setCountryReports(data['country'])
                setGlobalReports(data['global'])
                setLoading(false)
            }, [])

    }, [])

    function openModal(report, title) {
        // Implement logic to open the modal with the parameter

        const decodedString = decodeURIComponent(report)
            .replace(/\\n/g, '\n')   // Replace \n with line break
            .replace(/\\t/g, '\t')
            .replace(/"/g, '');
        setModalBody(decodedString)
        setModalTitle(title)
        setModalIsOpen(true)
      }

    function deleteReport(fname, bucket){
        if (bucket === 'cr-country-reports'){
            setCountryDelete(true)
        }else{
            setGlobalDelete(true)
        }
        fetch(process.env.REACT_APP_API + '/DeleteReport?bucket=' + bucket + '&object=' + fname)
        .then(res => res.json())
        .then(data => {
            alert(data)
            window.location.reload();
        })
    }

    const closeModal = () => {
        setModalIsOpen(false);
    };

    const modalStyles = {
        minWidth: 1000, // Minimum width in pixels
        minHeight: 300, // Minimum height in pixels
        display: 'block',
        alignItems: 'center',
        justifyContent: 'center',
        overflow: 'hidden'
      };

      const deleteBtn = {
        backgroundColor: '#D30000',
        color: 'white',
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
                            <th>Delete</th>
                        </tr>
                    </thead>
                    {loading ?
                        // <div className="db-table">
                        <tbody>
                            <tr>
                                <td colSpan="4">

                                    <div className='db-table'> <BeatLoader color="#f50057" /></div>
                                </td>
                            </tr>
                        </tbody>
                        :
                        countryReports.length === 0 ?
                            <tbody>
                                <tr>
                                    <td colSpan="4">
                                        <h6>No Country Reports Have Been Generated</h6>
                                    </td>
                                </tr>
                            </tbody>
                            :

                            <tbody>
                                {
                                    countryDelete ?
                                        <tr>
                                            <td colSpan="4">
            
                                                <div className='db-table'> <BeatLoader color="#f50057" /></div>
                                            </td>
                                        </tr>
                                    :
                                    countryReports.map((report, i) => (
                                        <tr key={i}>
                                            <td key={report.file}>{report['file']}</td>
                                            <td key={report.file + '-date'}>{report['creation-date']}</td>
                                            <td key={report.file + '-report'}><Button
                                                variant="contained"
                                                color='default'
                                                onClick={() => openModal(report.body, report.file)}
                                            >View</Button> </td>
                                            <td key={report.file + '-report'}><Button
                                                variant="contained"
                                                style={deleteBtn}
                                                onClick={() => deleteReport(report.file, 'cr-country-reports')}
                                            >Delete</Button> </td>

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
                            <th>Delete</th>
                        </tr>
                    </thead>
                    {loading ?
                        <tbody>
                            <tr>
                                <td colSpan="4">

                                    <div className='db-table'> <BeatLoader color="#f50057" /></div>
                                </td>
                            </tr>
                        </tbody>
                        :
                        globalReports.length === 0 ?
                            <tbody>
                                <tr>
                                    <td colSpan="4">
                                        <h6>No Global Reports Have Been Generated</h6>
                                    </td>
                                </tr>
                            </tbody>
                            :

                            <tbody>
                                {
                                    globalDelete ?
                                        <tr>
                                            <td colSpan="4">
            
                                                <div className='db-table'> <BeatLoader color="#f50057" /></div>
                                            </td>
                                        </tr>
                                    :
                                    globalReports.map((report, i) => (
                                        <tr key={i}>
                                            <td key={report.file}>{report['file']}</td>
                                            <td key={report.file + '-date'}>{report['creation-date']}</td>
                                            <td key={report.file + '-report'}><Button
                                                variant="contained"
                                                color='default'
                                                onClick={() => openModal(report.body, report.file)}
                                            >View</Button> 
                                            </td>
                                            <td key={report.file + '-report'}><Button
                                                variant="contained"
                                                style={deleteBtn}
                                                onClick={() => deleteReport(report.file, 'cr-global-reports')}
                                            >Delete</Button> 
                                            </td>

                                        </tr>
                                    ))
                                }
                            </tbody>
                    }

                </table>

            </div>

            <Dialog
                    className='report-modal'
                    open={modalIsOpen} 
                    onClose={closeModal} 
                    PaperProps={{
                        style: modalStyles,
                    }}
                    
                >
                    <div className="modalTitle">
                        <h4>{modalTitle}</h4>
                    </div>
                        <div className='report-div'>
                            <pre>{modalBody}</pre>
                        </div>

                    <DialogActions>
                        <Button className="modalCloseButton" colour="secondary" onClick={closeModal} color="primary">
                            Close
                        </Button>
                        {/* Additional actions or buttons */}
                    </DialogActions>
                </Dialog>
        </div>
    );
}

export default ReportTables;