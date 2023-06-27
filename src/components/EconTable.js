import { useEffect } from 'react';
import { useState } from 'react';
import BeatLoader from 'react-spinners/BeatLoader'

export default function EconTable() {
    const [records, setRecords] = useState([])
    const [gdpYears, setYears] = useState([])
    const [loading, setLoading] = useState(true)

    useEffect(() => {
        fetch('https://zrba2hfr19.execute-api.ca-central-1.amazonaws.com/default/DbRetrieve?table=econ')
        .then(res => res.json())
        .then(data => {
            setRecords(data['items'])
            setYears(data.years)
            console.log('testing')
            setLoading(false)
    })
  }, [])

  return(

    loading ?
    <div className="db-table">
        <BeatLoader color="#36d7b7" />
    </div>
    :
    <div class="db-table">
        <h3>GDP & Economic Table</h3>
        <table classNam = 'table' class="tableFixHead">
            <thead>
            <tr>
                <th key='country-h'>Country Name</th>
                <th key='currency-h'>Currency</th>
                {gdpYears.map((key)=>(
                    <th key={'gdp-' + key}>{key}</th>
                ))}
            </tr>
            </thead>
            <tbody>
            {
                records.map((record, i) => (
                <tr key = {i}>
                    <td key={'country-' + i}>{record.country}</td>
                    <td key={'currency-' + i}>{record.currency}</td>
                    {gdpYears.map((key) => record.gdp[key] !== undefined ?
                    <td key={'year-'+key+'-' + record.gdp[key]}>{record.gdp[key]}</td>:
                    <td></td>
                    )}
                </tr>
                ))
            }
            </tbody>
        </table>
    </div>
  )}
