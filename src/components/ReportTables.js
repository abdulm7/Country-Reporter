import React from 'react';
import CountryReportForm from './CountryReportForm';
import GlobalReportForm from './GlobalReportForm';

function ReportTables() {
  return (
    <div className="tables-container">
      <div className="table-wrapper">
        <div className="table-buttons table-buttons-center">
          <CountryReportForm/>
        </div>
        <h5>Country Reports</h5>
        <table>
            
          <thead>
            <tr>
              <th>Report Name</th>
              <th>Creation Date</th>
              <th>View</th>
            </tr>
          </thead>
          <tbody>
            {/* Table 1 rows */}
          </tbody>
        </table>
      </div>
      <div className="table-wrapper">
        <div className="table-buttons table-buttons-center">
          <GlobalReportForm/>
        </div>
        <h5>Global Reports</h5>
        <table>
          <thead>
            <tr>
              <th>Report Name</th>
              <th>Creation Date</th>
              <th>View</th>
            </tr>
          </thead>
          <tbody>
            {/* Table 2 rows */}
          </tbody>
        </table>
      </div>
    </div>
  );
}

export default ReportTables;