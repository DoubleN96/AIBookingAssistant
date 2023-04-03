// @mui material components
import Grid from "@mui/material/Grid";
import Card from "@mui/material/Card";

// Soft UI Dashboard React components
import SoftBox from "components/SoftBox";
import SoftTypography from "components/SoftTypography";
import StatsCard from "examples/Cards/StatisticsCards/StatsCard";
import piechartConfig from "examples/Charts/PieChart/configs";
import Icon from "@mui/material/Icon";
// Soft UI Dashboard React examples
import DashboardLayout from "examples/LayoutContainers/DashboardLayout";
import Footer from "examples/Footer";
import ProfileInfoCard from "examples/Cards/InfoCards/ProfileInfoCard";
import ProfilesList from "examples/Lists/ProfilesList";
import profilesListData from "layouts/commercial/data/profilesListData"
// Overview page components
import Header from "layouts/commercial/components/Header";
import PlatformSettings from "layouts/commercial/components/PlatformSettings";
import KPIOne from "layouts/commercial/components/KPIOne";
import KPITwo from "layouts/commercial/components/KPITwo";
import GradientLineChart from "examples/Charts/LineCharts/GradientLineChart";
import gradientLineChartData from "layouts/dashboard/data/gradientLineChartData";
import typography from "assets/theme/base/typography";

function Overview() {
  const { size } = typography;
  

  return (
    <DashboardLayout>
      <Header />
      <SoftBox py={3}>
      <SoftBox mb={3}>
          <Grid container spacing={3}>
          <Grid item xs={12} md={6} xl={4}>
            <PlatformSettings />
          </Grid>
          <Grid item xs={12} xl={8}>
            <ProfilesList title="conversations" profiles={profilesListData} />
          </Grid>
          </Grid>
        </SoftBox>
        <SoftBox mb={3}>
          <Grid container spacing={3}>
            <Grid item xs={12} sm={6} xl={3}>
              <StatsCard
                title={{ text: "Booking Link via Chat" }}
                count="93 clicks"
                percentage={{ color: "success", text: "+55%" }}
                icon={{ color: "info", component: "paid" }}
              />
            </Grid>
            <Grid item xs={12} sm={6} xl={3}>
              <StatsCard
                title={{ text: "Property visits" }}
                count="47"
                percentage={{ color: "success", text: "+3%" }}
                icon={{ color: "info", component: "public" }}
              />
            </Grid>
            <Grid item xs={12} sm={6} xl={3}>
              <StatsCard
                title={{ text: "Maintenance Requests" }}
                count="14"
                percentage={{ color: "error", text: "-2%" }}
                icon={{ color: "info", component: "emoji_events" }}
              />
            </Grid>
            <Grid item xs={12} sm={6} xl={3}>
              <StatsCard
                title={{ text: "Rooms Occupied" }}
                count="106"
                percentage={{ color: "success", text: "+5%" }}
                icon={{ color: "info", component: "shopping_cart" }}
              />
            </Grid>
          </Grid>
        </SoftBox>
        <Grid item xs={12} lg={12}>
              <GradientLineChart
                title="ChattyRental Overview"
                description={
                  <SoftBox display="flex" alignItems="center">
                    <SoftBox fontSize={size.lg} color="success" mb={0.3} mr={0.5} lineHeight={0}>
                      <Icon className="font-bold">arrow_upward</Icon>
                    </SoftBox>
                    <SoftTypography variant="button" color="text" fontWeight="medium">
                      4% more{" "}
                      <SoftTypography variant="button" color="text" fontWeight="regular">
                        in 2023
                      </SoftTypography>
                    </SoftTypography>
                  </SoftBox>
                }
                height="20.25rem"
                chart={gradientLineChartData}
              />
            </Grid>
      </SoftBox>
      <Footer />
    </DashboardLayout>
  );
}

export default Overview;
