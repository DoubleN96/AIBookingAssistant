//coded by Sandra Ashipala for Labláb AI hackathon 04.2023 <https://github.com/sandramsc>

// @mui material components
import Card from "@mui/material/Card";
import Grid from "@mui/material/Grid";
// Soft UI Dashboard React components
import SoftBox from "components/SoftBox";
import SoftTypography from "components/SoftTypography";
import logoWhatsApp from "assets/images/small-logos/logo-whatsapp.svg"
import logoTelegram from "assets/images/small-logos/logo-telegram.svg"
import logoWebBot from "assets/images/small-logos/logo-webbot.svg"
import MiniStatisticsCard from "examples/Cards/StatisticsCards/MiniStatisticsCard";
// Billing page components
import Bill from "layouts/dashboard/components/Bill";

function ExcelDatabase() {
  return (
    <Card id="delete-account">
      <SoftBox bgColor="grey-300">
        <Grid item xs={12} ml={2} pt={4} lg={6}>
            <SoftBox display="flex" flexDirection="column" height="100%">
              <SoftBox pt={1} pb={2.6} mb={0.5}>
                <SoftTypography variant="h4" color="#0594e0" fontWeight="medium">
                  Chat Integrations
                </SoftTypography>
              </SoftBox>
            </SoftBox>
          </Grid>
      <SoftBox pb={2} px={2}>
        <SoftBox component="ul" display="flex" flexDirection="column" p={0} height="25.69rem" m={0}>
        <Grid item xs={12} md={6} mb={2} lg={12}>
        <MiniStatisticsCard
                count="WhatsApp"
                title={{ color: "success", text: "click here to start" }}
                icon={<img src={logoWhatsApp} alt="whatsapp" />}
              />
          </Grid>
          <Grid item xs={12} md={6} mb={2} lg={12}>
        <MiniStatisticsCard
               count="Telegram"
               title={{ color: "success", text: "click here to start" }}
               icon={<img src={logoTelegram} alt="telegram" />}
              />
          </Grid>
          <Grid item xs={12} md={6} mb={2} lg={12}>
        <MiniStatisticsCard
              count="Website chatbot"
              title={{ color: "success", text: "click here to start" }}
              icon={<img src={logoWebBot} alt="chatbot" />}
              />
          </Grid>
        </SoftBox>
      </SoftBox>
      </SoftBox>
    </Card>
  );
}

export default ExcelDatabase;
