

import { useEffect } from 'react';
import { useState } from 'react';
import BeatLoader from 'react-spinners/BeatLoader'

export default function CountryReportForm() {

    const [countries, setCountries] = useState([])
    const [loading, setLoading] = useState(true)
    const [selectedOption, setSelectedOption] = useState('');
    
    const handleOptionChange = (event) => {
        setSelectedOption(event.target.value);
      };

      useEffect(() => {
    fetch('https://zrba2hfr19.execute-api.ca-central-1.amazonaws.com/default/JoinCountries')
    .then(res => res.json())
    .then(data => {
        setCountries(data)
        setLoading(false)
      
    })

  })

  return (

    loading ?
    <div className="db-table">
        <BeatLoader color="#36d7b7" />
    </div>
    :

    <div className='db-table'>
        <select value={selectedOption} onChange={handleOptionChange}>
            {countries.map((c) => (
                <option value={c}>{c}</option>
            ))}
        </select>
        {selectedOption && <p>You selected: {selectedOption}</p>}
    </div>
  )
}