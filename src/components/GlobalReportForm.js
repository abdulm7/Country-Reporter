

import { useEffect } from 'react';
import { useState } from 'react';
import BeatLoader from 'react-spinners/BeatLoader'
// import Modal from 'react-modal';
import { Button, Dialog, FormControl, Select, MenuItem, InputLabel} from '@material-ui/core';

export default function GlobalReportForm() {

    // const [countries, setCountries] = useState([])
    const [loading, setLoading] = useState(true)
    const [selectedOption, setSelectedOption] = useState('');
    const [years, setYears]= useState([]);
    const [modalIsOpen, setModalIsOpen] = useState(false);
    const [subLoading, setSubLoading] = useState(false)

    const handleOptionChange = (event) => {
        setSelectedOption(event.target.value);
      };

    const handleSubmit = (e) => {
      e.preventDefault();

      if (selectedOption === ''){
        alert("ERROR: You must select a contry to submit!")
      }else{
        setSubLoading(true)
        let endpoint = "CreateGlobalReport?year=" + selectedOption
        fetch(process.env.REACT_APP_API + endpoint)
            .then(res => res.json())
            .then(data => {
                setSelectedOption('');
                closeModal();
                window.location.reload();
            }, [])
      }
    };

    const openModal = () => {
        setModalIsOpen(true);
    };

    const closeModal = () => {
        setModalIsOpen(false);
    };

    useEffect(() => {
        fetch(process.env.REACT_APP_API + 'GetYears')
        .then(res => res.json())
        .then(data => {
            setYears(data)
            setLoading(false)
        
    }, [])

  }, [])

  const modalStyles = {
    minWidth: 400, // Minimum width in pixels
    minHeight: 200, // Minimum height in pixels
  };

  return (



    <div>
        <Button variant="contained" color="primary" onClick={openModal}>Create Global Report</Button>

        <Dialog
            className='modal'
            open={modalIsOpen} 
            onClose={closeModal} 
            PaperProps={{
                style: modalStyles,
              }}
        >
            {loading ?

            <div className="db-table form">
                <BeatLoader color="#f50057" />
            </div>
            :

            subLoading ?

            <div className="db-table form">
                <BeatLoader color="#f50057" />
            </div>

            :
            <form className='db-table form-center form' onSubmit={handleSubmit}>
                <h4>Create Global Report</h4>
                <FormControl>
                    <InputLabel>Year</InputLabel>
                    <Select className='country-select' value={selectedOption} onChange={handleOptionChange}>
                        {Array.isArray(years) ? years.map((y) => (
                            <MenuItem key={y + "-key"} value={y}>{y}</MenuItem> 
                        ))
                    :
                        <MenuItem></MenuItem>
                    }
                    </Select>
                    <Button className='btn-sumbit' variant="contained" color="secondary" type='submit'>Submit</Button>
                </FormControl>
            </form>}
        </Dialog>
    </div>
  )
}