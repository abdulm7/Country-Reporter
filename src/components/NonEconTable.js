import { useEffect } from 'react';
import { useState } from 'react';

export default function NonEconTable() {
    const [column, setColumn] = useState([])
    const [records, setRecords] = useState([])
    const [gdpYears, setYears] = useState([])

      useEffect(() => {
    fetch('https://zrba2hfr19.execute-api.ca-central-1.amazonaws.com/default/DbRetrieve?table=non-econ')
    .then(res => res.json())
    .then(data => {
      setColumn(Object.keys(data[0]))
      setRecords(data)
      setYears(Object.keys(data[0].gdp))
    })
  })

  return(
    <table classNam = 'table'>
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
