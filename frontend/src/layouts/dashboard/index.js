// @mui material components
import Grid from "@mui/material/Grid";
import Icon from "@mui/material/Icon";
import ExcelDatabase from "layouts/dashboard/components/ExcelDatabase";
import ChatInterface from "layouts/dashboard/components/ChatInterface";
// Soft UI Dashboard React components
import SoftBox from "components/SoftBox";
import SoftTypography from "components/SoftTypography";
import DefaultInfoCard from "examples/Cards/InfoCards/DefaultInfoCard";
// Soft UI Dashboard React examples
import DashboardLayout from "examples/LayoutContainers/DashboardLayout";
import DashboardNavbar from "examples/Navbars/DashboardNavbar";
import Footer from "examples/Footer";
import MiniStatisticsCard from "examples/Cards/StatisticsCards/MiniStatisticsCard";

import GradientLineChart from "examples/Charts/LineCharts/GradientLineChart";

// Soft UI Dashboard React base styles
import typography from "assets/theme/base/typography";

// Dashboard layout components
import GetStarted from "layouts/dashboard/components/GetStarted";
import Projects from "layouts/dashboard/components/Projects";
import OrderOverview from "layouts/dashboard/components/OrderOverview";

// Data

import gradientLineChartData from "layouts/dashboard/data/gradientLineChartData";

function Dashboard() {

  return (
    <DashboardLayout>
      <DashboardNavbar />
      <SoftBox py={3}>
        <SoftBox mb={3}>
          <Grid container spacing={2}>
            <Grid item xs={12} lg={12}>
              <GetStarted />
            </Grid>
          </Grid>
        </SoftBox>
        
        <Grid container mb={4} spacing={3}>
          <Grid item xs={12} md={6} lg={8}>
          <ExcelDatabase />
          </Grid>
          <Grid item xs={12} md={6} lg={4}>
          <ChatInterface />
          </Grid>
        </Grid>
      
        <Grid container spacing={3}>
          <Grid item xs={12} md={6} lg={6}>
            <Projects />
          </Grid>
          <Grid item xs={12} md={6} lg={6}>
            <OrderOverview />
          </Grid>
        </Grid>
      </SoftBox>
      <Footer />
    </DashboardLayout>
  );
}

export default Dashboard;
