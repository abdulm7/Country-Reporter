import { useEffect } from 'react';
import { useState } from 'react';
import BeatLoader from 'react-spinners/BeatLoader'

export default function NonEconTable() {
    const [records, setRecords] = useState([])
    const [popYears, setYears] = useState([])
    const [loading, setLoading] = useState(true)

      useEffect(() => {
    fetch('https://zrba2hfr19.execute-api.ca-central-1.amazonaws.com/default/DbRetrieve?table=non-econ')
    .then(res => res.json())
    .then(data => {
      setRecords(data['items'])
      setYears(data.years)
      setLoading(false)
      
    })

  })


  return(

    loading ?

    <BeatLoader color="#36d7b7" />
    :
    <div class="db-table">
        <h3>Population & Non-Economic Table</h3>
        <table classNam = 'table' class="tableFixHead">
            
            <thead>
            <tr>
                <th>Country</th>
                <th>Capital</th>
                <th>ISO3</th>
                <th>Area (km^2)</th>
                <th>Languages</th>
                {popYears.map((key)=>(
                    <th>{key}</th>
                ))}
            </tr>
            </thead>
            <tbody>
            {
                records.map((record, i) => (
                <tr key = {i}>

                    <td>{record.country}</td>
                    <td>{record.capital}</td>
                    <td>{record.aliases.iso3}</td>
                    <td>{record.area}</td>
                    <td>{JSON.stringify(record.languages)}</td>
                    {popYears.map((key) => record.population[key] !== undefined ?
                        <td>{record.population[key]}</td>:
                        <td></td>
                    )}
                </tr>
                ))
            }
            </tbody>
        </table>
      </div>
  )}
