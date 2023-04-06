// @mui material components
import Card from "@mui/material/Card";
import Grid from "@mui/material/Grid";
import Icon from "@mui/material/Icon";
import DefaultInfoCard from "examples/Cards/InfoCards/DefaultInfoCard";
// Soft UI Dashboard React components
import SoftBox from "components/SoftBox";
import SoftTypography from "components/SoftTypography";

import logoCancellation from "assets/images/small-logos/logo-cancellation.svg"
import logoUtilities from "assets/images/small-logos/logo-utilities.svg"
import logoServices from "assets/images/small-logos/logo-services.svg"
import logoMinMax from "assets/images/small-logos/logo-minmax.svg"

// Images
import wavesWhite from "assets/images/shapes/waves-white.svg";

function GetStarted() {
  return (
    <Card>
      <SoftBox bgColor="#0594e0" p={2}>
        <Grid container spacing={3}>
          <Grid item xs={12} ml={2} lg={6}>
            <SoftBox display="flex" flexDirection="column" height="100%">
              <SoftBox pt={1} mb={0.5}>
                <SoftTypography variant="h4" color="white" fontWeight="medium">
                  How We Work
                </SoftTypography>
              </SoftBox>
            </SoftBox>
          </Grid>
          <Grid container ml={2} mr={2} spacing={3}>
          <Grid item xs={12} md={6} lg={6}>
          <DefaultInfoCard
                    icon={<img src={logoCancellation} alt="cancelation" />}
                    value="Cancelation Policy"
                    prompt="READ MORE"
                  />
          </Grid>
          <Grid item xs={12} md={6} lg={6}>
          <DefaultInfoCard
                    icon={<img src={logoUtilities} alt="utilities" />}
                    value="Utility Costs"
                    prompt="READ MORE"
                  />
          </Grid>
          <Grid item xs={12} md={6} lg={6}>
          <DefaultInfoCard
                    icon={<img src={logoServices} alt="services" />}
                    value="Included Services"
                    prompt="READ MORE"
                  />
          </Grid>
          <Grid item xs={12} md={6} lg={6}>
          <DefaultInfoCard
                    icon={<img src={logoMinMax} alt="minmax" />}
                    value="Min & Max Stay"
                    prompt="READ MORE"
                  />
          </Grid>
        </Grid>
        
        </Grid>
      </SoftBox>
    </Card>
  );
}

export default GetStarted;
