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
        <table>
          <thead>
            <tr>
              <th>Table 1 Header 1</th>
              <th>Table 1 Header 2</th>
              <th>Table 1 Header 3</th>
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
        <table>
          <thead>
            <tr>
              <th>Table 2 Header 1</th>
              <th>Table 2 Header 2</th>
              <th>Table 2 Header 3</th>
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