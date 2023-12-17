import React from 'react';
import Typography from '@material-ui/core/Typography';
import './Footer.css';

const Footer: React.FC = () => {
  return (
    <footer className='footer'>
      <a
        href='https://www.neuralbridge.ai/'
        target='_blank'
        className='footer__company-name'
      >
        Neural Bridge
      </a>
      <div className='footer__links'>
        <a href='https://www.neuralbridge.ai/' className='footer__link'>
          About
        </a>
        <a href='https://www.neuralbridge.ai/' className='footer__link'>
          Contact
        </a>
        <a href='https://www.neuralbridge.ai/' className='footer__link'>
          Terms of Service
        </a>
        <a href='https://www.neuralbridge.ai/' className='footer__link'>
          Privacy Policy
        </a>
      </div>
      <Typography variant='body2' color='textSecondary' align='center'>
        © 2023 Neural Bridge. All rights reserved.
      </Typography>
    </footer>
  );
};

export default Footer;
