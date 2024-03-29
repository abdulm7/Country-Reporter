import { useEffect } from 'react';
import { useState } from 'react';
import BeatLoader from 'react-spinners/BeatLoader'

export default function EconTable() {
    const [records, setRecords] = useState([])
    const [gdpYears, setYears] = useState([])
    const [loading, setLoading] = useState(true)

    // console.log(process.env.REACT_APP_API + 'gettable?table=econ');

    useEffect(() => {
        fetch(process.env.REACT_APP_API + 'gettable&table=econ')
        .then(res => res.json())
        .then(data => {
            console.log(data)
            setRecords(data['items'])
            setYears(data.years)
            setLoading(false)
    })
  }, [])

  return(

    loading ?
    <div className="db-table">
        <BeatLoader color="#f50057" />
    </div>
    :
    <div className="db-table">
        <h3>GDP & Economic Table</h3>
        <table className="table tableFixHead">
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
                    <td key={'year-'+ key + '-' + record.gdp[key]}>{record.gdp[key]}</td>:
                    <td key={'empty-' + key + '-' + i}></td>
                    )}
                </tr>
                ))
            }
            </tbody>
        </table>
    </div>
  )}
