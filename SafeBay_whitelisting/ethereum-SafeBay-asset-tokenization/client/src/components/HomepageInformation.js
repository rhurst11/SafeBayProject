import React from 'react';

// MaterialUI imports
import Container from '@material-ui/core/Container';
import Grid from '@material-ui/core/Grid';

export default function HomepageInformation() {
    return (
        <Container style={{ 'marginTop': '2%', 'width': '100%' }}>
            <Grid container spacing={2}>
                <Grid item xs={3}></Grid>
                <Grid item xs={6}>
                    <h2 style={{ 'color': 'white', 'fontFamily': 'monospace', 'fontWeight': 'bold'}}>
                        SafeBay Token will support our security protocol! <span style={{ color: "#18FF1E" }}>SafeBay</span> 
                    </h2>
                    <h2 style={{ 'color': 'white', 'fontFamily': 'monospace', 'fontWeight': 'lighter' }}>
                        SafeBay Tokens must be owned in order to use the application and defi protocols. The supply will be burned with every transaction.
                    </h2>
                    <a href="https://stark-cliffs-51978.herokuapp.com/">
                        <img src="SafeBayLogo.svg" alt="SafeBayLogo" style={{ height: "160px", width: "160px" }} />
                    </a>
                </Grid>
                <Grid item xs={3}></Grid>
            </Grid>
        </Container>
    );
}