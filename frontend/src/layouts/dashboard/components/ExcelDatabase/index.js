//coded by Sandra Ashipala for Labláb AI hackathon 04.2023 <https://github.com/sandramsc>
// @mui material components
import Card from "@mui/material/Card";
import Grid from "@mui/material/Grid";
// Soft UI Dashboard React components
import SoftBox from "components/SoftBox";
import SoftTypography from "components/SoftTypography";

// Billing page components
import Bill from "layouts/dashboard/components/Bill";

function ExcelDatabase() {
  return (
    <Card id="delete-account">
        <Grid item xs={12} ml={2} pt={4} lg={6}>
            <SoftBox display="flex" flexDirection="column" height="100%">
              <SoftBox pt={1} mb={0.5}>
                <SoftTypography variant="h4" color="#0594e0" fontWeight="medium">
                  Settings
                </SoftTypography>
              </SoftBox>
            </SoftBox>
          </Grid>
      <SoftBox pb={2} px={2}>
        <SoftBox component="ul" display="flex" flexDirection="column" p={0} m={0}>
          <Bill
            name="DATABASE SPREADSHEET"
            company="ADD YOUR WEBSITE API"
          />
          <Bill
            name="DATABASE SPREADSHEET"
            company="ADD YOUR WEBSITE API"
          />
          <Bill
            name="DATABASE SPREADSHEET"
            company="ADD YOUR WEBSITE API"
          />
        </SoftBox>
      </SoftBox>
    </Card>
  );
}

export default ExcelDatabase;
