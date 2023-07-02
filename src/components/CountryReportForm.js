

import { useEffect } from 'react';
import { useState } from 'react';
import BeatLoader from 'react-spinners/BeatLoader'
// import Modal from 'react-modal';
import { Button, Dialog, FormControl, Select, MenuItem, InputLabel} from '@material-ui/core';

export default function CountryReportForm() {

    // const [countries, setCountries] = useState([])
    const [loading, setLoading] = useState(true)
    const [selectedOption, setSelectedOption] = useState('');
    const [countries,setCountries]= useState([]);
    const [modalIsOpen, setModalIsOpen] = useState(false);

    const handleOptionChange = (event) => {
        setSelectedOption(event.target.value);
      };

    const handleSubmit = (e) => {
      e.preventDefault();
      // Perform API call or other form submission logic
      // need to make corrections for backend

      if(selectedOption === ''){
        alert("ERROR: You must select a country to submit!")
      }else{
        setSelectedOption('');
        closeModal();
        window.location.reload();
      }
    };

    const openModal = () => {
        setModalIsOpen(true);
    };

    const closeModal = () => {
        setModalIsOpen(false);
    };

    useEffect(() => {
        fetch('https://zrba2hfr19.execute-api.ca-central-1.amazonaws.com/default/JoinCountries')
        .then(res => res.json())
        .then(data => {
            setCountries(data)
            // setSelectedOption(data[0])
            setLoading(false)
        
    }, [])

  })

  const modalStyles = {
    minWidth: 400, // Minimum width in pixels
    minHeight: 200, // Minimum height in pixels
  };

  return (


    <div>
        <Button variant="contained" color="primary" onClick={openModal}>Create Country Report</Button>

        <Dialog
            className='modal'
            open={modalIsOpen} 
            onClose={closeModal} 
            contentLabel="Form Modal"
            PaperProps={{
                style: modalStyles,
              }}
        >
            {loading ?

            <div className="db-table form">
                <BeatLoader color="#36d7b7" />
            </div>
            :

            <form className='db-table form-center form' onSubmit={handleSubmit}>
                <h4>Create Country Report</h4>
                <FormControl>
                    <InputLabel>Country</InputLabel>
                    <Select className='country-select' value={selectedOption} onChange={handleOptionChange}>
                        <MenuItem  value= "" >
                            Select a Country
                        </MenuItem >
                        {countries.map((c) => (
                            <MenuItem key={c + "-key"} value={c}>{c}</MenuItem>
                        ))}
                    </Select>
                    <Button className='btn-sumbit' variant="contained" color="secondary" type='submit'>Submit</Button>
                </FormControl>
            </form>}
        </Dialog>
    </div>
  )
}