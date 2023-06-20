import { useEffect } from 'react';
import { useState } from 'react';

export default function EconTable() {
    const [column, setColumn] = useState([])
    const [records, setRecords] = useState([])
    const [gdpYears, setYears] = useState([])

      useEffect(() => {
    fetch('https://zrba2hfr19.execute-api.ca-central-1.amazonaws.com/default/DbRetrieve?table=econ')
    .then(res => res.json())
    .then(data => {
      setColumn(Object.keys(data[0]))
      setRecords(data)
      setYears(Object.keys(data[0].gdp))
      gdpYears[0] = "GDP/Year ".concat(gdpYears[0])
    })

    
  })

  return(
    <table classNam = 'table' class="tableFixHead">
        <thead>
          <tr>
            <th>Country</th>
            <th>Currency</th>
            {gdpYears.map((key)=>(
                  <th>{key}</th>
            ))}
          </tr>
        </thead>
        <tbody>
          {
            records.map((record, i) => (
              <tr key = {i}>



                <td>{record.country}</td>
                <td>{record.currency}</td>
                {Object.keys(record.gdp).map((key)=>(
                  <td>{record.gdp[key]}</td>
                ))}
              </tr>
            ))
          }
        </tbody>
      </table>
  )}
