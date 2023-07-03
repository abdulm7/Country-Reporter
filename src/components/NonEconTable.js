import { useEffect } from 'react';
import { useState } from 'react';
import BeatLoader from 'react-spinners/BeatLoader'

export default function NonEconTable() {
    const [records, setRecords] = useState([])
    const [popYears, setYears] = useState([])
    const [loading, setLoading] = useState(true)
    const removedChars = /["[\]]/g;

      useEffect(() => {
    fetch('https://zrba2hfr19.execute-api.ca-central-1.amazonaws.com/default/DbRetrieve?table=non-econ')
    .then(res => res.json())
    .then(data => {
      setRecords(data['items'])
      setYears(data.years)
      setLoading(false)
      
    }, [])

  })


  return(

    loading ?

    <BeatLoader color="#f50057" />
    :
    <div className="db-table">
        <h3>Population & Non-Economic Table</h3>
        <table className="table tableFixHead">
            
            <thead>
            <tr>
                <th key='country-h'>Country</th>
                <th key='capital-h'>Capital</th>
                <th key='iso3-h'>ISO3</th>
                <th key='area-h'>Area (km^2)</th>
                <th key='lang-h'>Languages</th>
                {popYears.map((key)=>(
                    <th key={key + '-h'}>{key}</th>
                ))}
            </tr>
            </thead>
            <tbody>
            {
                records.map((record, i) => (
                <tr key = {i}>

                    <td key={record.country + '-name'}>{record.country}</td>
                    <td key={record.country + '-capital'}>{record.capital}</td>
                    <td key={record.country + '-iso3'}>{record.aliases.iso3}</td>
                    <td key={record.country + '-area'}>{record.area}</td>
                    <td key={record.country + '-langs'}>{JSON.stringify(record.languages).replace(removedChars, "")}</td>
                    {popYears.map((key) => record.population[key] !== undefined ?
                        <td key={record.country + '-' + record.population[key] + '-' + key}>{record.population[key]}</td>:
                        <td key={'empty-' + key + '-'+ i}></td>
                    )}
                </tr>
                ))
            }
            </tbody>
        </table>
      </div>
  )}
